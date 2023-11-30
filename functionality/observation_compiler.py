import pandas as pd
import sqlite3
import numpy as np
import time
from functionality.db_manager import DBManager


class observation_compiler():
  def __init__(self):

    self.db_manager = DBManager()
    
    self.current_amount_of_nfl_observations = self.get_amount_of_master_sport_obs("NFL")

    self.current_amount_of_mlb_observations = self.get_amount_of_master_sport_obs("MLB")

    self.current_amount_of_nba_observations = self.get_amount_of_master_sport_obs("NBA")

    self.current_amount_of_nhl_observations = self.get_amount_of_master_sport_obs("NHL")

    self.current_amount_of_nhl_observations_pregame = self.get_amount_of_master_sport_obs("NHL_PREGAME")

    self.current_amount_of_nba_observations_pregame = self.get_amount_of_master_sport_obs("NBA_PREGAME")

    self.current_amount_of_nfl_observations_pregame = self.get_amount_of_master_sport_obs("NFL_PREGAME")

    try:
          session = self.db_manager.create_session()
          self.master_observations_sheet = pd.read_sql_table('master_model_observations', con=self.db_manager.get_engine())
    except Exception as e:
      print(e)
      raise
    finally:
      session.close()
    

    self.master_observations_sheet = pd.read_csv('users/master_model_observations.csv')

    self.schema = ['sport_title', 'completed','game_id', 'game_date', 'team', 'minutes_since_commence', 'opponent', 'snapshot_time', 'ev', 'average_market_odds', 'highest_bettable_odds', 'sportsbooks_used']


  def compile_observations(self):
    nfl_obs = pd.read_csv('users/model_obs_nfl.csv')
    mlb_obs = pd.read_csv('users/model_obs.csv')
    nba_obs = pd.read_csv('users/model_obs_nba.csv')
    nhl_obs = pd.read_csv('users/model_obs_nhl.csv')
    nhl_obs_pregame = pd.read_csv('users/model_obs_nhl_pregame.csv')
    nba_obs_pregame = pd.read_csv('users/model_obs_nba_pregame.csv')
    nfl_obs_pregame = pd.read_csv('users/model_obs_nfl_pregame.csv')

    update = False


    if len(nfl_obs) > self.current_amount_of_nfl_observations:

      new_nfl_obs = nfl_obs.tail(amount_of_new_observations).copy()

      new_nfl_obs['sport_title'] = 'NFL'

      new_nfl_obs['team'] = nfl_obs['team_1']

      new_nfl_obs['completed'] = False

      new_nfl_obs['game_date'] = pd.to_datetime(new_nfl_obs['commence_time']).dt.date

      new_df = pd.DataFrame()

      new_df = new_nfl_obs[self.schema]

      self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

      self.current_amount_of_nfl_observations = len(nfl_obs)

      update = True

    if len(nfl_obs_pregame) > self.current_amount_of_nfl_observations_pregame:
      amount_of_new_observations = len(nfl_obs_pregame) - self.current_amount_of_nfl_observations_pregame

      new_nfl_obs = nfl_obs_pregame.tail(amount_of_new_observations).copy()

      new_nfl_obs['sport_title'] = 'NFL_PREGAME'

      new_nfl_obs['team'] = nfl_obs_pregame['team_1']

      new_nfl_obs['average_market_odds'] = nfl_obs_pregame['average_market_odds']

      new_nfl_obs['completed'] = False

      new_nfl_obs['game_date'] = pd.to_datetime(new_nfl_obs['commence_time']).dt.date

      new_df = pd.DataFrame()

      new_df = new_nfl_obs[self.schema]

      self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

      self.current_amount_of_nfl_observations_pregame = len(nfl_obs_pregame)

      update = True
    
    if len(nba_obs) > self.current_amount_of_nba_observations:
      amount_of_new_observations = len(nba_obs) - self.current_amount_of_nba_observations

      new_nba_obs = nba_obs.tail(amount_of_new_observations).copy()

      new_nba_obs['sport_title'] = 'NBA'

      new_nba_obs['team'] = nba_obs['team_1']

      new_nba_obs['completed'] = False

      new_nba_obs['game_date'] = pd.to_datetime(new_nba_obs['commence_time']).dt.date

      new_df = pd.DataFrame()

      new_df = new_nba_obs[self.schema]

      self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

      self.current_amount_of_nba_observations = len(nba_obs)

      update = True
    
    if len(nba_obs_pregame) > self.current_amount_of_nba_observations_pregame:
      amount_of_new_observations = len(nba_obs_pregame) - self.current_amount_of_nba_observations_pregame

      new_nba_obs = nba_obs_pregame.tail(amount_of_new_observations).copy()

      new_nba_obs['sport_title'] = 'NBA_PREGAME'

      new_nba_obs['team'] = nba_obs_pregame['team_1']

      new_nba_obs['completed'] = False

      new_nba_obs['game_date'] = pd.to_datetime(new_nba_obs['commence_time']).dt.date
      
      new_df = pd.DataFrame()

      new_df = new_nba_obs[self.schema]

      self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

      self.current_amount_of_nba_observations_pregame = len(nba_obs_pregame)

      update = True
    
    if len(nhl_obs) > self.current_amount_of_nhl_observations:
      amount_of_new_observations = len(nhl_obs) - self.current_amount_of_nhl_observations

      new_nhl_obs = nhl_obs.tail(amount_of_new_observations).copy()

      new_nhl_obs['sport_title'] = 'NHL'

      new_nhl_obs['team'] = nhl_obs['team_1']

      new_nhl_obs['completed'] = False

      new_nhl_obs['game_date'] = pd.to_datetime(new_nhl_obs['commence_time']).dt.date

      new_df = pd.DataFrame()

      new_df = new_nhl_obs[self.schema]

      self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

      self.current_amount_of_nhl_observations = len(nhl_obs)

      update = True
    
    if len(nhl_obs_pregame) > self.current_amount_of_nhl_observations_pregame:
      amount_of_new_observations = len(nhl_obs_pregame) - self.current_amount_of_nhl_observations_pregame

      new_nhl_obs = nhl_obs_pregame.tail(amount_of_new_observations).copy()

      new_nhl_obs['sport_title'] = 'NHL_PREGAME'

      new_nhl_obs['team'] = nhl_obs_pregame['team_1']

      new_nhl_obs['completed'] = False

      new_nhl_obs['game_date'] = pd.to_datetime(new_nhl_obs['commence_time']).dt.date

      new_df = pd.DataFrame()

      new_df = new_nhl_obs[self.schema]

      self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

      self.current_amount_of_nhl_observations_pregame = len(nhl_obs_pregame)

      update = True

