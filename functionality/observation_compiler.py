import pandas as pd
import sqlite3
import numpy as np
import time

class observation_compiler():
  def __init__(self):
    
    self.current_amount_of_nfl_observations = self.get_amount_of_master_sport_obs("NFL")

    self.current_amount_of_mlb_observations = self.get_amount_of_master_sport_obs("MLB")

    self.master_observations_sheet = pd.read_csv('users/master_model_observations.csv')

    self.schema = ['sport_title', 'completed','game_id', 'game_date', 'team', 'minutes_since_commence', 'opponent', 'snapshot_time', 'ev', 'average_market_odds', 'highest_bettable_odds', 'sportsbooks_used']


  def compile_observations(self):
    nfl_obs = pd.read_csv('users/model_obs_nfl.csv')
    mlb_obs = pd.read_csv('users/model_obs.csv')

    if len(nfl_obs) > self.current_amount_of_nfl_observations:
      amount_of_new_observations = len(nfl_obs) - self.current_amount_of_nfl_observations

      new_nfl_obs = nfl_obs.tail(amount_of_new_observations).copy()

      new_nfl_obs['sport_title'] = 'NFL'

      new_nfl_obs['team'] = nfl_obs['team_1']

      new_nfl_obs['completed'] = False

      new_nfl_obs['game_date'] = pd.to_datetime(new_nfl_obs['commence_time']).dt.date

      new_nfl_obs['average_market_odds'] = new_nfl_obs['average_market_odds_recent']
      new_df = new_nfl_obs[self.schema]

      self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

      self.current_amount_of_nfl_observations = len(nfl_obs)


    if len(mlb_obs) > self.current_amount_of_mlb_observations:
      amount_of_new_observations = len(mlb_obs) - self.current_amount_of_mlb_observations

      new_mlb_obs = mlb_obs.tail(amount_of_new_observations).copy()
      new_mlb_obs['sport_title'] = 'MLB'

      new_mlb_obs['completed'] = False

      new_mlb_obs['game_date'] = new_mlb_obs['date']

      new_df = new_mlb_obs[self.schema]

      self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

      self.current_amount_of_mlb_observations = len(mlb_obs)

    self.master_observations_sheet.to_csv('users/master_model_observations.csv', index=False)

  def update_completed_observations(self):
    conn = sqlite3.connect('smartbetter.db')
    scores = pd.read_sql('SELECT * FROM scores', conn)
    conn.close()

    completed_ids = scores['game_id'].unique().tolist()

    self.master_observations_sheet['completed'] = np.where(self.master_observations_sheet['game_id'].isin(completed_ids), True, False)

    self.master_observations_sheet.to_csv('users/master_model_observations.csv', index=False)


  def get_amount_of_master_sport_obs(self, sport_title):
    master_model_obs = pd.read_csv('users/master_model_observations.csv')

    sport_obs = master_model_obs[master_model_obs['sport_title'] == sport_title]

    return len(sport_obs)



    























    

    





