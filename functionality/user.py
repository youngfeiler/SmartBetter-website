import pandas as pd
from functionality.db_manager import db_manager

class User():
    def __init__(self, username):
        self.username = username
        self.password = ''


    def create_user(self, firstname, lastname, username, password, phone, bankroll, sign_up_date, payed):
      #df = pd.read_csv('users/login_info.csv')
      try:
          session = db_manager.create_session()
          df = pd.read_sql_table('login_info', con=db_manager.get_engine())
      except Exception as e:
        print(e)
        return str(e)
      finally:
        session.close()
      
      #change the column date_signed_up to string
      df['date_signed_up'] = df['date_signed_up'].astype(str)
      sign_up_date = str(sign_up_date)

      info_row = [firstname, lastname, self.username, password, phone, bankroll, payed, sign_up_date]

      df.loc[len(df)] = info_row
      try:
          df.to_sql('login_info', con=db_manager.get_engine(), if_exists='replace', index=False)
      except Exception as e:
        print(e)
        return (str(e))
      finally:
        return 
    def add_strategy_to_user(self, username, strategy_name):
      df = pd.read_csv('users/user_strategy_names.csv')
      info_row = [username, strategy_name, False]
      df.loc[len(df)] = info_row
      df.to_csv('users/user_strategy_names.csv', index=False)
    
    def delete_strategy_to_user(username, strategy_name):
      df = pd.read_csv('users/user_strategy_names.csv')
      df = df[~((df['username'] == username) & (df['strategy_name'] == strategy_name))]
      df.to_csv('users/user_strategy_names.csv', index=False)
      return df

    def get_strategies_associated_with_user(self):
      df = pd.read_csv('users/user_strategy_names.csv')
      df = df[df['username'] == self.username]
      strategies = df['strategy_name'].tolist()
      unique_strategies = list(set(strategies))
      return unique_strategies





