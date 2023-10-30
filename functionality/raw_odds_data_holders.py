import pandas as pd

class RawOddsHolders():
  def __init__(self):
    self.initialize_nfl_data()
    self.initialize_nba_data()

    

  def initialize_nfl_data(self):
    odds_data = pd.read_parquet('/Users/micahblackburn/Desktop/SMARTBETTOR_CODEBASE/odds_data/nfl_raw_odds_data.parquet')
    scores_data = pd.read_csv('../extra_info_sheets/nfl_extra_info.csv')

    odds_data = odds_data.dropna(subset=['team_1'])

    odds_data["commence_date"] = pd.to_datetime(odds_data["commence_time"]).dt.date.astype(str)
    odds_data['hour_of_start'] = pd.to_datetime(odds_data["commence_time"]).dt.hour.astype(str)
    odds_data["my_game_id"] =odds_data['team_1'] + odds_data['team_2'] + odds_data["commence_date"]

    scores_data['commence_date'] = pd.to_datetime(scores_data['date']).dt.date.astype(str)

    scores_data['my_game_id'] = scores_data['team_1'] + scores_data['team_2'] + scores_data["commence_date"]
     
    merged_df = pd.merge(odds_data, scores_data, on='my_game_id', how='outer', suffixes=('', '_df2'))

    self.raw_nfl_odds_data = merged_df

    return

  def initialize_nba_data(self):
    odds_data = pd.read_parquet('/Users/micahblackburn/Desktop/SMARTBETTOR_CODEBASE/odds_data/nba_raw_odds_data.parquet')
    scores_data = pd.read_csv('../extra_info_sheets/nba_extra_info.csv')

    odds_data = odds_data.dropna(subset=['team_1'])

    odds_data["commence_date"] = pd.to_datetime(odds_data["commence_time"]).dt.date.astype(str)
    odds_data['hour_of_start'] = pd.to_datetime(odds_data["commence_time"]).dt.hour.astype(str)
    odds_data["my_game_id"] =odds_data['team_1'] + odds_data['team_2'] + odds_data["commence_date"]

    scores_data['commence_date'] = pd.to_datetime(scores_data['date']).dt.date.astype(str)

    scores_data['my_game_id'] = scores_data['team_1'] + scores_data['team_2'] + scores_data["commence_date"]
     
    merged_df = pd.merge(odds_data, scores_data, on='my_game_id', how='outer', suffixes=('', '_df2'))

    self.raw_nba_odds_data = merged_df

    return
    

  