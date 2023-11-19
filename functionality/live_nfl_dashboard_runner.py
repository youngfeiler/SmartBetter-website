import pickle
import torch
import pandas as pd
import numpy as np
import requests
import datetime
from .util import *
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import os

class live_nfl_dashboard_runner():
    def __init__(self):
        self.model_storage = {}
        self.store_model_info()
        self.display_df = pd.DataFrame()
        self.SHEET_HEADER =['game_id', 
                            'commence_time', 'time_pulled', 'team_1', 'team_2', 'barstool_1_odds', 'barstool_1_time', 'barstool_2_odds', 'barstool_2_time', 'betclic_1_odds', 'betclic_1_odds', 'betclic_1_time', 'betclic_1_time', 'betclic_2_odds', 'betclic_2_odds', 'betclic_2_time', 'betclic_2_time', 'betfair_1_odds', 'betfair_1_time', 'betfair_2_odds', 'betfair_2_time', 'betfred_1_odds', 'betfred_1_time', 'betfred_2_odds', 'betfred_2_time', 'betmgm_1_odds', 'betmgm_1_time', 'betmgm_2_odds', 'betmgm_2_time', 'betonlineag_1_odds', 'betonlineag_1_time', 'betonlineag_2_odds', 'betonlineag_2_time', 'betrivers_1_odds', 'betrivers_1_time', 'betrivers_2_odds', 'betrivers_2_time', 'betsson_1_odds', 'betsson_1_time', 'betsson_2_odds', 'betsson_2_time', 'betus_1_odds', 'betus_1_time', 'betus_2_odds', 'betus_2_time', 'betvictor_1_odds', 'betvictor_1_time', 'betvictor_2_odds', 'betvictor_2_time', 'betway_1_odds', 'betway_1_time', 'betway_2_odds', 'betway_2_time', 'bovada_1_odds', 'bovada_1_time', 'bovada_2_odds', 'bovada_2_time', 'casumo_1_odds', 'casumo_1_time', 'casumo_2_odds', 'casumo_2_time', 'circasports_1_odds', 'circasports_1_time', 'circasports_2_odds', 'circasports_2_time', 'coral_1_odds', 'coral_1_time', 'coral_2_odds', 'coral_2_time', 'draftkings_1_odds', 'draftkings_1_time', 'draftkings_2_odds', 'draftkings_2_time', 'fanduel_1_odds', 'fanduel_1_time', 'fanduel_2_odds', 'fanduel_2_time', 'foxbet_1_odds', 'foxbet_1_time', 'foxbet_2_odds', 'foxbet_2_time', 'gtbets_1_odds', 'gtbets_1_time', 'gtbets_2_odds', 'gtbets_2_time', 'intertops_1_odds', 'intertops_1_time', 'intertops_2_odds', 'intertops_2_time', 'ladbrokes_1_odds', 'ladbrokes_1_time', 'ladbrokes_2_odds', 'ladbrokes_2_time', 'livescorebet_1_odds', 'livescorebet_1_time', 'livescorebet_2_odds', 'livescorebet_2_time', 'lowvig_1_odds', 'lowvig_1_odds', 'lowvig_1_time', 'lowvig_1_time', 'lowvig_2_odds', 'lowvig_2_odds', 'lowvig_2_time', 'lowvig_2_time', 'marathonbet_1_odds', 'marathonbet_1_time', 'marathonbet_2_odds', 'marathonbet_2_time', 'matchbook_1_odds', 'matchbook_1_time', 'matchbook_2_odds', 'matchbook_2_time', 'mrgreen_1_odds', 'mrgreen_1_odds', 'mrgreen_1_time', 'mrgreen_1_time', 'mrgreen_2_odds', 'mrgreen_2_odds', 'mrgreen_2_time', 'mrgreen_2_time', 'mybookieag_1_odds', 'mybookieag_1_time', 'mybookieag_2_odds', 'mybookieag_2_time', 'nordicbet_1_odds', 'nordicbet_1_time', 'nordicbet_2_odds', 'nordicbet_2_time', 'onexbet_1_odds', 'onexbet_1_time', 'onexbet_2_odds', 'onexbet_2_time', 'paddypower_1_odds', 'paddypower_1_time', 'paddypower_2_odds', 'paddypower_2_time', 'pinnacle_1_odds', 'pinnacle_1_odds', 'pinnacle_1_time', 'pinnacle_1_time', 'pinnacle_2_odds', 'pinnacle_2_odds', 'pinnacle_2_time', 'pinnacle_2_time', 'pointsbetus_1_odds', 'pointsbetus_1_time', 'pointsbetus_2_odds', 'pointsbetus_2_time', 'sport888_1_odds', 'sport888_1_time', 'sport888_2_odds', 'sport888_2_time', 'sugarhouse_1_odds', 'sugarhouse_1_time', 'sugarhouse_2_odds', 'sugarhouse_2_time', 'superbook_1_odds', 'superbook_1_time', 'superbook_2_odds', 'superbook_2_time', 'twinspires_1_odds', 'twinspires_1_time', 'twinspires_2_odds', 'twinspires_2_time', 'unibet_eu_1_odds', 'unibet_eu_1_time', 'unibet_eu_2_odds', 'unibet_eu_2_time', 'unibet_uk_1_odds', 'unibet_uk_1_time', 'unibet_uk_2_odds', 'unibet_uk_2_time', 'unibet_us_1_odds', 'unibet_us_1_time', 'unibet_us_2_odds', 'unibet_us_2_time', 'virginbet_1_odds', 'virginbet_1_time', 'virginbet_2_odds', 'virginbet_2_time', 'williamhill_us_1_odds', 'williamhill_us_1_time', 'williamhill_us_2_odds', 'williamhill_us_2_time', 'wynnbet_1_odds', 'wynnbet_1_odds', 'wynnbet_1_time', 'wynnbet_1_time', 'wynnbet_2_odds', 'wynnbet_2_odds', 'wynnbet_2_time', 'wynnbet_2_time']
        
    def store_model_info(self):
          with open(f'models/encoders/nfl_model_1.pkl', 'rb') as f:
            loaded_encoder = pickle.load(f)
          with open(f'models/scalers/nfl_model_1.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)
          with open(f'models/params/nfl_model_1.pkl', 'rb') as f:
            loaded_ordered_params_dict = pickle.load(f)
            loaded_params_dict = dict(loaded_ordered_params_dict)
          loaded_model = torch.load(f'models/model_objs/nfl_model_1.pth')

          this_model_dict = {
            'model': loaded_model,
            'encoder': loaded_encoder,
            'scaler': loaded_scaler,
            'params': loaded_params_dict,
            'pred_thresh': loaded_params_dict['pred_thresh']
            }
          try:
            this_model_dict['params']['bettable_books'].remove('pinnacle')
            this_model_dict['params']['bettable_books'].remove('unibet_us')  
            this_model_dict['params']['bettable_books'].remove('mybookieag')
          except:
             pass
          self.model_storage['SmartBetterNFLModel'] = this_model_dict

    def make_snapshot(self, df):

      # snapshot_df = pd.DataFrame(columns=self.SHEET_HEADER)
      snapshot_df = pd.DataFrame()

      current_time_utc = datetime.utcnow()

      date = current_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

      my_dict = {value: '' for value in self.SHEET_HEADER}

      for game in df:
          # Information about the game
          my_dict['game_id'] = game['id']
          my_dict['commence_time'] = format_time(game['commence_time'])
          my_dict['time_pulled'] = format_time(date)

          # Compiles each bookmakers lines into a dictionary and then appends that row to a df
          for bookie in game['bookmakers']:
              # Get team name
              my_dict['team_1'] = bookie['markets'][0]['outcomes'][0]['name']
              my_dict['team_2'] = bookie['markets'][0]['outcomes'][1]['name']

              # Find the appropriate column
              if f'{bookie["key"]}_1_odds' in my_dict and f'{bookie["key"]}_2_odds' in my_dict:

                  my_dict[bookie['key'] + "_1_odds"] = bookie['markets'][0]['outcomes'][0]['price']
                  my_dict[bookie['key'] + "_1_time"] = format_time(bookie['last_update'])

                  my_dict[bookie['key'] + "_2_odds"] = bookie['markets'][0]['outcomes'][1]['price']
                  my_dict[bookie['key'] + "_2_time"] = format_time(bookie['last_update'])

          snapshot_df = snapshot_df.append(my_dict, ignore_index=True)

          my_dict = {value: '' for value in self.SHEET_HEADER}

      return snapshot_df
  
    def get_nfl_odds(self):

      API_KEY = os.environ.get("THE_ODDS_API_KEY")
      SPORT = 'americanfootball_nfl'
      REGIONS = 'us,eu,uk'
      MARKETS = 'h2h' 
      ODDS_FORMAT = 'decimal'  # decimal | american
      DATE_FORMAT = 'iso'

      odds_response = requests.get(
          f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}',
          params={
              'api_key': API_KEY,
              'regions': REGIONS,
              'markets': MARKETS,
              'oddsFormat': ODDS_FORMAT,
              'dateFormat': DATE_FORMAT,
          }
      )

      if odds_response.status_code != 200:
          print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
      else:
        odds_json = odds_response.json()

        # Make a dataframe from this pull
        df = pd.DataFrame.from_dict(odds_json)

        # Process this data
        snap = self.make_snapshot(odds_json)

        return snap

    def convert_times_to_mst(self, df):
      # Actually converts it to MSt when we're in daylight savings time, but as long as we're not in GMT we're chilling
      time_columns = [col for col in df.columns if 'time' in col]
      
      df[time_columns] = df[time_columns].apply(lambda x: pd.to_datetime(x))
      df[time_columns] = df[time_columns]- pd.Timedelta(hours=7)

      return df 

    def add_extra_info(self, df):

      extra_info = pd.read_csv('nfl_data/nfl_extra_info.csv')

      df["commence_date"] = pd.to_datetime(df["commence_time"]).dt.date.astype(str)
      df['hour_of_start'] = pd.to_datetime(df["commence_time"]).dt.hour.astype(str)
      df["my_game_id"] =df['team_1'] + df['team_2'] + df["commence_date"]

      extra_info['commence_date'] = pd.to_datetime(extra_info['date']).dt.date.astype(str)

      extra_info['my_game_id'] = extra_info['team_1'] + extra_info['team_2'] + extra_info["commence_date"]

      merged_df = pd.merge(df, extra_info, on='my_game_id', how='outer', suffixes=('', '_df2'))

      merged_df = merged_df.dropna(subset=['team_1'])

      merged_df = merged_df.drop(columns=['commence_date', 'date', 'time', 'time_am', 'real_time', 'team_1_df2', 'team_2_df2', 'commence_date_df2'])

      merged_df = merged_df.replace('None', np.nan)

      time_columns = [col for col in merged_df.columns if 'time' in col]

      time_columns.remove('commence_time')

      for col in time_columns:
          merged_df[col] = pd.to_datetime(merged_df[col], errors='coerce')

      values = merged_df[time_columns].to_numpy()

      # Use np.nanmax along the specified axis (axis=1) to find the maximum time value while ignoring NaN
      max_times = np.nanmax(values, axis=1)

      merged_df['snapshot_time'] = max_times

      # Convert the time columns to datetime objects
      merged_df['commence_time'] = pd.to_datetime(merged_df['commence_time'])
      merged_df['snapshot_time'] = pd.to_datetime(merged_df['snapshot_time'])

      # Calculate the time difference in minutes and sum them up
      merged_df['minutes_since_commence'] = (merged_df['snapshot_time'] - merged_df['commence_time']).dt.total_seconds() / 60

      # merged_df.to_csv('live_merged_df.csv', index=False)

      return merged_df
    
    def replace_missing_vals(self, df):
      odds_columns = [col for col in df.columns if 'odds' in col]
      time_columns = [col for col in df.columns if 'time' in col]

      for col in odds_columns:
          df[col] = df[col].replace(np.nan, 0)
          df[col] = df[col].replace('', 0)
          df[col] = df[col].astype('float64')

      for col in time_columns:
          df[col] = df[col].replace(np.nan, '1/1/1970 00:00:00')
          df[col] = df[col].replace('', '1/1/1970 00:00:00')

          df[col] = pd.to_datetime(df[col])
      return df
    
    def stack_df(self, df):

      # Select the first subset:
      cols_with_one = [col for col in df.columns if '_1' in col]
      cols_with_two = [col for col in df.columns if '_2' in col]
      extra_cols = ['game_id', 'commence_time', 'time_pulled', 'my_game_id', 'hour_of_start', 'week', 'day_of_week', 'winning_team', 'home_away_neutral', 'home_team', 'away_team',  'home_team_division', 'away_team_division', 'team_1_division', 'team_2_division', 'home_team_conference', 'away_team_conference', 'day_night', 'snapshot_time', 'minutes_since_commence']

      for each in extra_cols:
          cols_with_one.append(each)

          
          cols_with_two.append(each)

      df1 = df[cols_with_one]
      df2 = df[cols_with_two]

      # # Get list of column names from df1
      df2.columns = df1.columns.tolist()

      df_stacked = pd.concat([df1, df2], axis=0, ignore_index=True)

      # Reset the index of the new DataFrame
      df_stacked = df_stacked.reset_index(drop=True)

      # If team_1 is equal to the winning team, make target 1, otherwise, 0
      df_stacked['target'] = np.where(df_stacked['team_1'] == df_stacked['winning_team'], 1, 0)

      # Finds the team that is not the team_1 and assign the opponent column
      df_stacked['opponent'] = np.where(df_stacked['team_1'] == df_stacked['home_team'], df_stacked['away_team'], df_stacked['home_team'])

      # Makes the first teams division  
      df_stacked['this_team_division'] = np.where(df_stacked['team_1'] == df_stacked['home_team'], df_stacked['home_team_division'], df_stacked['away_team_division'])
  
      # Makes the opponent team division
      df_stacked['opponent_team_division'] = np.where(df_stacked['team_1'] == df_stacked['home_team'], df_stacked['away_team_division'], df_stacked['home_team_division'])

      # Makes the first teams conference
      df_stacked['this_team_conference'] = np.where(df_stacked['team_1'] == df_stacked['home_team'], df_stacked['home_team_conference'], df_stacked['away_team_conference'])

      # Makes the opponent teams conference
      df_stacked['opponent_team_conference'] = np.where(df_stacked['team_1'] == df_stacked['home_team'], df_stacked['away_team_conference'], df_stacked['home_team_conference'])

      df_stacked['home_away'] = np.where(df_stacked['team_1'] == df_stacked['home_team'], 1, 0)

      # df_stacked['snapshot_time'] = df_stacked['snapshot_time_taken'].dt.time

      cols_to_drop=['time_pulled', 'home_team', 'away_team', 'winning_team']

      result = df_stacked.drop(columns=cols_to_drop)

      return result

    def make_some_features(self, df):
       
       def make_highest_bettable_odds(df):
        subset_columns = [col for col in df.columns if any(item in col for item in self.model_storage['SmartBetterNFLModel']['params']['bettable_books'])]

        time_cols = [col for col in subset_columns if '_1_time' in col]
        odds_cols = [col for col in subset_columns if '_1_odds' in col]

        # Convert 'snapshot_time' to datetime
        df['snapshot_time'] = pd.to_datetime(df['snapshot_time'])

        # Extract date and time parts from 'snapshot_time'
        snapshot_date = df['snapshot_time'].dt.date
        snapshot_time = df['snapshot_time'].dt.time

        # Convert time columns to datetime format
        time_df = df[time_cols].apply(pd.to_datetime).apply(lambda x: x.dt.time)

        max_time_per_row = time_df.max(axis=1)

        # Add the result as a new column to the original DataFrame
        time_df['max_time'] = max_time_per_row

        # Create a timedelta DataFrame by combining date from 'snapshot_time' and time from 'time_df'
        time_diff_df = snapshot_date.to_frame().join(time_df).apply(lambda row: pd.Timestamp.combine(row[0], row['max_time']), axis=1) - df['snapshot_time']
        # Calculate absolute values of time differences
        time_diff_df = time_diff_df.abs()

        # Create a mask based on the threshold
        threshold = self.model_storage['SmartBetterNFLModel']['params']['update_time_threshold']

        mask = time_diff_df <= threshold

        # Apply the mask to odds_df and replace False values with 0
        odds_df_masked = df[odds_cols].where(mask, 0)

        # Calculate the maximum odds for each row
        df['highest_bettable_odds'] = odds_df_masked[odds_cols].max(axis=1)

        return df
       
       def make_average_market_odds_old(df):
        # calculates the average market odds for all of the odds we have (including old odds)
        odds_columns = [col for col in df.columns if col.endswith('_odds')]
        odds_df = df[odds_columns]
        df_array = odds_df.values

        # Create mask for values greater than 0.5 (this masks out missing values )
        mask = df_array > 0.5

        # Apply mask and calculate row-wise average
        row_avg = np.nanmean(np.where(mask, df_array, np.nan), axis=1)

        df['average_market_odds_old'] = row_avg

        return df

       def make_average_market_odds_recent(df):
          time_cols = [col for col in df.columns if '_1_time' in col]
          odds_cols = [col for col in df.columns if '_1_odds' in col]

          # Convert 'snapshot_time' to datetime
          df['snapshot_time'] = pd.to_datetime(df['snapshot_time'])

          # Extract date and time parts from 'snapshot_time'
          snapshot_date = df['snapshot_time'].dt.date
          snapshot_time = df['snapshot_time'].dt.time

          # Convert time columns to datetime format
          time_df = df[time_cols].apply(pd.to_datetime).apply(lambda x: x.dt.time)

          max_time_per_row = time_df.max(axis=1)

          # Add the result as a new column to the original DataFrame
          time_df['max_time'] = max_time_per_row

          # Create a timedelta DataFrame by combining date from 'snapshot_time' and time from 'time_df'
          time_diff_df = snapshot_date.to_frame().join(time_df).apply(lambda row: pd.Timestamp.combine(row[0], row['max_time']), axis=1) - df['snapshot_time']
          # Calculate absolute values of time differences
          time_diff_df = time_diff_df.abs()

          # Create a mask based on the threshold
          threshold = self.model_storage['SmartBetterNFLModel']['params']['update_time_threshold']

          mask = time_diff_df <= threshold

          # Apply the mask to odds_df and replace False values with NaN
          odds_df_masked = df[odds_cols].where(mask, 0)

          # Apply a mask to keep only values greater than 0
          odds_df_masked = odds_df_masked[odds_df_masked > 0]

          # Calculate the mean odds for each row (ignoring NaN values)
          df['average_market_odds'] = odds_df_masked.mean(axis=1, skipna=True)

          return df

       df = make_average_market_odds_old(df)

       df = make_highest_bettable_odds(df)

       df = make_average_market_odds_recent(df)

       df['average_market_odds'].fillna(0, inplace=True)

       return df

    def filter_by_params(self, df):

       def filter_by_minutes_since_commence(df):
          df = df[df['minutes_since_commence'] >= self.model_storage['SmartBetterNFLModel']['params']['min_minutes_since_commence']]
          df = df[df['minutes_since_commence'] <= self.model_storage['SmartBetterNFLModel']['params']['max_minutes_since_commence']]

          return df
       
       def filter_by_average_market_odds(df):
        df = df[df['average_market_odds_old'] >= self.model_storage['SmartBetterNFLModel']['params']['min_avg_odds']]
        df = df[df['average_market_odds_old'] <= self.model_storage['SmartBetterNFLModel']['params']['max_avg_odds']]
        return df
       
       #TODO: MIN EV
       def filter_by_ev_thresh(df):        
        odds_columns = [x for x in df.columns if x.endswith('_odds')]

        df['ev'] = ((1/df['average_market_odds_old'])*(100*df['highest_bettable_odds']-100)) - ((1-(1/df['average_market_odds_old'])) * 100)

        print(self.model_storage['SmartBetterNFLModel']['params']['min_ev'])

        df = df[df['ev'] >= self.model_storage['SmartBetterNFLModel']['params']['min_ev']]

        # df = df[df['ev'] >= -100]
        
        df = df[df['ev'] <= self.model_storage['SmartBetterNFLModel']['params']['max_ev']]

        df['ev'] = df['ev'].round(1)

        return df
       
       def filter_by_best_odds(df):
          df = df[df['highest_bettable_odds'] >= self.model_storage['SmartBetterNFLModel']['params']['min_avg_odds']]
          df = df[df['highest_bettable_odds'] <= self.model_storage['SmartBetterNFLModel']['params']['max_avg_odds']]

          return df

       df = filter_by_minutes_since_commence(df)

       df = filter_by_average_market_odds(df)

       df = filter_by_ev_thresh(df)

       df = filter_by_best_odds(df)

       test_series = df['team_1_division'].copy()

       df.drop(columns = ['team_1_division'], inplace=True)

       df['team_1_division'] = test_series.iloc[:, 0]

       return df

    def preprocess(self, df):
      df = self.convert_times_to_mst(df)

      self.market_odds = self.add_extra_info(df)

      self.stacked_df_missing_vals = self.replace_missing_vals(self.market_odds)

      self.stacked_df_plain = self.stack_df(self.stacked_df_missing_vals)

      self.stacked_df_features_added = self.make_some_features(self.stacked_df_plain)

      self.filtered_df = self.filter_by_params(self.stacked_df_features_added)

      self.display_df = self.filtered_df.copy()

      return 
    
    def format_for_nn(self):
       def drop_unnecesary_columns(df):
        df = df.drop(columns=['game_id', 'my_game_id', 'ev', 'commence_time'])
        time_columns = [col for col in df.columns if 'time' in col]

        return_df = df.drop(columns=time_columns)

        return return_df

       def standardize_numerical_values(df):
        self.categorical_columns = ['team_1', 'team_1_division', 'team_1_conference', 'hour_of_start', 'week', 'day_of_week', 'home_away_neutral', 'home_team_division', 'away_team_division', 'team_2_division', 'home_team_conference', 'away_team_conference', 'day_night', 'opponent', 'this_team_division', 'opponent_team_division', 'this_team_conference', 'opponent_team_conference', 'home_away']

        self.numerical_columns = [col for col in df.columns if col not in self.categorical_columns and 'time' not in col and 'target' not in col]

        # Select the subset 
        df_numerical = df[self.numerical_columns]
        df = df.drop(columns='target')

        # Create an instance of StandardScaler and fit it on the training data
        scaler = self.model_storage['SmartBetterNFLModel']['scaler']

        scaled_df = scaler.transform(df[self.numerical_columns])
        
        return scaled_df
      
       def encode_categorical_variables(df):

        encoded = np.empty((len(df), 0))

        encoded_column_names = []  

        encoder_obj = self.model_storage['SmartBetterNFLModel']['encoder']

        for col in self.categorical_columns:

            col_encoder = encoder_obj[col]

            col_data = df[[col]]

            encoded_columns = col_encoder.transform(col_data)

            # Concatenate encoded columns along axis 1 (columns) within each dataset
            encoded = np.hstack((encoded, encoded_columns))

        # Generate column names based on the encoding
        for i in range(encoded.shape[1]):
            col_name = f"encoded_{i}"
            encoded_column_names.append(col_name)

        return encoded
       
       self.filtered_df = drop_unnecesary_columns(self.filtered_df)

       self.scaled_arr = standardize_numerical_values(self.filtered_df)

       self.filtered_df['week'] = self.filtered_df['week'].astype(str)

       self.coded_arr = encode_categorical_variables(self.filtered_df)

       self.final_data_for_model = np.hstack((self.scaled_arr, self.coded_arr))

       self.final_data_for_model = self.final_data_for_model.astype(np.float32)

       return

    def make_live_dash_data(self):
      def find_matching_columns(row):
          def process_column_header(header):
            book = header.split('_1_odds')[0].title()
            return book
          bettable_books = ['barstool', 'betfred', 'betmgm', 'betonlineag', 'betrivers', 'betus', 'circasports', 'draftkings', 'fanduel', 'foxbet','mybookieag', 'pinnacle', 'pointsbetus', 'unibet_us', 'williamhill_us', 'wynnbet']
          return [process_column_header(col) for col in bettable_books if row[col+'_1_odds'] == row['highest_bettable_odds']]
      

      print('nfl running')
      market_odds_df = self.get_nfl_odds()

      # Makes self.filtered_df
      self.preprocess(market_odds_df)

      if not self.filtered_df.empty:
        for strategy_name, strategy_dict in self.model_storage.items():
          self.format_for_nn()
          input_tensor = torch.tensor(self.final_data_for_model, dtype=torch.float32)
          strategy_dict['model'].eval()
          predictions = strategy_dict['model'](input_tensor)

          predictions_array = predictions.detach().numpy()

          # mask = predictions_array > strategy_dict['pred_thresh']
          mask = predictions_array > -10000

          filtered_df = self.display_df[mask]

          if not filtered_df.empty:
            filtered_df['sportsbooks_used'] = filtered_df.apply(find_matching_columns, axis=1)

            filtered_df.to_csv('users/model_obs_nfl.csv', mode = 'a', header=False, index = False)

            print(len(filtered_df))

          elif filtered_df.empty:
             pass
          
      return
    

    

       
