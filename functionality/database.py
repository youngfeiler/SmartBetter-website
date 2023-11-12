import pandas as pd
import pickle
from .user import User
from .util import map_commence_time_game_id, decimal_to_american, american_to_decimal
import os
import shutil
from .result_updater import result_updater
import numpy as np
from flask import jsonify
import math
from datetime import datetime, timedelta
import ast
import sqlite3
import stripe
import logging
import json

# Configure the logging level for the stripe module
logging.getLogger("stripe").setLevel(logging.ERROR)

STRIPE_PUBLIC_KEY = 'pk_live_51Nm0vBHM5Jv8uc5M5hu3bxlKg6soYb2v9xSg5O7a9sXi6JQJpl7nPWiNKrNHGlXf5g8PFnN6sn0wcLOrixvxF8VH00nVoyGtCk'
STRIPE_PRIVATE_KEY = os.environ.get("API_KEY")
stripe.api_key = STRIPE_PRIVATE_KEY


class database():
    def __init__(self):
        self = self

    def make_conn(self):
        conn = sqlite3.connect('smartbetter.db')
        return conn

    def get_all_usernames(self):
      conn = self.make_conn()
      query = "SELECT username FROM login_info"
      df = pd.read_sql(query, conn)
      self.users= df['username'].tolist()
      conn.close()   # Close the connection
    
    def add_user(self, firstname, lastname, username, password, phone, bankroll, sign_up_date, payed):
       new_user = User(username)

       new_user.create_user(firstname, lastname, username, password, phone, bankroll, sign_up_date, payed)

       self.users = self.get_all_usernames()

    def check_account(self,username):
      conn = self.make_conn()
      df = pd.read_sql('SELECT * FROM login_info', conn)
      conn.close()
      user_info = df[df['username'] == username]
      time_difference = datetime.now() - datetime.strptime(user_info['date_signed_up'].item(), '%Y-%m-%d %H:%M:%S.%f')
    
      days_difference = time_difference.days
      if user_info['payed'].item() or (days_difference <= 8):
        return True
      else:
        return False
          
    def check_login_credentials(self, username, password):
      #df = pd.read_csv('users/login_info.csv')
      conn = self.make_conn()
      df = pd.read_sql('SELECT * FROM login_info', conn)
      conn.close()   # Close the connection
      user_info = df[df['username'] == username]
      if user_info.empty:
        return False
      else:
        if password == user_info['password'].item():
          return True
    
    def check_duplicate_account(self,username):
        self.check_payments()
        conn = self.make_conn()
        df = pd.read_sql('SELECT * FROM login_info', conn)
        conn.close()   # Close the connection
        user_info = df[df['username'] == username]
        if user_info['payed'].item():
          conn = self.make_conn()
          #remove this row from the df and push it back to sqllite
          df = df[df['username'] != username]
          df.to_sql('login_info', conn, if_exists='replace', index=False)
          conn.close()
          return True
        else:
          conn.close()
          return False
        
    def get_user_bank_roll(self, user):
        #df = pd.read_csv('users/login_info.csv')
        conn = self.make_conn()
        df = pd.read_sql('SELECT * FROM login_info', conn)
        conn.close()   # Close the connection
        user_df = df[df['username'] == user]
        return user_df['bankroll'].iloc[0]

    def add_to_bankroll(self, user, amount):
         try:
          conn = self.make_conn()
          df = pd.read_sql('SELECT * FROM login_info', conn)
          conn.close()   # Close the connection
          #df = pd.read_csv('users/login_info.csv')

          user_df = df[df['username'] == user]

          new_bankroll = float(user_df['bankroll'].iloc[0]) + float(amount)

          df.loc[df['username'] == user, 'bankroll'] = new_bankroll
          #back to conn db 
          conn = self.make_conn()
          df.to_sql('login_info', conn, if_exists='replace', index=False)
          #df.to_csv('users/login_info.csv', index=False)
          conn.close()  # Commit the changes

          return True
         except:
            conn.close()
            return False
    
    def update_bankroll(self, user, amount):
         try:
          conn = self.make_conn()
          df = pd.read_sql('SELECT * FROM login_info', conn)
          conn.close()   # Close the connection
          #df = pd.read_csv('users/login_info.csv')

          user_df = df[df['username'] == user]

          new_bankroll = amount

          df.loc[df['username'] == user, 'bankroll'] = new_bankroll
          #back to conn db 
          conn = self.make_conn()
          df.to_sql('login_info', conn, if_exists='replace', index=False)
          #df.to_csv('users/login_info.csv', index=False)
          conn.close()  # Commit the changes

          return True
         except:
            conn.close()
            return False

    def get_recommended_bet_size(self, user, df):
       df['decimal_highest_bettable_odds'] = df['highest_bettable_odds'].apply(american_to_decimal)
       df['win_prob'] =  (1 / df['average_market_odds']) 
       bankroll = self.get_user_bank_roll(user)
       bankroll = float(bankroll)
       df['bet_amount'] = (((df['decimal_highest_bettable_odds'] - 1) * df['win_prob'] - (1 - df['win_prob'])) / (df['decimal_highest_bettable_odds']- 1)) * 0.5 * bankroll
                          #((    Decimal Odds                    – 1) * Decimal Winning Percentage – (1 – Winning Percentage)) / (Decimal Odds – 1) * Kelly Multiplier
       df['bet_amount'] = df['bet_amount'].round(2)
       return df
   
    def add_made_bet_to_db(self, jayson):
      #drop dollar sign from bet amount
      jayson['bet_amount'] = jayson['bet_amount'].replace('$', '')
      df = pd.DataFrame(columns=jayson.keys())
      df = df.append(jayson, ignore_index =True)
      odds = int(df['highest_bettable_odds'])
      df['bet_profit'] = np.where(odds > 0, (odds * float(df['bet_amount'])) /100, float(df['bet_amount']) /(-1 * odds/100))
      df['time_placed'] = datetime.now()
      #change time_placed to a datetime supported by sqlite 
      #change df['date'] from y-m-d to d-m-y where y is a two digit year
      df['time_placed'] = df['time_placed'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
      conn = self.make_conn()
      read_in = pd.read_sql('SELECT * FROM placed_bets', conn)
      put_out = read_in.append(df, ignore_index=True)
      put_out.to_sql('placed_bets', conn, if_exists='replace', index=False)
      conn.close() 
      return
      
    def get_live_dash_data(self, user_name, sport):
       
       # TODO: Check this logic
       def american_to_decimal(american_odds):
        positive_mask = american_odds > 0
        negative_mask = american_odds < 0
        decimal_odds = np.empty_like(american_odds, dtype=float)
        decimal_odds[positive_mask] = (american_odds[positive_mask] / 100) + 1
        decimal_odds[negative_mask] = (100 / np.abs(american_odds[negative_mask])) + 1
        decimal_odds[~(positive_mask | negative_mask)] = 1.0 
        return decimal_odds

       def minutes_seconds(row):
          
          seconds = int(float(row['time_difference_seconds']))
          if seconds < 60:
            row['time_difference_formatted'] = f'{seconds} sec'

          elif seconds >= 60 and seconds < 3600:
            minutes = math.floor(seconds / 60)
            new_seconds = (seconds % 60)
            row['time_difference_formatted'] = f'{minutes} min {new_seconds} sec'
             
          else:
            hours = math.floor(seconds / 3600)
            seconds_after_hour = seconds % 3600
            new_minutes = math.floor(seconds_after_hour / 60)
            new_seconds = seconds_after_hour % 60
            row['time_difference_formatted'] = f'{hours} hours {new_minutes} min {new_seconds} sec'
          
          return row

       def format_list_of_strings(strings):
           return ', '.join(strings[0])
      
       def calculate_accepted_bettable_odds(row):
        value_new = row['highest_bettable_odds']
        if value_new < 0:
          if value_new < -500:
             value_new = value_new + (value_new * 0.1)
          else:
             value_new = value_new + (value_new * 0.05)
        else:
          if value_new > 500:
             value_new = value_new - (value_new * 0.1)
          else:
             if (value_new - (value_new * 0.05)) <= 100: 
                less_than_100 = 100 - (value_new - (value_new * 0.05))
                value_new = -100 - less_than_100
             else:
              value_new = value_new - (value_new * 0.05)
        #round value_new to nearest whole number 
        value_new = round(value_new)
        return value_new
       
       conn = self.make_conn()
       scores_df = pd.read_sql('SELECT * FROM scores', conn)
       conn.close()

       df = pd.read_csv('users/master_model_observations.csv')
       
       df_sport = df[df['sport_title'] == sport]
       
       filtered_df = df_sport[df_sport['completed'] == False]

       filtered_df.sort_values(by='snapshot_time', ascending=False, inplace=True)

       columns_to_compare = ['team']

       df_no_duplicates = filtered_df.drop_duplicates(subset=columns_to_compare)

       def decimal_to_american(decimal_odds):
        american_odds = np.where(decimal_odds >= 2.0, (decimal_odds - 1) * 100, -100 / (decimal_odds - 1))
        return american_odds.astype(int)

        # Apply the conversion function using NumPy vectorization
       df_no_duplicates['highest_bettable_odds'] = decimal_to_american(df_no_duplicates['highest_bettable_odds'])
       
       first_20_rows = df_no_duplicates.head(20)

       if 'team' in first_20_rows.columns:
          first_20_rows['team_1'] = first_20_rows['team']
       else:
          pass
       
       if not first_20_rows.empty:
        first_20_rows['highest_acceptable_odds']= first_20_rows.apply(calculate_accepted_bettable_odds, axis=1)

        # first_20_rows['highest_acceptable_odds'] = decimal_to_american(first_20_rows['highest_acceptable_odds'])

       current_time = datetime.now() 

       first_20_rows['current_time'] = current_time + pd.Timedelta(hours=2)

       first_20_rows['snapshot_time'].apply(pd.to_datetime)

       first_20_rows['current_time'] = pd.to_datetime(first_20_rows['current_time'])

       first_20_rows['snapshot_time'] = pd.to_datetime(first_20_rows['snapshot_time'])

        # Format the datetime object as "Thu, Nov 9, 2023"
       first_20_rows['game_date'] = pd.to_datetime(first_20_rows['game_date']).dt.strftime("%a %b %d, %Y")

       first_20_rows['time_difference_seconds'] = (first_20_rows['current_time'] - first_20_rows['snapshot_time']).dt.total_seconds()
        
       first_20_rows['sportsbooks_used'] = first_20_rows['sportsbooks_used'].apply(ast.literal_eval)

       first_20_rows['sportsbooks_used'] = first_20_rows['sportsbooks_used'].apply(lambda x: format_list_of_strings([x]))
       
       first_20_rows = first_20_rows.apply(minutes_seconds, axis=1)

       first_20_rows = self.get_recommended_bet_size(user_name, first_20_rows)

       first_20_rows = self.filter_5_min_cooloff(user_name, sport, first_20_rows)

       first_20_rows['ev'] = first_20_rows['ev'].round(1)

       return first_20_rows
    
    def get_unsettled_bet_data(self, user):
      conn = self.make_conn()
      #df = pd.read_csv('users/placed_bets.csv')
      df = pd.read_sql('SELECT * FROM placed_bets', conn)
      #scores_df = pd.read_csv('mlb_data/scores.csv')
      scores_df = pd.read_sql('SELECT * FROM scores', conn)
      conn.close()   # Close the connection
      df = df[df['user_name'] == user]

      df['highest_bettable_odds'] = df['highest_bettable_odds'].astype(float)
      df['bet_amount'] = df['bet_amount'].astype(float)


      df['bet_profit'] = np.where(df['highest_bettable_odds'] > 0, (df['highest_bettable_odds'] * df['bet_amount']) /100, df['bet_amount'] /(-1 * df['highest_bettable_odds']/100))



      scores_df = scores_df[['game_id', 'winning_team']]

      merged_df = df.merge(scores_df, on='game_id', how='left')

      filtered_df = merged_df[merged_df['winning_team'].isna()]
      grouped_df = filtered_df.groupby(['game_id', 'team'])

      filtered_df['amount_of_bets'] = grouped_df['game_id'].transform('size')
      filtered_df['highest_odds'] = grouped_df['highest_bettable_odds'].transform('max')
      filtered_df['p_l'] = grouped_df['bet_profit'].transform('sum')
      filtered_df['total_bet_amount'] = grouped_df['bet_amount'].transform('sum')
      filtered_df['average_odds_dec'] = (filtered_df['p_l'] + filtered_df['total_bet_amount']) / filtered_df['total_bet_amount']
      filtered_df['average_odds'] = filtered_df['average_odds_dec'].apply(decimal_to_american)



      game_id_df = filtered_df.drop_duplicates(subset=['team'])
      game_id_df_grouped = game_id_df.groupby('game_id')


      def calculate_if_win(group):
        if len(group) == 2:
            row1 = group.iloc[0]
            row2 = group.iloc[1]
            result1 = row1['p_l'] - row2['total_bet_amount']
            result2 = row2['p_l'] - row1['total_bet_amount']
            group.loc[group.index[0], 'if_win'] = result1
            group.loc[group.index[1], 'if_win'] = result2

            group.loc[group.index[0], 'team'] = row1['team'].split('v.')[0]
            group.loc[group.index[1], 'team'] = row2['team'].split('v.')[0]

        elif len(group) == 1:
            row = group.iloc[0].copy()
            row['ev'] = ''
            row['team'] = group.iloc[0]['team'].split('v.')[1]
            row['highest_bettable_odds'] = ''
            row['sportsbook'] = ''
            row['bet_profit'] = ''
            row['amount_of_bets'] = ''
            row['average_odds'] = ''
            row['highest_odds'] = ''
            row['p_l'] = ''
            row['total_bet_amount'] = 0
            group = group.append(row, ignore_index=True) 
            group.loc[group.index[0], 'if_win'] = group.iloc[0]['p_l']
            group.loc[group.index[1], 'if_win'] = group.iloc[0]['total_bet_amount'] * -1
            group.loc[group.index[0], 'team'] = group.iloc[0]['team'].split('v.')[0]
        return group
      

      game_id_df_grouped = game_id_df_grouped.apply(calculate_if_win).reset_index(drop=True)

      game_id_df_grouped['if_win'] = round(game_id_df_grouped['if_win'],1)
      game_id_df_grouped['average_odds'] = game_id_df_grouped['average_odds'].apply(lambda x: round(x, 0) if isinstance(x, (int, float)) else x)



      return_df = game_id_df_grouped[['game_id', 'team', 'user_name', 'average_odds', 'highest_odds', 'if_win']]

      return return_df
    
    def calculate_user_bankroll(self, username):
      conn = self.make_conn()
      placed_bets = pd.read_sql('SELECT * FROM placed_bets', conn)
      login_info = pd.read_sql('SELECT * FROM login_info', conn)
      current_bankroll = self.get_user_bank_roll(username)
      placed_bets = placed_bets[placed_bets['user_name'] == username]
      scores_df = pd.read_sql('SELECT * FROM scores', conn)
      profit_by_book = pd.read_sql('SELECT * FROM profit_by_book', conn)
      conn.close()   # Close the connection


      scores_df = scores_df[['game_id', 'winning_team']]
      merged_df = placed_bets.merge(scores_df, on='game_id', how='left')
      merged_df = merged_df[merged_df['winning_team'].notna()]
      merged_df['team_bet_on'] = [cell.split('v.')[0] for cell in merged_df['team']]

      merged_df['bet_profit'] = merged_df['bet_profit'].astype(float)
      merged_df['bet_amount'] = merged_df['bet_amount'].astype(float)

      # merged_df['bet_result'] = np.where(merged_df['winning_team'] == merged_df['team_bet_on'], merged_df['bet_profit'], merged_df['bet_profit'] * -1)
      merged_df['bet_result'] = np.where(merged_df['winning_team'] == merged_df['team_bet_on'], merged_df['bet_profit'], merged_df['bet_amount'] * -1)
      #call calculate_p_l_by_book
      #profit_by_book = pd.read_csv('users/profit_by_book.csv')
    

      if username in profit_by_book['username'].values:
          #if it does, remove the row
          profit_by_book = profit_by_book[profit_by_book['username'] != username]
      #make a new df called append_df with the same columns as profit_by_book
      append_columns = profit_by_book.columns.to_list()
      append_df = pd.DataFrame(columns = append_columns)
      #add a row in append_df with 'username' as username and all of the other columns as 0
      append_df.loc[0, 'username'] = username
      #make all other columns at row 0 = 0
      append_df = append_df.fillna(0)
      #for each row in merged_df
      for idx, row in merged_df.iterrows():

        ls = row['sportsbooks_used'].split(', ')
        # for each element in ls replace [ and ] with nothing
        ls = [element.replace('[', '').replace(']', '').replace("'","") for element in ls]
        for book in ls:
          # Check if the book already exists in append_df DataFrame columns
          if book in append_df.columns:
            # If it does, add the profit/loss to the existing value 
            append_df[book][0] += row['bet_result']
          else:
            # If it doesn't, add the book as a new column
            #make a new column that is named book 
            append_df[book] = 0 
            append_df[book][0] += row['bet_result']

      #append append_df to profit_by_book
      #profit_by_book = profit_by_book.append(append_df, ignore_index=True)
      #profit_by_book.to_csv('users/profit_by_book.csv', index=False)
      #profit_by_book.to_sql('profit_by_book', conn, if_exists='replace', index=False)
      # calculate total profit/loss of all bets in placed_bets 
      total_profit_loss = merged_df['bet_result'].sum()
      # add total profit/loss to current bankroll
      new_bankroll = round(float(current_bankroll) + total_profit_loss, 2)
      # update users/login_info.csv with new bankroll
      login_info[login_info['username'] == username]['bankroll'].iloc[0] = new_bankroll
      #login_info.to_csv('users/login_info.csv', index=False)
      conn = self.make_conn()
      login_info.to_sql('login_info', conn, if_exists='replace', index=False)
      conn.close()   # Close the connection
      
      return new_bankroll
      
    def filter_5_min_cooloff(self, username, sport, df):
       conn = self.make_conn()
       placed_bets = pd.read_sql('SELECT * FROM placed_bets', conn)
       conn.close()

       user_df = placed_bets[placed_bets['user_name'] == username]

       user_df['time_placed'] = pd.to_datetime(user_df['time_placed'])

       user_time_df = user_df[(datetime.now()- user_df['time_placed']  < pd.Timedelta(seconds=300))]

       if sport == "NFL":
          user_time_df['teams_bet_on'] = user_time_df['team'].str.split('v.').str[0]
          df = df[~df['team_1'].isin(user_time_df['teams_bet_on'])]

       elif sport == "MLB":
          user_time_df['teams_bet_on'] = user_time_df['team'].str.split('v.').str[0]
          df = df[~df['team'].isin(user_time_df['teams_bet_on'])]

       return df

    def check_payments(self):
      conn = self.make_conn()
      try:
            # List all PaymentIntents from Stripe
            payment_intents = stripe.PaymentIntent.list()
            paid_users = set()  # Create a set to store usernames of paid users

            # Iterate through the PaymentIntents and add the usernames of paid users to the set
            for payment_intent in payment_intents.data:
                if payment_intent.customer:
                    customer = stripe.Customer.retrieve(payment_intent.customer)
                    email = customer.email
                    paid_users.add(email)

            # Update the 'paid' column in the SQLite database
            cursor = conn.cursor()
            for username in paid_users:
                cursor.execute("UPDATE login_info SET payed = 1 WHERE username = ?", (username,))
                conn.commit()

            cursor.close()

      except stripe.error.StripeError as e:
            print(f"Stripe Error: {e}")
      except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
      conn.close()
      return

    def get_user_info(self, username):
      conn = self.make_conn()
      df = pd.read_sql('SELECT * FROM login_info', conn)
      conn.close()
      df = df[df['username'] == username]
      return df.to_dict('records')

    def cancel_subscription(self,username):
      try:
        # Get the user's subscription ID from the Stripe API
        customer = stripe.Customer.list(email=username)
        subscriptions = stripe.Subscription.list(customer=customer.data[0].id)
        
        if subscriptions.data:
            subscription_id = subscriptions.data[0].id

            # Cancel the subscription in Stripe
            canceled_subscription = stripe.Subscription.delete(subscription_id)

            if canceled_subscription.status == 'canceled':
                # Update the 'paid' column in the SQLite database
                conn = sqlite3.connect('smartbetter.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE login_info SET payed = 0 WHERE username = ?", (username,))
                conn.commit()
                conn.close()
                
                return True, "Subscription canceled successfully."
    
        return False, "No active subscription found for this user."
      except stripe.error.StripeError as e:
        return False, str(e)
    
    def get_scenario_results(self, data_holder, input):
      if input['sport'] == "NFL":
        data = data_holder.raw_nfl_odds_data
      elif input['sport'] == "NBA":
         data = data_holder.raw_nba_odds_data
      
      for key, val in input.items():
          if isinstance(val, list) and len(val) > 1:
            try:
              data = data[data[key].isin(val)]
            except Exception as e:
               pass
          elif isinstance(val, list) and len(val) ==1:
            try:
               data = data[data[key]== val]
            except Exception as e:
               pass

      data['my_game_id'] = data['game_id'] + data['team_1']

      grouped = data.groupby('my_game_id')

      closest_observations = []

      # Step 2-4: Find the closest observation for each game
      for game_id, group in grouped:
          filtered_group = group[group['minutes_since_commence'] <= 0]
          if not filtered_group.empty:
              filtered_group = filtered_group[filtered_group['highest_bettable_odds'] > 0]
              filtered_group['abs_diff'] = abs(filtered_group['minutes_since_commence'] - 0)
              closest_observation = filtered_group[filtered_group['abs_diff'] == filtered_group['abs_diff'].min()]
              closest_observations.append(closest_observation)

      result_df = pd.concat(closest_observations, ignore_index=True)

      result_df.to_csv('/Users/micahblackburn/Desktop/RESULT_DF_1.CSV', index=False)

      result_df['result'] = np.where(result_df['target'] == 1, result_df['highest_bettable_odds'] - 1, -1)

      result_df.sort_values(by = 'snapshot_time', inplace=True)

      result_df['running_sum'] = result_df['result'].cumsum()

      result_df.to_csv('/Users/micahblackburn/Desktop/RESULT_DF.CSV', index=False)

      result_df['date'] = pd.to_datetime(result_df['snapshot_time'].dt.date)

      grouped = result_df.groupby('date')['result'].sum()

      new_df = result_df.groupby('date')['result'].sum().reset_index()

      new_df['running_sum'] = new_df['result'].cumsum()



      return jsonify(data=new_df.to_json(orient='records', date_format='iso'))