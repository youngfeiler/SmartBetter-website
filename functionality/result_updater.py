import pandas as pd
import requests
import os
from functionality.db_manager import DBManager


class result_updater():
    
  def __init__ (self):
      self.db_manager = DBManager()
      self.API_KEY = os.environ.get("THE_ODDS_API_KEY")
      self.MARKETS = 'h2h'
      self.REGIONS = 'us,eu,uk'
      self.ODDS_FORMAT = 'decimal'
      self.DATE_FORMAT = 'iso'
  

  def pull_scores(self, sport):
    self.scores_df = ''
    odds_response = requests.get(
      f'https://api.the-odds-api.com/v4/sports/{sport}/scores/',
      params={
          'api_key': self.API_KEY,
          'daysFrom': int(3)
      }
    )

    if odds_response.status_code != 200:
      print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
      odds_json = odds_response.json()

      df = pd.DataFrame.from_dict(odds_json)

      self.scores_df = df

      self.scores_json = odds_json

      return odds_json

  def update_results(self, sport):
     
     def get_final_score(team_name, data):
        for each in data['scores']:
           if each['name'] == team_name:
              return int(each['score'])
           else:
              pass
     
     try:
      scores_dict = self.pull_scores(sport)

      try:
          session = self.db_manager.create_session()
          df = pd.read_sql_table('scores', con=self.db_manager.get_engine())
      except Exception as e:
        print(e)
        raise
      finally:
        session.close()

      for each in scores_dict:
            if each['completed'] == False:
                pass
            elif each['completed'] == True:
                home_score = get_final_score(each['home_team'], each)
                away_score = get_final_score(each['away_team'], each)
                df_list = []
                df_list.append(each['id'])
                df_list.append(each['sport_title'])
                df_list.append(each['commence_time'])
                df_list.append(each['home_team'])
                df_list.append(each['away_team'])
                df_list.append(home_score)
                df_list.append(away_score)
                if home_score > away_score:
                    df_list.append(each['home_team'])
                elif home_score < away_score:
                    df_list.append(each['away_team'])
            df.loc[len(df)] = df_list
      df_unique_game_id = df.drop_duplicates(subset=['game_id'])

      try:
        session = self.db_manager.create_session()
        df_unique_game_id.to_sql('scores', con=self.db_manager.get_engine(), if_exists='replace', index=False)
      except Exception as e:
          print(e)
      finally:
        return True
     except:
        print("Live results couldn't be updated. Trying agiain in 5 min... ")
        return False




     