<<<<<<< HEAD
    #if len(mlb_obs) > self.current_amount_of_mlb_observations:
            
     # self.master_observations_sheet = self.master_observations_sheet[self.master_observations_sheet['sport_title'] != 'MLB']

      # mlb_obs['sport_title'] = 'MLB'

      # mlb_obs['team'] = mlb_obs['team_1']

      # mlb_obs['completed'] = False

      # nhl_obs_pregame['game_date'] = pd.to_datetime(nhl_obs_pregame['commence_time']).dt.date
=======
    if len(mlb_obs) > self.current_amount_of_mlb_observations:
      amount_of_new_observations = len(mlb_obs) - self.current_amount_of_mlb_observations

      new_mlb_obs = mlb_obs.tail(amount_of_new_observations).copy()
      new_mlb_obs['sport_title'] = 'MLB'

      new_mlb_obs['completed'] = False

      new_mlb_obs['game_date'] = new_mlb_obs['date']
>>>>>>> c603b957715a40c1636218134bf3dba027f983e5

      # new_df = pd.DataFrame()

<<<<<<< HEAD
      # new_df = nhl_obs_pregame[self.schema]
=======
      new_df = new_mlb_obs[self.schema]
>>>>>>> c603b957715a40c1636218134bf3dba027f983e5

      # self.master_observations_sheet = pd.concat([self.master_observations_sheet, new_df], axis=0)

<<<<<<< HEAD
      # self.current_amount_of_nhl_observations_pregame = len(nhl_obs_pregame)
=======
      self.current_amount_of_mlb_observations = len(mlb_obs)
>>>>>>> c603b957715a40c1636218134bf3dba027f983e5

      # update = True

    self.master_observations_sheet.to_csv('users/master_model_observations.csv', index=False)
    self.master_observations_sheet['new_column'] = self.master_observations_sheet['game_id'].astype(str) + self.master_observations_sheet['snapshot_time'].astype(str)
    
    if update: 
      try:
            session = self.db_manager.create_session()
            self.master_observations_sheet.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='replace', index=False)
      except Exception as e:
          print(e)


  def update_completed_observations(self):
    try:
          session = self.db_manager.create_session()
          scores =  pd.read_sql_table('scores', con=self.db_manager.get_engine())
    except Exception as e:
        print(e)
        return str(e)
    finally:
        session.close()

    completed_ids = scores['game_id'].unique().tolist()

    self.master_observations_sheet['completed'] = np.where(self.master_observations_sheet['game_id'].isin(completed_ids), True, False)

    try:
          self.master_observations_sheet.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='replace', index=False)
    except Exception as e:
        print(e)
        return 
    finally:
        return 


  def get_amount_of_master_sport_obs(self, sport_title):
    try:
          session = self.db_manager.create_session()
          master_model_obs = pd.read_sql_table('master_model_observations', con=self.db_manager.get_engine())
    except Exception as e:
      print(e)
      return str(e)
    finally:
      session.close()
    sport_obs = master_model_obs[master_model_obs['sport_title'] == sport_title]

    return len(sport_obs)


    























    

    






