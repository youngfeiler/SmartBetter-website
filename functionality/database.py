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
import datetime

class database():
    def __init__(self):
        self = self

    def get_all_usernames(self):
      df = pd.read_csv('users/login_info.csv')
      self.users= df['username'].tolist()
    
    def add_user(self, firstname, lastname, username, password, phone, bankroll):
       new_user = User(username)

       new_user.create_user(firstname, lastname, username, password, phone, bankroll)

       self.users = self.get_all_usernames()

    def check_login_credentials(self, username, password):
      df = pd.read_csv('users/login_info.csv')
      user_info = df[df['username'] == username]
      if user_info.empty:
        return False
      else:
        if password == user_info['password'].item():
          return True

    def make_data(self, strategy_name):
        full_df = self.get_data(strategy_name)

        df = full_df[full_df['target'] > -1]
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.date

        
        # Group the DataFrame by date and get the last cumulative result for each day
        grouped = df.groupby('date')['cumulative_result'].last()
        
        datapoints = []
        total_p_l = df['total_p_l'].iloc[0].item()
        total_precision = round(df['total_precision'].iloc[0].item() * 100, 1)
        best_day = df['best_day_prof'].iloc[0].item()
        worst_day = df['worst_day_prof'].iloc[0].item()
        total_bets_placed = df['total_bets_placed'].iloc[0].item()
        return_on_money = df['return_on_money'].iloc[0].item()

        for date, result_sum in grouped.items():
            formatted_date = date.strftime('%Y-%m-%d')

            teams = df[df['date'] == date][['team', 'result']].to_dict(orient='records')
            day_results = df[df['date'] == date][['date', 'daily_result']].tail(1).to_dict(orient='records')

            datapoints.append({'date': formatted_date, 'result_sum': result_sum, 'teams': teams, 'day_results': day_results, 'total_p_l':total_p_l, 'total_precision': total_precision, 'best_day': best_day, 'worst_day': worst_day, 'total_bets_placed': total_bets_placed, 'return_on_money': return_on_money})

        return datapoints
    
    def make_team_dist_data(self, strategy_name):
        df = self.get_data(strategy_name)

        # Calculate the number of rows where the 'result' column is above and below 0
        above_zero_counts = df[df['result'] > 0]['team'].value_counts().reset_index()
        above_zero_counts.columns = ['team', 'above_zero_count']

        below_zero_counts = df[df['result'] < 0]['team'].value_counts().reset_index()
        below_zero_counts.columns = ['team', 'below_zero_count']

        # Merge the above and below zero counts into a single DataFrame
        team_counts = pd.merge(above_zero_counts, below_zero_counts, on='team', how='outer').fillna(0)

        # Calculate the total count for each team (sum of above and below zero counts)
        team_counts['total_count'] = team_counts['above_zero_count'] + team_counts['below_zero_count']

        # Sort the dataset by the total count in descending order
        team_counts = team_counts.sort_values(by='total_count', ascending=False)

        # Convert the data to a format that can be sent to JavaScript (JSON)
        response_data = {
            'teams': team_counts['team'].tolist(),
            'above_zero_counts': team_counts['above_zero_count'].tolist(),
            'below_zero_counts': team_counts['below_zero_count'].tolist()
        }

        return jsonify(response_data)

    def make_book_dist_data(self, strategy_name):
        df = self.get_data(strategy_name)

        # Parse 'sportsbook(s)_used' column as a list
        df['sportsbook(s)_used'] = df['sportsbook(s)_used'].apply(eval)

        # Explode the 'sportsbook(s)_used' column to transform lists into separate rows
        df_exploded = df.explode('sportsbook(s)_used')

        # Group the data by 'sportsbook(s)_used' and calculate the counts and sum of results
        book_counts = df_exploded.groupby('sportsbook(s)_used').agg(
            above_zero_counts=('result', lambda x: (x > 0).sum()),
            below_zero_counts=('result', lambda x: (x < 0).sum()),
            total_result=('result', 'sum')
        ).reset_index()

        # Sort the dataset by the total result in descending order
        book_counts = book_counts.sort_values(by='total_result', ascending=False)

        # Convert the data to a format that can be sent to JavaScript (JSON)
        response_data = {
            'book': book_counts['sportsbook(s)_used'].tolist(),
            'above_zero_counts': book_counts['above_zero_counts'].tolist(),
            'below_zero_counts': book_counts['below_zero_counts'].tolist(),
            'total_result': book_counts['total_result'].tolist()
        }

        return jsonify(response_data)

    def make_active_bet_data(self, strategy_name):
       
       df = self.get_data(strategy_name)
       live_df = df[pd.isna(df['target'])]

       live_df['highest_bettable_odds'] = np.where(live_df['highest_bettable_odds'] >= 2,(live_df['highest_bettable_odds']-1)*100, -100/(live_df['highest_bettable_odds']-1))

       live_df['highest_bettable_odds'] = live_df['highest_bettable_odds'].astype(int)

       live_df = live_df.rename(columns={'sportsbook(s)_used': 'sportsbook'})
       live_df['ev'] = live_df['ev'].round(1)


       selected_columns = live_df[['team', 'opponent', 'ev', 'highest_bettable_odds', 'date', 'sportsbook']]
       selected_columns['sportsbook'] = selected_columns['sportsbook'].str.split(',')
       rows_as_dicts = selected_columns.to_dict(orient='records')

       return jsonify(rows_as_dicts)

    def get_all_user_strategies(self):
      df = pd.read_csv('users/user_strategy_names.csv')
      return df['strategy_name'].tolist()

    def get_data(self, strategy_name):
       return pd.read_csv(f'live_performance_data/{strategy_name}.csv')
    
    def get_user_strategies(self, username):
      this_user = User(username)
      strategies = this_user.get_strategies_associated_with_user()
      return strategies
    
    def delete_user_strategy(self, username, strategy_name):
       # delete the strategy from the user_strategy_names.csv
       this_user = User(username)
       this_user.delete_strategy_to_user(username, strategy_name)
       os.remove(f'models/model_objs/{strategy_name}.pth')
       os.remove(f'models/encoders/{strategy_name}.pkl')
       os.remove(f'models/scalers/{strategy_name}.pkl')
       os.remove(f"models/params/{strategy_name}.pkl")
       pass

    def check_if_strategy_exists_and_handle_duplicate(self, input_name, input_strat_params):
      
      # if the params are equal to eachother, handle, else do nothing
      for strat_filename in os.listdir('models/params'):
        if strat_filename == '.DS_Store':
          pass
        else:
          with open(f'models/params/{strat_filename}', "rb") as file:
            strategy_params_ordered_dict = pickle.load(file)
            strategy_params_dict = dict(strategy_params_ordered_dict)
            if strategy_params_dict.items() == input_strat_params.items():
              self.handle_duplicate_strategy(input_name, strat_filename)
              return True
      return False
    
    def handle_duplicate_strategy(self, input_name, pre_existing_strategy_filename):

      pre_existing_strategy_name = pre_existing_strategy_filename.split('.pkl')[0]

      existing_obj_path = f'models/model_objs/{pre_existing_strategy_name}.pth'
      new_obj_path = f'models/model_objs/{input_name}.pth'

      shutil.copy(existing_obj_path, new_obj_path)

      existing_encoder_path = f'models/encoders/{pre_existing_strategy_name}.pkl'
      new_encoder_path = f'models/encoders/{input_name}.pkl'

      shutil.copy(existing_encoder_path, new_encoder_path)

      existing_scaler_path = f'models/scalers/{pre_existing_strategy_name}.pkl'
      new_scaler_path = f'models/scalers/{input_name}.pkl'

      shutil.copy(existing_scaler_path, new_scaler_path)

      existing_params_path = f'models/params/{pre_existing_strategy_name}.pkl'
      new_params_path = f'models/params/{input_name}.pkl'

      shutil.copy(existing_params_path, new_params_path)

      existing_performance_path = f'live_performance_data/{pre_existing_strategy_name}.csv'

      new_performance_path = f'live_performance_data/{input_name}.csv'

      shutil.copy(existing_performance_path, new_performance_path)

    def update_winning_teams_data(self):

      scores_df = pd.read_csv('mlb_data/scores.csv')

      game_winners = scores_df.set_index('game_id')['winning_team'].to_dict()

      for file in os.listdir('live_performance_data'):
        if file.endswith('.csv'):
          performance_df = pd.read_csv(f'live_performance_data/{file}')

          def fill_na_with_winner(row):
            game_id = row['game_id']
            team = row['team']
            opponent = row['opponent']
            winning_team = game_winners.get(game_id)
            if team == winning_team:
                return 1
            elif opponent == winning_team:
                return 0
            else:
                return row['target']
            
          performance_df['target'] = performance_df.apply(fill_na_with_winner, axis=1)

          performance_df.to_csv(f'live_performance_data/{file}', index=False)

    def update_strategy_performance_files(self):
      
       game_id_to_commence_time = map_commence_time_game_id()
       
       for file in os.listdir('live_performance_data'):
          
          if file.endswith('.csv'):
           try:
            strat_name = file.split('.csv')[0]

            with open(f'models/params/{strat_name}.pkl', 'rb') as f:
              loaded_ordered_params_dict = pickle.load(f)
              loaded_params_dict = dict(loaded_ordered_params_dict)
              bettable_books = [book + '_1_odds' for book in loaded_params_dict['bettable_books']]

            full_df = pd.read_csv(f'live_performance_data/{file}')

            df = full_df[full_df['target'] >= 0]

            live_df = full_df[pd.isna(full_df['target'])]

            count_bets = int(len(df))

            df['result'] = np.where(df['target'] == 1, df['highest_bettable_odds']*100-100, -100).round().astype(int)

            df['date'] = df['game_id'].replace(game_id_to_commence_time)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

            df = df.sort_values(by='date')

            df['daily_result'] = df.groupby(df['date'])['result'].transform('sum')

            df['cumulative_result'] = df['result'].cumsum()

            total_pl =  int(df['result'].sum())

            df['total_p_l'] = total_pl

            df['total_ev_per_bet'] = total_pl / count_bets

            count_wins = len(df[df['result'] > 0])

            df['total_precision'] = float(int(count_wins)/int(count_bets))
            
            best_idx = df['daily_result'].idxmax()
            best_row = df.loc[best_idx]
            df['best_day_prof'] = best_row['daily_result']
            worst_idx = df['daily_result'].idxmin()
            worst_row = df.loc[worst_idx]
            df['worst_day_prof'] = worst_row['daily_result']

            df['total_bets_placed'] = count_bets

            return_on_money = (total_pl/(count_bets*100))*100

            df['return_on_money'] = round(return_on_money, 1)

            df = df.apply(lambda x: x.astype(int) if x.dtypes == 'int64' else x)

            def process_column_header(header):
              book = header.split('_1_odds')[0].title()
              return book
            
            def find_matching_columns(row):
                return [process_column_header(col) for col in bettable_books if row[col] == row['highest_bettable_odds']]

            df['sportsbook(s)_used'] = df.apply(find_matching_columns, axis=1)
            live_df['sportsbook(s)_used'] = live_df.apply(find_matching_columns, axis=1)

            df = pd.concat([df, live_df],axis=0 )

            df.to_csv(f'live_performance_data/{file}', index=False)
           except:
            pass
      
    def check_text_permission(self, user, strategy):
       df = pd.read_csv('users/user_strategy_names.csv')

       user_strat_df = df.loc[(df['username'] == user) & (df['strategy_name'] ==strategy)]


       if not user_strat_df.empty and user_strat_df['text_alerts'].iloc[0]:
        return True
       else:
        return False

    def update_text_permission(self, user, strategy):
       df = pd.read_csv('users/user_strategy_names.csv')

       # Find the row that matches the user and strategy
       row_to_modify = df.loc[(df['username'] == user) & (df['strategy_name'] == strategy)]

       if not row_to_modify.empty:
       # Get the index of the row
          index_to_modify = row_to_modify.index[0]

       # Modify the 'text_alerts' value in the original DataFrame
          df.at[index_to_modify, 'text_alerts'] = not df.at[index_to_modify, 'text_alerts']

       # Save the modified DataFrame to the same CSV file
          df.to_csv('users/user_strategy_names.csv', index=False)

          return True
       
    def get_user_bank_roll(self, user):
        df = pd.read_csv('users/login_info.csv')
        user_df = df[df['username'] == user]
        return user_df['bankroll'].iloc[0]

    def add_to_bankroll(self, user, amount):
         try:
          df = pd.read_csv('users/login_info.csv')

          user_df = df[df['username'] == user]

          new_bankroll = float(user_df['bankroll'].iloc[0]) + float(amount)

          df.loc[df['username'] == user, 'bankroll'] = new_bankroll
    
          df.to_csv('users/login_info.csv', index=False)

          return True
         except:
            return False

    def get_recommended_bet_size(self, user, df):
       df['decimal_highest_bettable_odds'] = df['highest_bettable_odds'].apply(american_to_decimal)
       df['win_prob'] =  (1 / df['average_market_odds']) 
       bankroll = self.get_user_bank_roll(user)
       df['bet_amount'] = (((df['decimal_highest_bettable_odds'] - 1) * df['win_prob'] - (1 - df['win_prob'])) / (df['decimal_highest_bettable_odds']- 1)) * 0.5 * bankroll
                          #((    Decimal Odds                    – 1) * Decimal Winning Percentage – (1 – Winning Percentage)) / (Decimal Odds – 1) * Kelly Multiplier
       df['bet_amount'] = df['bet_amount'].round(2)
       return df
       
    def add_made_bet_to_db(self, jayson):

      df = pd.DataFrame(columns=jayson.keys())
      df = df.append(jayson, ignore_index =True)
      odds = int(df['odds'])
      df['bet_profit'] = np.where(odds > 0, (odds * float(df['bet_amount'])) /100, float(df['bet_amount']) /(-1 * odds/100))
      read_in = pd.read_csv('users/placed_bets.csv')
      put_out = read_in.append(df, ignore_index=True)
      put_out.to_csv('users/placed_bets.csv', index = False)
      return
    
    def get_live_dash_data(self, user_name):
       df = pd.read_csv('users/model_obs.csv')
       result_updater_instance = result_updater()
       result_updater_instance.update_results()
       scores_df = pd.read_csv('mlb_data/scores.csv')
       
       scores_df = scores_df[['game_id', 'winning_team']]
       merged_df = df.merge(scores_df, on='game_id', how='left')

       filtered_df = merged_df[merged_df['winning_team'].isna()]

       filtered_df['sportsbooks_used_string'] = filtered_df['sportsbooks_used'].astype(str)

       df_sorted = filtered_df.sort_values(by='snapshot_time', ascending=False)

       df_sorted = pd.DataFrame(df_sorted)


       columns_to_compare = ['game_id', 'ev', 'team', 'opponent', 'highest_bettable_odds', 'sportsbooks_used_string', 'date']

       df_no_duplicates = df_sorted.drop_duplicates(subset=columns_to_compare)


       df_no_duplicates['highest_bettable_odds'] = df_no_duplicates['highest_bettable_odds'].map(decimal_to_american)

       def convert_to_list(value):
          if isinstance(value, str):
              return [value]
          elif isinstance(value, list):
              return value
          else:
              return []

       df_no_duplicates['sportsbooks_used_list'] = df_no_duplicates['sportsbooks_used'].apply(convert_to_list)

       df_no_duplicates = df_no_duplicates.drop(columns=['sportsbooks_used', 'sportsbooks_used_string', 'winning_team'])

       df_no_duplicates.rename(columns={'sportsbooks_used_list': 'sportsbooks_used'}, inplace=True)
       
       first_20_rows = df_no_duplicates.head(20)

       current_time = datetime.datetime.now() 

       first_20_rows['current_time'] = current_time #+ pd.Timedelta(hours=6)

       first_20_rows['snapshot_time'].apply(pd.to_datetime)

       first_20_rows['current_time'] = pd.to_datetime(first_20_rows['current_time'])

       first_20_rows['snapshot_time'] = pd.to_datetime(first_20_rows['snapshot_time'])

       first_20_rows['time_difference_seconds'] = (first_20_rows['current_time'] - first_20_rows['snapshot_time']).dt.total_seconds()
       
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
       
       first_20_rows = first_20_rows.apply(minutes_seconds, axis=1)

       first_20_rows = self.get_recommended_bet_size(user_name, first_20_rows)
       return first_20_rows

    def get_unsettled_bet_data(self, user):
      df = pd.read_csv('users/placed_bets.csv')
      scores_df = pd.read_csv('mlb_data/scores.csv')
      df = df[df['user_name'] == user]

      df['bet_profit'] = np.where(df['odds'] > 0, (df['odds'] * df['bet_amount']) /100, df['bet_amount'] /(-1 * df['odds']/100))

      result_updater_instance = result_updater()
      result_updater_instance.update_results()

      scores_df = scores_df[['game_id', 'winning_team']]

      merged_df = df.merge(scores_df, on='game_id', how='left')

      filtered_df = merged_df[merged_df['winning_team'].isna()]
      grouped_df = filtered_df.groupby(['game_id', 'team'])

      filtered_df['amount_of_bets'] = grouped_df['game_id'].transform('size')
      filtered_df['highest_odds'] = grouped_df['odds'].transform('max')
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

            group.loc[group.index[0], 'team'] = row1['team'].split('v. ')[0]
            group.loc[group.index[1], 'team'] = row2['team'].split('v. ')[0]

        elif len(group) == 1:
            row = group.iloc[0].copy()
            row['ev'] = ''
            row['team'] = group.iloc[0]['team'].split('v. ')[1]
            row['odds'] = ''
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
            group.loc[group.index[0], 'team'] = group.iloc[0]['team'].split('v. ')[0]
        return group
      

      game_id_df_grouped = game_id_df_grouped.apply(calculate_if_win).reset_index(drop=True)

      game_id_df_grouped['if_win'] = round(game_id_df_grouped['if_win'],1)
      game_id_df_grouped['average_odds'] = game_id_df_grouped['average_odds'].apply(lambda x: round(x, 0) if isinstance(x, (int, float)) else x)



      return_df = game_id_df_grouped[['game_id', 'team', 'user_name', 'average_odds', 'highest_odds', 'if_win']]

      return return_df
    
    def calculate_user_bankroll(self, username):
      #this will also update the user's p/l for each book
      placed_bets = pd.read_csv('users/placed_bets.csv')
      login_info = pd.read_csv('users/login_info.csv')

      current_bankroll = self.get_user_bank_roll(username)

      placed_bets = placed_bets[placed_bets['user_name'] == username]

      scores_df = pd.read_csv('mlb_data/scores.csv')
      result_updater_instance = result_updater()
      result_updater_instance.update_results()

      scores_df = scores_df[['game_id', 'winning_team']]
      merged_df = placed_bets.merge(scores_df, on='game_id', how='left')
      merged_df = merged_df[merged_df['winning_team'].notna()]
      merged_df['team_bet_on'] = [cell.split('v. ')[0] for cell in merged_df['team']]




      merged_df['bet_profit'] = merged_df['bet_profit'].astype(float)

      # merged_df['bet_result'] = np.where(merged_df['winning_team'] == merged_df['team_bet_on'], merged_df['bet_profit'], merged_df['bet_profit'] * -1)
      merged_df['bet_result'] = np.where(merged_df['winning_team'] == merged_df['team_bet_on'], merged_df['bet_profit'], merged_df['bet_amount'] * -1)

      test_df_user = merged_df[merged_df['user_name'] == 'youngfeiler']
      test_df = test_df_user.groupby('game_date')['bet_result'].sum()
      print(test_df)


      #call calculate_p_l_by_book
      profit_by_book = pd.read_csv('users/profit_by_book.csv')
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

        ls = row['sportsbook'].split(', ')
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
      profit_by_book = profit_by_book.append(append_df, ignore_index=True)
      profit_by_book.to_csv('users/profit_by_book.csv', index=False)
      # calculate total profit/loss of all bets in placed_bets 
      total_profit_loss = merged_df['bet_result'].sum()
      # add total profit/loss to current bankroll
      new_bankroll = round(current_bankroll + total_profit_loss, 2)
      # update users/login_info.csv with new bankroll
      login_info[login_info['username'] == username]['bankroll'].iloc[0] = new_bankroll
      login_info.to_csv('users/login_info.csv', index=False)

      
      return new_bankroll
      
    def get_user_performance_data(self, username):
      scores_df = pd.read_csv('mlb_data/scores.csv')
      placed_bets = pd.read_csv('users/placed_bets.csv')
      placed_bets = placed_bets[placed_bets['user_name'] == username]
      scores_df = scores_df[['game_id', 'winning_team']]
      merged_df = placed_bets.merge(scores_df, on='game_id', how='left')
      merged_df = merged_df[merged_df['winning_team'].notna()]
      merged_df['team_bet_on'] = [cell.split('v. ')[0] for cell in merged_df['team']]
      merged_df['bet_profit'] = merged_df['bet_profit'].astype(float)
      merged_df['bet_result'] = np.where(merged_df['winning_team'] == merged_df['team_bet_on'], merged_df['bet_profit'], merged_df['bet_amount'] * -1)

      merged_df['game_date'] = pd.to_datetime(merged_df['game_date'])

      grouped = merged_df.groupby('game_date')['bet_result'].sum().reset_index()

      # Calculate the running cumulative sum
      grouped['running_profit'] = grouped['bet_result'].cumsum() 

      datapoints = []

      wins = merged_df[merged_df['bet_result'] > 0]['bet_result'].count()
      losses = merged_df[merged_df['bet_result'] < 0]['bet_result'].count()

      total_p_l = round(merged_df['bet_result'].sum(),1)

      total_precision = round(wins/losses, 1)

      best_day_profit = round(grouped['bet_result'].max(),1)

      worst_day_loss = round(grouped['bet_result'].min(),1)

      total_bets_placed = merged_df['bet_result'].count()

      return_on_money = round((total_p_l / merged_df['bet_amount'].sum())*100,2)

      for index, row in grouped.iterrows():
        formatted_date = row['game_date'].strftime('%Y-%m-%d')

        datapoints.append({
            'date': formatted_date,
            'daily_result': float(row['bet_result']),
            'running_p_l':float(row['running_profit']),
            'total_p_l': float(total_p_l),
            'total_precision': float(total_precision),
            'best_day': float(best_day_profit),
            'worst_day': float(worst_day_loss),
            'total_bets_placed': int(total_bets_placed),
            'return_on_money': float(return_on_money)
        })

      return jsonify(datapoints)











    

    
  






















    

    
       



