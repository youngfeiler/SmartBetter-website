import pandas as pd

class RawOddsHolders():
  def __init__(self):
    self.initialize_nfl_data()
    self.initialize_nba_data()

    

  def initialize_nfl_data(self):
    odds_data = pd.read_parquet('/Users/micahblackburn/Desktop/SMARTBETTOR_CODEBASE/odds_data/nfl_raw_odds_data.parquet')
    scores_data = pd.read_csv('../extra_info_sheets/nfl_extra_info.csv')


    self.raw_nfl_odds_data = odds_data

    return

  def initialize_nba_data(self):
    odds_data = pd.read_parquet('/Users/micahblackburn/Desktop/SMARTBETTOR_CODEBASE/odds_data/nba_raw_odds_data.parquet')
    scores_data = pd.read_csv('../extra_info_sheets/nba_extra_info.csv')

  
    self.raw_nba_odds_data = odds_data

    return
    

  