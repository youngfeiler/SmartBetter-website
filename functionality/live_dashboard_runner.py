import requests 
import numpy 
import pandas as pd
from .live_data_collector import data_collector
from .util import get_odds, preprocess, make_stacked_df
import pickle
import torch
import pytz




#for each of the 3 strategies we will host, take the user input from the site about which books they can bet 

# Get the market odds 

# do all the manipulation (have an input for bettable books so that the user can select. Each session should display its own model predictions)

# make sure we only contain reallllly recent odds 

# run that df through the models 

# return the rows that it likes 

# repeat after each 1s

class live_dashboard_runner():
    def __init__(self):
        self = self
        self.model_storage = {}
        # self.database_instance = database() 
        self.store_model_info()
        

    def store_model_info(self):
          loaded_model = torch.load(f'models/model_objs/SmartBetterModel.pth')
          loaded_model.eval()
          with open(f'models/encoders/SmartBetterModel.pkl', 'rb') as f:
            loaded_encoder = pickle.load(f)
          with open(f'models/scalers/SmartBetterModel.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)
          with open(f'models/params/SmartBetterModel.pkl', 'rb') as f:
            loaded_ordered_params_dict = pickle.load(f)
            loaded_params_dict = dict(loaded_ordered_params_dict)
            
          loaded_data_collector = data_collector(
            encoders=loaded_encoder,
            scaler = loaded_scaler,
            min_minutes_since_commence=loaded_params_dict['min_minutes_since_commence'],
            max_minutes_since_commence=loaded_params_dict['max_minutes_since_commence'],
            min_avg_odds=loaded_params_dict['min_avg_odds'],
            max_avg_odds=loaded_params_dict['max_avg_odds'],
            min_ev=loaded_params_dict['min_ev'],
            bettable_books=loaded_params_dict['bettable_books']
            )
          
          this_model_dict = {
            'model': loaded_model,
            'encoder': loaded_encoder,
            'scaler': loaded_scaler,
            'params': loaded_params_dict,
            'data_collector': loaded_data_collector,
            'pred_thresh': loaded_params_dict['pred_thresh']
            }
          
          self.model_storage['SmartBetterModel'] = this_model_dict
    
    def make_live_dash_data(self):
        # somewhere in here, need to filter the highest bettable odds as only those that have been updated within the last 10 seconds 

        market_odds_df = get_odds()
        combined_market_extra_df = preprocess(market_odds_df)
        self.market_odds = combined_market_extra_df
        self.stacked_df = make_stacked_df(combined_market_extra_df)

        for strategy_name, strategy_dict in self.model_storage.items():

            this_model_raw_data_point = strategy_dict['data_collector'].format(self.stacked_df)

            if this_model_raw_data_point is not False:
              
              input_tensor = torch.tensor(this_model_raw_data_point.values, dtype=torch.float32)

              predictions = strategy_dict['model'](input_tensor)

              ind_list = []
              for idx, pred in enumerate(predictions):
                pred_float = pred.detach().numpy()[0]
                
                #if pred_float >= strategy_dict['pred_thresh']:
                if pred_float >= -100:
                  ind_list.append(idx)

              if len(ind_list) > 0:
                bet_list = self.get_team_odds_book(this_model_raw_data_point, ind_list, strategy_dict)

                return self.handle_bets(bet_list, self.stacked_df, strategy_name, strategy_dict['params']['bettable_books'])
              


    def format_sportsbook_names_from_column_names(self, cols):
        formatted_cols = [col.split('_')[0] for col in cols]
        return formatted_cols[:-1]
        
    def de_standardize(self, arr, cols, this_scaler):

        odds = this_scaler.inverse_transform(arr)

        return pd.DataFrame(odds, columns=cols)

    def decode(self, col_name, arr, this_encoder):
        return pd.DataFrame(this_encoder[col_name].inverse_transform(arr))
          
    def get_team_odds_book(self, datapoint_full, indices, strategy):

      datapoint = datapoint_full.iloc[indices]

      this_model_numerical_data = datapoint.iloc[:, :44]
      numerical_column_names = datapoint.columns[0:44].tolist()
      numerical_data_unstandardized = self.de_standardize(this_model_numerical_data, numerical_column_names, strategy['scaler'])

      # need to place highest_bettable_odds somewhere in here
      team_data = datapoint.iloc[:, 46:76]
      team_data_decoded = self.decode('team_1', team_data, strategy['encoder'])
      info_data = pd.concat([numerical_data_unstandardized, team_data_decoded], axis=1)
      info_data = info_data.rename(columns={info_data.columns[-1]: 'team'})

      return info_data

    def handle_bets(self, bet_df, stacked_df, strategy_name, bettable_books):
      live_results_df = pd.read_csv(f'live_performance_data/please_make_bets.csv')
      return_df = pd.DataFrame()

      stacked_df = stacked_df.rename(columns={'team_1': 'team'})

      stacked_df = self.make_snapshot_time(stacked_df)

      stacked_df = self.make_highest_bettable_odds(stacked_df, bettable_books)

      for idx, row in bet_df.iterrows():

        team = row['team']

        stacked_df_team = stacked_df[stacked_df['team'] == team]

        for sidx, srow in stacked_df_team.iterrows():
          if abs(srow['minutes_since_commence'] - row['minutes_since_commence']) <= 1:

            common_columns = stacked_df_team.columns.intersection(live_results_df.columns)

            df_to_append = stacked_df[common_columns]

            row_to_append = df_to_append.iloc[sidx].to_frame().T

            row_to_append  = self.fill_extra_cols(row_to_append, bettable_books)
            
            return_df = return_df.append(row_to_append, ignore_index=True)

      return return_df     

    def fill_extra_cols(self, df, bettable_books):

      df['ev'] = ((1/df['average_market_odds'])*(100*df['highest_bettable_odds']-100)) - ((1-(1/df['average_market_odds'])) * 100)
      df = df[df['ev'] >=10]

      df['ev'] = df['ev'].apply(lambda x: round(x, 2))

      game_id_to_commence_time = self.market_odds.set_index('game_id')['commence_time'].to_dict()

      df['date'] = df['game_id'].map(game_id_to_commence_time)

      df['date'] = pd.to_datetime(df['date']).dt.date

      def process_column_header(header):
        book = header.split('_1_odds')[0].title()
        return book
            
      def find_matching_columns(row):
          return [process_column_header(col) for col in bettable_books if row[col+'_1_odds'] == row['highest_bettable_odds']]

      df['sportsbooks_used'] = df.apply(find_matching_columns, axis=1)

      return df
    
    def make_snapshot_time(self, df):
       df['snapshot_time'] = pd.to_datetime('now', utc=True)
       df['snapshot_time'] = df['snapshot_time'] - pd.Timedelta(hours=7)
       df['snapshot_time'] = df['snapshot_time'].dt.tz_localize(None)

       return df
   
    
    def filter_by_lag_val(self, df, bettable_books):
        
        snap_time_col = df['snapshot_time']

        bettable_books.append('nordicbet')
        
        subset_columns = [col for col in df.columns if any(item in col for item in bettable_books)]

        time_cols = [col for col in subset_columns if '_1_time' in col]
        odds_cols = [col for col in subset_columns if '_1_odds' in col]
        odds_df = df[odds_cols]

        # Convert the bettable time columns to deltas
        time_df = pd.DataFrame()
        for col in time_cols:
            time_df[col] = pd.to_datetime(pd.to_datetime(df[col]).dt.time.astype(str))

        result_df = time_df.sub(snap_time_col, axis=0)

        result_df = result_df.abs()

        mask = result_df <= pd.Timedelta(seconds=10)

        mask.columns = odds_df.columns

        odds_df_masked = odds_df.where(mask, 0)

        time_cols = [x for x in df.columns if x.endswith('_time')]

        result = df.drop(columns=time_cols)

        result['highest_bettable_odds'] = odds_df_masked[odds_cols].max(axis=1)

        return result
    
    
    def make_highest_bettable_odds(self, df, bettable_books):
       
       df = self.filter_by_lag_val(df, bettable_books)

       return df








    



