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
import stripe
import logging
import json
from functionality.models import LoginInfo  # Import your SQLAlchemy model
from sqlalchemy.orm.exc import NoResultFound
from ast import literal_eval
import pytz


# Configure the logging level for the stripe module
logging.getLogger("stripe").setLevel(logging.ERROR)

STRIPE_PUBLIC_KEY = 'pk_live_51Nm0vBHM5Jv8uc5M5hu3bxlKg6soYb2v9xSg5O7a9sXi6JQJpl7nPWiNKrNHGlXf5g8PFnN6sn0wcLOrixvxF8VH00nVoyGtCk'
STRIPE_PRIVATE_KEY = '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'
stripe.api_key = STRIPE_PRIVATE_KEY


class database():
    def __init__(self, db_manager):
        self = self
        self.db_manager = db_manager

    def get_all_usernames(self):
      try:
        session = self.db_manager.create_session()
        usernames = session.query(LoginInfo.username).all()

        usernames_list = [username[0] for username in usernames]

        self.users = usernames_list
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()
        return
      
    def get_scores(self):
      try:
          session = self.db_manager.create_session()
          read_in =  pd.read_sql_table('scores', con=self.db_manager.get_engine())
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()
        return read_in
    
    def add_user(self, firstname, lastname, username, password, phone, bankroll, sign_up_date, payed):
       new_user = User(username)

       print("adding user")

       new_user.create_user(firstname, lastname, username, password, phone, bankroll, sign_up_date, payed, self.db_manager)

       self.users = self.get_all_usernames()
       print(self.users)
       return

    def check_account(self,username):
      try:
        # Create a session
        session = self.db_manager.create_session()
        
        # Query the user's record by username
        user = session.query(LoginInfo).filter_by(username=username).first()
        
        if user:
            
            # Calculate the time difference
            time_difference = datetime.now() - (datetime.strptime(user.date_signed_up, '%Y-%m-%d %H:%M:%S.%f'))
            # Calculate the days difference
            days_difference = time_difference.days
            
            # Check if the user is paid or signed up within the last 8 days
            if user.payed or days_difference <= 8:
                return True
            else:
                return False
        else:
            return False
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()
     
    def check_login_credentials(self, username, password):

      
      try:
        # Create a session
        session = self.db_manager.create_session()

        # Query the user by username
        try:
            user = session.query(LoginInfo).filter_by(username=username).one()
            print(user)
            print("WAHOOOO STEFAN SUCKS BALLS")
        except NoResultFound:
            return False
