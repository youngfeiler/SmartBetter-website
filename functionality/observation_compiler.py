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
    

    self.schema = ['sport_title', 'completed','game_id', 'game_date', 'team', 'minutes_since_commence', 'opponent', 'snapshot_time', 'ev', 'average_market_odds', 'highest_bettable_odds', 'sportsbooks_used']


  def compile_observations(self):
    nfl_obs = pd.read_csv('users/model_obs_nfl.csv')
    mlb_obs = pd.read_csv('users/model_obs.csv')
    nba_obs = pd.read_csv('users/model_obs_nba.csv')
    nhl_obs = pd.read_csv('users/model_obs_nhl.csv')
    nhl_obs_pregame = pd.read_csv('users/model_obs_nhl_pregame.csv')
    nba_obs_pregame = pd.read_csv('users/model_obs_nba_pregame.csv')
    nfl_obs_pregame = pd.read_csv('users/model_obs_nfl_pregame.csv')

    self.current_amount_of_nfl_observations = self.get_amount_of_master_sport_obs("NFL")
    self.current_amount_of_mlb_observations = self.get_amount_of_master_sport_obs("MLB")
    self.current_amount_of_nba_observations = self.get_amount_of_master_sport_obs("NBA")
    self.current_amount_of_nhl_observations = self.get_amount_of_master_sport_obs("NHL")
    self.current_amount_of_nhl_observations_pregame = self.get_amount_of_master_sport_obs("NHL_PREGAME")
    self.current_amount_of_nba_observations_pregame = self.get_amount_of_master_sport_obs("NBA_PREGAME")
    self.current_amount_of_nfl_observations_pregame = self.get_amount_of_master_sport_obs("NFL_PREGAME")

    if len(nfl_obs) > self.current_amount_of_nfl_observations:
      new_obs = pd.DataFrame()

      amount_of_new_observations = len(nfl_obs) - self.current_amount_of_nfl_observations

      new_obs = nfl_obs.tail(amount_of_new_observations).copy()

      new_obs['sport_title'] = 'NFL'

      new_obs['team'] = new_obs['team_1']

      new_obs['completed'] = False

      new_obs['game_date'] = pd.to_datetime(new_obs['commence_time']).dt.date

      new_obs['new_column'] = new_obs['game_id'].astype(str) + new_obs['snapshot_time'].astype(str)

      new_df = pd.DataFrame()

      new_df = new_obs[self.schema]

      try:
          new_df.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='append', index=False)
      except Exception as e:
        print(e)
        return (str(e))  

    if len(nfl_obs_pregame) > self.current_amount_of_nfl_observations_pregame:
      new_obs = pd.DataFrame()

      amount_of_new_observations = len(nfl_obs_pregame) - self.current_amount_of_nfl_observations_pregame

      new_obs = nfl_obs_pregame.tail(amount_of_new_observations).copy()

      new_obs['sport_title'] = 'NFL_PREGAME'

      new_obs['team'] = new_obs['team_1']

      new_obs['completed'] = False

      new_obs['game_date'] = pd.to_datetime(new_obs['commence_time']).dt.date

      new_obs['new_column'] = new_obs['game_id'].astype(str) + new_obs['snapshot_time'].astype(str)

      new_df = pd.DataFrame()

      new_df = new_obs[self.schema]

      try:
          new_df.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='append', index=False)
      except Exception as e:
        print(e)
        return (str(e))
    
    if len(nba_obs) > self.current_amount_of_nba_observations:
      new_obs = pd.DataFrame()

      amount_of_new_observations = len(nba_obs) - self.current_amount_of_nba_observations

      new_obs = nba_obs.tail(amount_of_new_observations).copy()

      new_obs['sport_title'] = 'NBA'

      new_obs['team'] = new_obs['team_1']

      new_obs['completed'] = False

      new_obs['game_date'] = pd.to_datetime(new_obs['commence_time']).dt.date

      new_obs['new_column'] = new_obs['game_id'].astype(str) + new_obs['snapshot_time'].astype(str)

      new_df = pd.DataFrame()

      new_df = new_obs[self.schema]

      try:
          new_df.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='append', index=False)
      except Exception as e:
        print(e)
        return (str(e))
    
    if len(nba_obs_pregame) > self.current_amount_of_nba_observations_pregame:
      new_obs = pd.DataFrame()

      amount_of_new_observations = len(nba_obs_pregame) - self.current_amount_of_nba_observations_pregame

      new_obs = nba_obs_pregame.tail(amount_of_new_observations).copy()

      new_obs['sport_title'] = 'NBA_PREGAME'

      new_obs['team'] = new_obs['team_1']

      new_obs['completed'] = False

      new_obs['game_date'] = pd.to_datetime(new_obs['commence_time']).dt.date

      new_obs['new_column'] = new_obs['game_id'].astype(str) + new_obs['snapshot_time'].astype(str)

      new_df = pd.DataFrame()

      new_df = new_obs[self.schema]

      try:
          new_df.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='append', index=False)
      except Exception as e:
        print(e)
        return (str(e))
    
    if len(nhl_obs) > self.current_amount_of_nhl_observations:
      new_obs = pd.DataFrame()


      amount_of_new_observations = len(nhl_obs) - self.current_amount_of_nhl_observations

      new_obs = nhl_obs.tail(amount_of_new_observations).copy()

      new_obs['sport_title'] = 'NHL'

      new_obs['team'] = new_obs['team_1']

      new_obs['completed'] = False

      new_obs['game_date'] = pd.to_datetime(new_obs['commence_time']).dt.date

      new_obs['new_column'] = new_obs['game_id'].astype(str) + new_obs['snapshot_time'].astype(str)

      new_df = pd.DataFrame()

      new_df = new_obs[self.schema]

      try:
          new_df.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='append', index=False)
      except Exception as e:
        print(e)
        return (str(e))
    
    if len(nhl_obs_pregame) > self.current_amount_of_nhl_observations_pregame:
      new_obs = pd.DataFrame()

      amount_of_new_observations = len(nhl_obs_pregame) - self.current_amount_of_nhl_observations_pregame

      new_obs = nhl_obs_pregame.tail(amount_of_new_observations).copy()

      new_obs['sport_title'] = 'NHL_PREGAME'

      new_obs['team'] = new_obs['team_1']

      new_obs['completed'] = False

      new_obs['game_date'] = pd.to_datetime(new_obs['commence_time']).dt.date

      new_obs['new_column'] = new_obs['game_id'].astype(str) + new_obs['snapshot_time'].astype(str)

      new_df = pd.DataFrame()

      new_df = new_obs[self.schema]

      try:
          new_df.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='append', index=False)
      except Exception as e:
        print(e)
        return (str(e))

    if len(mlb_obs) > self.current_amount_of_mlb_observations:
      new_obs = pd.DataFrame()

      amount_of_new_observations = len(mlb_obs) - self.current_amount_of_mlb_observations

      new_obs = mlb_obs.tail(amount_of_new_observations).copy()

      new_obs['sport_title'] = 'MLB'

      new_obs['team'] = new_obs['team']

      new_obs['completed'] = False

      new_obs['game_date'] = new_obs['date']

      new_obs['new_column'] = new_obs['game_id'].astype(str) + new_obs['snapshot_time'].astype(str)

      new_df = pd.DataFrame()

      new_df = new_obs[self.schema]

      try:
          new_df.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='append', index=False)
      except Exception as e:
        print(e)
        return (str(e))

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

    uncompleted_obs = self.master_observations_sheet[self.master_observations_sheet['completed'] == False]['game_id'].unique().tolist()

    self.master_observations_sheet['completed'] = np.where(
        self.master_observations_sheet['game_id'].isin(completed_ids),
        True,
        False
      )
    try:
          self.master_observations_sheet.to_sql('master_model_observations', con=self.db_manager.get_engine(), if_exists='replace', index=False)
    except Exception as e:
        print(e)
        return 

  def get_amount_of_master_sport_obs(self, sport_title):
    try:
          session = self.db_manager.create_session()
          query = """
            SELECT COUNT(*) 
            FROM master_model_observations
            WHERE sport_title = :sport_title
            """
          engine = self.db_manager.get_engine()
          result = session.execute(query, {"sport_title": sport_title})
          length = result.scalar()
          session.close()
          print(length)
        
    except Exception as e:
      print(e)
      return str(e)
    finally:
      # session.close()
      return length


    























    

    






