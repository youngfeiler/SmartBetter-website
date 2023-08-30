import pandas as pd
import sqlite3

class User():
    def __init__(self, username):
        self.username = username
        self.password = ''
    def make_conn(self):
        conn = sqlite3.connect('smartbetter.db')
        return conn

    def create_user(self, firstname, lastname, username, password, phone, bankroll):
      #df = pd.read_csv('users/login_info.csv')
      conn = self.make_conn()
      df = pd.read_sql('SELECT * FROM login_info', conn)
      info_row = [firstname, lastname, self.username, password, phone, bankroll]

      df.loc[len(df)] = info_row

      #df.to_csv('users/login_info.csv', index=False)
      df.to_sql('login_info', conn, if_exists='replace', index=False)

      self.add_strategy_to_user(self.username, 'SmartBetter low risk demo strategy')
      conn.commit()  # Commit the changes
      conn.close()   # Close the connection

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