# Check if the password matches
        if user.password == password:
            return True
        else:
            return False
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()
    
    def check_duplicate_account(self,username):
      print("checking duplicate account")
      self.check_payments()
      try:
        # Create a session
        session = self.db_manager.create_session()

        # Query the user's record by username
        user = session.query(LoginInfo).filter_by(username=username).first()

        if user and user.payed:
            # If the user exists and is paid, you can remove the user record
            # from the database using SQLAlchemy
            session.delete(user)
            session.commit()
            return True
        else:
            return False
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()

    def get_permission(self, username):
      try:
          customer = stripe.Customer.list(email=username)
          customer_id = customer.data[0].id if customer.data else None
          if customer_id:
              user_subscriptions = stripe.Subscription.list(customer=customer_id)
              if user_subscriptions.data:
                  highest_price = 0
                  highest_price_subscription = None
                  for subscription in user_subscriptions.data:
                      for item in subscription['items']['data']:
                          price = item['price']['unit_amount']
                          price_id = item['price']['unit_amount']
                          if price > highest_price:
                              highest_price = price
                              highest_price_subscription = subscription
                              highest_price_price_id= price_id
                  if highest_price_subscription:
                      highest_price_status = highest_price_subscription.get('status')
                      print("Highest Priced Subscription:")
                      print(highest_price)
                      print("Highest Priced Status:")
                      print(highest_price_status)
                      print("Highest Priced id:")
                      print(highest_price_price_id)
                      return({
                         'status':highest_price_status,
                         'permission':self.get_plan_from_price_id(highest_price_price_id)
                         })
                  else:
                      return({
                         'status': 'none',
                         'permission': 'free' 
                         })
              else:
                  return({
                         'status': 'none',
                         'permission': 'free' 
                         })
          else:
              return({
                         'status': 'none',
                         'permission': 'free' 
                         })

      except stripe.error.StripeError as e:
          print(f"Stripe Error: {e}")
          return None

    def get_plan_from_price_id(self, price_id):
       plans = {
        'price_1OSlSoHM5Jv8uc5MR6vK5xrA':'ev',
        'price_1OG9CDHM5Jv8uc5MTtdQOZMv': 'standard',
        'price_1NqdGPHM5Jv8uc5MkYrJm2UX': 'premium',
        'price_1OG9DhHM5Jv8uc5MfiE2UdHR': 'premium',
      }
       return plans.get(price_id, 'Not found in plans')
 
    def get_user_bank_roll(self, user):
      try:
        # Create a session
        session = self.db_manager.create_session()

        # Query the user's record by username
        user = session.query(LoginInfo).filter_by(username=user).first()

        if user:
            # If the user exists, you can directly access the 'bankroll' attribute
            return user.bankroll
        else:
            return None
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()

    def add_to_bankroll(self, username, amount):
      try:
        # Create a session
        session = self.db_manager.create_session()

        # Query the user's record by username
        user = session.query(LoginInfo).filter_by(username=username).first()

        if user:
            # If the user exists, update the bankroll
            new_bankroll = float(user.bankroll) + float(amount)
            user.bankroll = new_bankroll
            session.commit()
            return True
        else:
            return False
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()
  
    def update_bankroll(self, username, amount):
      try:
        # Create a session
        session = self.db_manager.create_session()

        # Query the user's record by username
        user = session.query(LoginInfo).filter_by(username=username).first()

        if user:
            # If the user exists, update the bankroll
            user.bankroll = amount
            session.commit()
            return True
        else:
            return False
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()

    def get_recommended_bet_size(self, bankroll, df):
       
       df['decimal_highest_bettable_odds'] = df['highest_bettable_odds'].apply(american_to_decimal)

       df['win_prob'] =  (1 / df['average_market_odds']) 

       bankroll = float(bankroll)

       df['bet_amount'] = ((df['win_prob'] * df['decimal_highest_bettable_odds']) - 1) / (df['decimal_highest_bettable_odds']-1) * 0.5 * bankroll

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
      try:
          session = self.db_manager.create_session()
          read_in =  pd.read_sql_table('placed_bets', con=self.db_manager.get_engine())
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()
      put_out = read_in.append(df, ignore_index=True)
      try:
          put_out.to_sql('placed_bets', con=self.db_manager.get_engine(), if_exists='replace', index=False)
      except Exception as e:
        print(e)
        return str(e)
      return
      
    def get_live_dash_data(self, bankroll, sport):

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
       
       def calculate_accepted_bettable_odds_pos_ev_no_ai(row):
          value_new = row['highest_bettable_odds']
          # rewrite to make each thing still +EV
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
          
       filtered_df = None

       try:
          session = self.db_manager.create_session()
          engine = self.db_manager.get_engine()
          if sport == "POSITIVE_EV":
            filtered_df = pd.read_csv("/Users/stefanfeiler/Desktop/headers.csv")

          elif sport == "PREGAME": 
            query = """
            SELECT *
            FROM master_model_observations
            WHERE sport_title LIKE '%%PREGAME%%'
            """
            filtered_df = pd.read_sql_query(query, engine)

          else:
            query = """
            SELECT *
            FROM master_model_observations
            WHERE sport_title = %s AND completed = 0 AND average_market_odds > 0.01
            ORDER BY snapshot_time DESC
            """
            filtered_df = pd.read_sql_query(query, engine, params=[sport])

       except Exception as e:
        print(e)
        return str(e)
       finally:
            if session:
                session.close()

       
       if sport != 'POSITIVE_EV':
        filtered_df = filtered_df[filtered_df['completed'] == False]
        filtered_df = filtered_df.dropna(subset=['team'])
        filtered_df = filtered_df.dropna(subset=['opponent'])
        filtered_df = filtered_df[filtered_df['team'].astype(str).str.strip() != '']
        filtered_df.sort_values(by="snapshot_time", ascending=False, inplace=True)
        columns_to_compare = ['team']
        df_no_duplicates = filtered_df.drop_duplicates(subset=columns_to_compare)
       else:
          df_no_duplicates = filtered_df.drop_duplicates()


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

       current_time = datetime.now() 

       first_20_rows['current_time'] = current_time + pd.Timedelta(hours=2)

       first_20_rows['snapshot_time'].apply(pd.to_datetime)

       first_20_rows['current_time'] = pd.to_datetime(first_20_rows['current_time'])

       first_20_rows['snapshot_time'] = pd.to_datetime(first_20_rows['snapshot_time'])

        # Format the datetime object as "Thu, Nov 9, 2023"
       first_20_rows['game_date'] = pd.to_datetime(first_20_rows['game_date']).dt.strftime("%a %b %d, %Y")

       first_20_rows['time_difference_seconds'] = (first_20_rows['current_time'] - first_20_rows['snapshot_time']).dt.total_seconds()

       if sport == "NFL":
          first_20_rows['time_difference_seconds'] = first_20_rows['time_difference_seconds'] -32400
       elif sport == "NBA" or sport == "NHL" or sport == "PREGAME":
          first_20_rows['time_difference_seconds'] = first_20_rows['time_difference_seconds'] -21600
          
       first_20_rows['sportsbooks_used'] = first_20_rows['sportsbooks_used'].apply(ast.literal_eval)

       first_20_rows['sportsbooks_used'] = first_20_rows['sportsbooks_used'].apply(lambda x: format_list_of_strings([x]))
       
       first_20_rows = first_20_rows.apply(minutes_seconds, axis=1)

       first_20_rows = self.get_recommended_bet_size(bankroll, first_20_rows)

      #  first_20_rows = self.filter_5_min_cooloff(user_name, first_20_rows)

       first_20_rows['ev'] = first_20_rows['ev'].round(1)

       return first_20_rows

    def get_positive_ev_dash_data(self, filters, user_bankroll):
       
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

        pwin = row['no_vig_prob_1']
        plose = 1-row['no_vig_prob_1']
        winnings_needed = plose/pwin
        decimal_odds = winnings_needed + 1
        if decimal_odds > 2:
           return int((decimal_odds - 1) * 100)
        else:
           return int(-100 / (decimal_odds - 1))
      
       def decimal_to_american(decimal_odds):
        american_odds = np.where(decimal_odds >= 2.0, (decimal_odds - 1) * 100, -100 / (decimal_odds - 1))
        return american_odds.astype(int) 
       
       def calculate_bet_amount(row, user_bankroll):
          odds = row['highest_bettable_odds'] 
          win_probability = row['no_vig_prob_1']
          kelly_percentage = ((win_probability * odds) - 1) / (odds-1)
          return kelly_percentage * user_bankroll * 0.25

       df = pd.read_csv("users/positive_ev_dash_data.csv")

       df = df[df['highest_bettable_odds'] > 1.01]

       df['game_date'] = pd.to_datetime(df['game_date'])

       current_time_gmt = datetime.now(pytz.timezone('GMT'))

       df = df[df['game_date'] >= current_time_gmt]

       df['game_date']= (df['game_date'] - pd.Timedelta(hours=6)).dt.strftime('%A, %B %d, %Y')

       df['sportsbooks_used_formatted'] = df['sportsbooks_used'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)

       if len(filters) > 1:
          if filters['sport-league-filter'].upper() != 'ALL':
            df = df[df['sport_league_display'] == filters['sport-league-filter']]
          if filters['market-filter'].upper() != 'ALL':
            df = df[df['market_display'] == filters['market-filter'].title()]
          if filters['game-date-filter'].upper() != 'ALL':
            df = df[df['game_date']== filters['game-date-filter'].title()]
          if filters['sportsbook-filter'].upper() != 'ALL':
            df = df[df['sportsbooks_used_formatted'].apply(lambda x: filters['sportsbook-filter'].title() in x)]
          
       df.drop(columns=['sportsbooks_used_formatted'], inplace=True)

       df_no_duplicates = df.drop_duplicates()

       df_no_duplicates['bet_amount'] = df_no_duplicates.apply(calculate_bet_amount, args=(user_bankroll,), axis=1)

       df_no_duplicates['bet_amount'] = df_no_duplicates['bet_amount'].round(2)

      # Apply the conversion function using NumPy vectorization
       
       df_no_duplicates['highest_bettable_odds'] = decimal_to_american(df_no_duplicates['highest_bettable_odds'])
       
       first_20_rows = df_no_duplicates

       if 'team' in first_20_rows.columns:
          first_20_rows['team_1'] = first_20_rows['team']
       else:
          pass
       
       if not first_20_rows.empty:
        first_20_rows['highest_acceptable_odds']= first_20_rows.apply(calculate_accepted_bettable_odds, axis=1)

       current_time = datetime.now() 

       first_20_rows['current_time'] = current_time #- pd.Timedelta(hours=7)

       first_20_rows['snapshot_time'].apply(pd.to_datetime)

       first_20_rows['current_time'] = pd.to_datetime(first_20_rows['current_time'])

       first_20_rows['snapshot_time'] = pd.to_datetime(first_20_rows['snapshot_time'])

       first_20_rows['game_date'] = first_20_rows['game_date'].apply(lambda x: pd.to_datetime(x).strftime('%a %b %d, %Y'))

       first_20_rows['time_difference_seconds'] = (first_20_rows['current_time'] - first_20_rows['snapshot_time']).dt.total_seconds()
        
       first_20_rows['sportsbooks_used'] = first_20_rows['sportsbooks_used'].apply(ast.literal_eval)

       first_20_rows['sportsbooks_used'] = first_20_rows['sportsbooks_used'].apply(lambda x: format_list_of_strings([x]))
       
       first_20_rows = first_20_rows.apply(minutes_seconds, axis=1)

       first_20_rows['ev'] = first_20_rows['ev'].round(1)

       first_20_rows.sort_values(filters['sort-by'][0], ascending = filters['sort-by'][1], inplace= True)

       return first_20_rows.head(200)
  
    def get_unsettled_bet_data(self, user):
      try:
        session = self.db_manager.create_session()
        scores_df = pd.read_sql_table('scores', con=self.db_manager.get_engine())
        df = pd.read_sql_table('placed_bets', con=self.db_manager.get_engine())
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()
      df = df[df['user_name'] == user]

      df['highest_bettable_odds'] = df['highest_bettable_odds'].astype(float)

      df['bet_amount'] = df['bet_amount'].astype(float)

      df['bet_profit'] = np.where(df['highest_bettable_odds'] > 0, (df['highest_bettable_odds'] * df['bet_amount']) /100, df['bet_amount'] /(-1 * df['highest_bettable_odds']/100))

      scores_df = scores_df[['game_id', 'winning_team']]

      merged_df = df.merge(scores_df, on='game_id', how='left')

      filtered_df = merged_df[merged_df['winning_team'].isna()]
      filtered_df['team'] = filtered_df['team'].str.replace(r'\s+v\.', 'v.')
      filtered_df['team'] = filtered_df['team'].str.replace(r'v\.\s+', 'v.')
      filtered_df['team'] = filtered_df['team'].str.replace(r'\s*v\.\s*', 'v.')
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
      try:
        engine = self.db_manager.get_engine()
        session = self.db_manager.create_session()

        # SQL query to fetch filtered placed bets
        placed_bets_query = f"""
        SELECT pb.*
        FROM placed_bets pb
        WHERE pb.user_name = %s
        """
        placed_bets = pd.read_sql_query(placed_bets_query, engine, params=[username])

        # SQL query to fetch only game_id and winning_team from scores
        scores_query = """
        SELECT game_id, winning_team
        FROM scores
        """
        scores_df = pd.read_sql_query(scores_query, engine)

        # SQL query to perform the merge (join) operation
        merged_query = f"""
        SELECT pb.*, sc.winning_team
        FROM placed_bets pb
        LEFT JOIN scores sc ON pb.game_id = sc.game_id
        WHERE pb.user_name = %s AND sc.winning_team IS NOT NULL
        """
        merged_df = pd.read_sql_query(merged_query, engine, params=[username])
        print(datetime.now())
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()

      print('time to run pandas stuff')
      print(datetime.now())
      current_bankroll = self.get_user_bank_roll(username)

      merged_df['team'] = merged_df['team'].str.replace(r'\s+v\.', 'v.')
      merged_df['team'] = merged_df['team'].str.replace(r'v\.\s+', 'v.')
      merged_df['team'] = merged_df['team'].str.replace(r'\s*v\.\s*', 'v.')

      merged_df['team_bet_on'] = [cell.split('v.')[0] for cell in merged_df['team']]

      merged_df['bet_profit'] = merged_df['bet_profit'].astype(float)
      merged_df['bet_amount'] = merged_df['bet_amount'].astype(float)
      merged_df['bet_result'] = np.where(merged_df['winning_team'] == merged_df['team_bet_on'], merged_df['bet_profit'], merged_df['bet_amount'] * -1)
      total_profit_loss = merged_df['bet_result'].sum()

      new_bankroll = round(float(current_bankroll) + total_profit_loss, 2)

      return new_bankroll
      
    def filter_5_min_cooloff(self, username, df):
       try:
          session = self.db_manager.create_session()
          placed_bets =  pd.read_sql_table('placed_bets', con=self.db_manager.get_engine())
       except Exception as e:
        print(e)
        return str(e)
       finally:
         session.close()

       user_df = placed_bets[placed_bets['user_name'] == username]

       user_df['time_placed'] = pd.to_datetime(user_df['time_placed'])

       user_time_df = user_df[(datetime.now()- user_df['time_placed']  < pd.Timedelta(seconds=300))]
       
       user_time_df['teams_bet_on'] = user_time_df['team'].str.split('v.').str[0]
       df = df[~df['team_1'].isin(user_time_df['teams_bet_on'])]

       return df

    def check_payments(self):
      try:
            # List all PaymentIntents from Stripe
            subscriptions = stripe.Subscription.list(status='active')
            cancelled_subscriptions = stripe.Subscription.list(status='canceled')
            trialing_subscriptions = stripe.Subscription.list(status='trialing')
            paid_users = [] # Create a set to store usernames of paid users
            # Iterate through the PaymentIntents and add the usernames of paid users to the set
            for subscription in cancelled_subscriptions.data:

              customer = stripe.Customer.retrieve(subscription.customer)
              email = customer.email
              paid_users.append((email, subscription.status == 'active'))
            for subscription in subscriptions.data:
              # print(subscription)
              customer = stripe.Customer.retrieve(subscription.customer)
              email = customer.email
              paid_users.append((email, subscription.status == 'active'))
            for subscription in trialing_subscriptions.data:
              customer = stripe.Customer.retrieve(subscription.customer)
              email = customer.email
              paid_users.append((email, subscription.status == 'trialing'))

            # Update the 'paid' column in the SQLite database
            for username, is_active in paid_users:
              try:
                session = self.db_manager.create_session()
                session.query(LoginInfo).filter_by(username=username).update({"payed": int(is_active)})
                session.commit()
              except Exception as e:
                print(e)
                return str(e)
              finally:
                session.close()

      except stripe.error.StripeError as e:
            print(f"Stripe Error: {e}")
      return

    def get_user_info(self, username):
      user_dict = None
      try:
        # Create a session
        session = self.db_manager.create_session()

        # Query the user's record by username
        user_info = session.query(LoginInfo).filter_by(username=username).first()
        print(user_info.firstname)
        user_dict = {
          "firstname": user_info.firstname,
          "lastname": user_info.lastname,
          "username": user_info.username,
          "password": user_info.password,
          "phone": user_info.phone,
          "bankroll": user_info.bankroll,
          "payed": user_info.payed,
          "date_signed_up": user_info.date_signed_up
        }
      except Exception as e:
        return str(e)
      finally:
        session.close()
        return user_dict

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
              try:
       
                session = self.db_manager.create_session()
                session.query(LoginInfo).filter_by(username=username).update({"payed": 0})
                session.commit()
              except Exception as e:
                print(e)
                return str(e)
              finally:
                session.close()
                return True, "Subscription canceled successfully."
    
        return False, "No active subscription found for this user."
      except stripe.error.StripeError as e:
        print(e)
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

      result_df['result'] = np.where(result_df['target'] == 1, result_df['highest_bettable_odds'] - 1, -1)

      result_df.sort_values(by = 'snapshot_time', inplace=True)

      result_df['running_sum'] = result_df['result'].cumsum()

      result_df['date'] = pd.to_datetime(result_df['snapshot_time'].dt.date)

      grouped = result_df.groupby('date')['result'].sum()

      new_df = result_df.groupby('date')['result'].sum().reset_index()

      new_df['running_sum'] = new_df['result'].cumsum()

      return jsonify(data=new_df.to_json(orient='records', date_format='iso'))
    
    def make_bet_tracker_dashboard_data_kelley(self, df):
       
       allowed_or_not = pd.DataFrame()
       appended = pd.DataFrame()

       df['my_game_id'] = df['team'] + df['game_id']

       for team in df['my_game_id'].unique():
          try:
            team_df = df[df['my_game_id'] == team]
            team_df_sorted = team_df.sort_values(by='snapshot_time')
            start_time = team_df_sorted['snapshot_time'].iloc[0]
            for index, row in team_df_sorted.iterrows():
              if row['snapshot_time'] - start_time >= pd.Timedelta(minutes=5):
                start_time = row['snapshot_time']
                team_df_sorted.at[index, 'allowed'] = 1
            allowed_or_not = pd.concat([allowed_or_not, team_df_sorted], axis=0)
          except Exception as e:
            print(e)
       
       df = allowed_or_not[allowed_or_not['allowed'] == 1]

       initial_bankroll = 1000

       df['decimal_prob'] = 1/df['average_market_odds']

       df['kelley_perc'] = ((df['highest_bettable_odds'] - 1) * df['decimal_prob'] - (1-df['decimal_prob'])) / (df['highest_bettable_odds']-1) * 0.5

       grouped_df = df.groupby('game_date')
      
       i = 0
       for key, val in grouped_df:
          group = grouped_df.get_group(key)
          if i == 0:
            starting_bankroll=initial_bankroll
          else:
            starting_bankroll = ending_bankroll
          for index, row in group.iterrows():
              group.at[index, 'bet_amount'] = row['kelley_perc'] * starting_bankroll
              group.at[index,'result'] = np.where(row['winning_team'] == row['team'], (group.at[index, 'bet_amount'] * row['highest_bettable_odds'] - group.at[index, 'bet_amount']) , -group.at[index, 'bet_amount'])
          
          ending_bankroll = group['result'].sum() + starting_bankroll

          appended = pd.concat([appended, group], ignore_index=True)

       sum_per_day = appended.groupby('game_date').sum().reset_index()

       sum_per_day['running_sum'] = sum_per_day['result'].cumsum()

       sum_per_day['running_sum'] = sum_per_day['running_sum'] + starting_bankroll

       appended['running_sum'] = appended['result'].cumsum()

       appended['running_sum'] = appended['running_sum'] + starting_bankroll

       return appended, sum_per_day
    
    def make_bet_tracker_dashboard_data_standard(self, df):
       allowed_or_not = pd.DataFrame()
       appended = pd.DataFrame()
       for team in df['team'].unique():
          try:
            team_df = df[df['team'] == team]
            team_df_sorted = team_df.sort_values(by='game_date')
            start_time = team_df_sorted['snapshot_time'].iloc[0]
            for index, row in team_df_sorted.iterrows():
              if row['snapshot_time'] - start_time >= pd.Timedelta(minutes=5):
                start_time = row['snapshot_time']
                team_df_sorted.at[index, 'allowed'] = 1
            allowed_or_not = pd.concat([allowed_or_not, team_df_sorted], axis=0)
          except Exception as e:
            print(e)
       
       df = allowed_or_not[allowed_or_not['allowed'] == 1]

       initial_bankroll = 1000

       unit_size = 100



       grouped_df = df.groupby('game_date')
      
       i = 0
       for key, val in grouped_df:
          group = grouped_df.get_group(key)
          if i == 0:
            starting_bankroll=initial_bankroll
          else:
            starting_bankroll = ending_bankroll
          for index, row in group.iterrows():
              group.at[index, 'bet_amount'] = unit_size
              group.at[index,'result'] = np.where(row['winning_team'] == row['team'], (group.at[index, 'bet_amount'] * row['highest_bettable_odds'] - unit_size) , -1 * unit_size)
          
          ending_bankroll = group['result'].sum() + starting_bankroll

          appended = pd.concat([appended, group], ignore_index=True)

       sum_per_day = appended.groupby('game_date').sum().reset_index()

       sum_per_day['running_sum'] = sum_per_day['result'].cumsum()

       sum_per_day['running_sum'] = sum_per_day['running_sum'] + starting_bankroll

       appended['running_sum'] = appended['result'].cumsum()

       appended['running_sum'] = appended['running_sum'] + starting_bankroll

       return appended, sum_per_day

    def add_winning_teams(self, df):
      scores = self.get_scores()
      merged_df = df.merge(scores, on='game_id', how='left')
      return_df = merged_df[merged_df['winning_team'].notna()]
      return return_df
    
    def get_worst_day(self, df):

      sum_by_date = df.groupby('game_date')['result'].sum().reset_index()

      min_sum_value = sum_by_date['result'].min()

      return min_sum_value
    
    def get_best_day(self, df):

      sum_by_date = df.groupby('game_date')['result'].sum().reset_index()

      max_sum_value = sum_by_date['result'].max()

      return max_sum_value

    def make_daily_game_results(self, df):
      grouped_by_game_id = df.groupby('game_id')['result'].sum().reset_index()
      df = df.merge(grouped_by_game_id, on='game_id', how='left', suffixes=('', '_summed'))

      grouped = df.groupby('game_id').last()

      smushed = grouped.groupby('game_date').agg({
          'team': lambda x: x.tolist(),  
          'result_summed': lambda x: x.tolist()
      })

      smushed['game_info'] = [
    ", ".join([f"{team}: {self.format_dollar(result)}" for team, result in zip(teams, results)])
    for teams, results in zip(smushed['team'], smushed['result_summed'])
]

      return pd.Series(smushed['game_info']).reset_index(drop=True)

    def format_dollar(self, num):
       num = float(num)
       if num < 0:
          return f"-${abs(num):.2f}"
       if num >=0:
          return f"+${num:.2f}"

    def get_bet_tracker_dashboard_data(self, params):
      
      #Could work, could switch to sql, whatever 
      master_model_obs = pd.read_csv('users/master_model_observations.csv')

      master_model_obs = master_model_obs[master_model_obs['average_market_odds'] > 1]

      if params['sport_title'] != 'All':
          master_model_obs = master_model_obs[master_model_obs['sport_title'] == params['sport_title']]
          print(master_model_obs['sport_title'])
      if params['timing'] == 'Pregame only':
         master_model_obs = master_model_obs[master_model_obs['minutes_since_commence'] <= 0]
      if params['timing'] == 'Live only':
         master_model_obs = master_model_obs[master_model_obs['minutes_since_commence'] >= 0]

      master_model_obs = self.add_winning_teams(master_model_obs)

      master_model_obs['game_date'] = pd.to_datetime(master_model_obs['game_date'])
      master_model_obs['snapshot_time'] = pd.to_datetime(master_model_obs['snapshot_time'])

      master_model_obs = master_model_obs.sort_values('snapshot_time')

      if params['bet_size'] == 'Kelley':
         master_model_obs, return_df = self.make_bet_tracker_dashboard_data_kelley(master_model_obs)
      if params['bet_size'] == 'Standard':
          master_model_obs, return_df = self.make_bet_tracker_dashboard_data_standard(master_model_obs)
    
      return_df['hover_info'] = self.make_daily_game_results(master_model_obs)

      return_df['total_pl'] = master_model_obs['result'].sum()

      return_df['worst_day'] = self.get_worst_day(master_model_obs)

      return_df['best_day'] = self.get_best_day(master_model_obs)

      return_df['win_rate'] = (master_model_obs['result'] > 0).sum() / ((master_model_obs['result'] < 0).sum() + (master_model_obs['result'] > 0).sum())

      return_df['amount_of_bets'] = len(master_model_obs)

      return_df['return_on_money'] = return_df['total_pl'] / master_model_obs['bet_amount'].sum()

      return_df['game_date'] = return_df['game_date'].dt.strftime('%b %d')

      return return_df.to_dict(orient='list')       

    def get_filter_dropdown_values(self):

       df = pd.read_csv('users/positive_ev_dash_data.csv')

       df['game_date'] = pd.to_datetime(df['game_date'])

       current_time_gmt = datetime.now(pytz.timezone('GMT'))

       df = df[df['game_date'] >= current_time_gmt]

       df = df.sort_values('game_date')

       df['game_date'] = (df['game_date'] - pd.Timedelta(hours = 6)).dt.strftime('%A, %B %d, %Y')

       df['sportsbooks_used'] = df['sportsbooks_used'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)
       sportsbook_list = list({element for sublist in df['sportsbooks_used'] for element in sublist})

       return jsonify({
          'sport_league_display': ['all'] + sorted(df['sport_league_display'].unique().tolist()),
          'market_display': ['all'] + sorted(df['market_display'].unique().tolist()),
          'game_date': ['all'] + df['game_date'].unique().tolist(),
          'sportsbooks_used': ['all'] + sorted(sportsbook_list),
        })