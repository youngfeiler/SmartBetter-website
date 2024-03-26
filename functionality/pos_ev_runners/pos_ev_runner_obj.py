import requests
import os
import pandas as pd
import numpy as np
from datetime import datetime
import traceback
import json
import flock as flock



class PositiveEVDashboardRunner():
  def __init__(self, sport):

    self.API_KEY = os.environ.get("THE_ODDS_API_KEY")

    self.sport = sport

    self.sport_path = {
       "NBA": "pos_ev_data/nba_pos_ev_data.csv",
       "NHL": "pos_ev_data/nhl_pos_ev_data.csv",
       "NCAAB": "pos_ev_data/ncaab_pos_ev_data.csv",
       }
    
    self.arb_sport_path = {
       "NBA": "arb_data/nba_arb_data.csv",
       "NHL": "arb_data/nhl_arb_data.csv",
       "NCAAB": "arb_data/ncaab_arb_data.csv",
       }
    
    self.market_view_sport_path = {
       "NBA": "market_view_data/nba_market_view_data.csv",
       "NHL": "market_view_data/nhl_market_view_data.csv",
       "NCAAB": "market_view_data/ncaab_market_view_data.csv",
       }
    
    self.sport_names = {
       "NBA": "basketball_nba",
       "NHL": "icehockey_nhl",
       "NCAAB": "basketball_ncaab",
       }

    self.sports = [self.sport_names[self.sport]]

    self.file_output_path = self.sport_path[self.sport]

    self.arb_file_output_path = self.arb_sport_path[self.sport]

    self.market_view_file_output_path = self.market_view_sport_path[self.sport]

    self.markets_sports = {
       'americanfootball_ncaaf': ['h2h', 'spreads', 'totals', 'alternate_spreads', 'alternate_totals', 'team_totals','player_pass_tds', 'player_pass_yds', 'player_pass_completions', 'player_pass_attempts', 'player_pass_interceptions', 'player_pass_longest_completion', 'player_rush_yds', 'player_rush_attempts', 'player_rush_longest', 'player_receptions', 'player_reception_yds', 'player_reception_longest', 'player_kicking_points', 'player_field_goals', 'player_tackles_assists', 'h2h_q1', 'h2h_q2', 'h2h_q3', 'h2h_q4', 'h2h_h1', 'h2h_h2', 'spreads_q1','spreads_q2', 'spreads_q3', 'spreads_q4', 'spreads_h1', 'spreads_h2', 'totals_q1', 'totals_q2', 'totals_q3', 'totals_q4', 'totals_h1', 'totals_h2'],

       'americanfootball_nfl': ['h2h', 'spreads', 'totals', 'alternate_spreads', 'alternate_totals', 'team_totals','player_pass_tds', 'player_pass_yds', 'player_pass_completions', 'player_pass_attempts', 'player_pass_interceptions', 'player_pass_longest_completion', 'player_rush_yds', 'player_rush_attempts', 'player_rush_longest', 'player_receptions', 'player_reception_yds', 'player_reception_longest', 'player_kicking_points', 'player_field_goals', 'player_tackles_assists', 'h2h_q1', 'h2h_q2', 'h2h_q3', 'h2h_q4', 'h2h_h1', 'h2h_h2', 'spreads_q1','spreads_q2', 'spreads_q3', 'spreads_q4', 'spreads_h1', 'spreads_h2', 'totals_q1', 'totals_q2', 'totals_q3', 'totals_q4', 'totals_h1', 'totals_h2'],

       'basketball_nba': [
          'h2h',
          'spreads', 
          'totals', 'alternate_spreads', 'alternate_totals','team_totals', 'player_points', 'player_rebounds', 'player_assists', 'player_threes', 'player_double_double', 'player_blocks', 'player_steals', 'player_turnovers', 'player_points_rebounds_assists', 'player_points_rebounds', 'player_points_assists', 'player_rebounds_assists', 'h2h_q1', 'h2h_q2', 'h2h_q3', 'h2h_q4', 'h2h_h1', 'h2h_h2', 'spreads_q1','spreads_q2', 'spreads_q3', 'spreads_q4', 'spreads_h1', 'spreads_h2', 'totals_q1', 'totals_q2', 'totals_q3', 'totals_q4', 'totals_h1', 'totals_h2'
          ],

       'basketball_ncaab':[
          'h2h', 
         'spreads', 'totals', 'alternate_spreads', 'alternate_totals', 
         'team_totals', 'player_points', 'player_rebounds', 'player_assists', 'player_threes', 'player_double_double', 'player_blocks', 'player_steals', 'player_turnovers', 'player_points_rebounds_assists', 'player_points_rebounds', 'player_points_assists', 'player_rebounds_assists', 'h2h_q1', 'h2h_q2', 'h2h_q3', 'h2h_q4', 'h2h_h1', 'h2h_h2', 'spreads_q1','spreads_q2', 'spreads_q3', 'spreads_q4', 'spreads_h1', 'spreads_h2', 'totals_q1', 'totals_q2', 'totals_q3', 'totals_q4', 'totals_h1', 'totals_h2'
                           ],

       'basketball_euroleague':['h2h', 'spreads', 'totals', 'alternate_spreads', 'alternate_totals', 'team_totals'],

       'icehockey_nhl':['h2h', 'spreads', 'totals', 'alternate_spreads', 'alternate_totals', 'team_totals', 'player_points', 'player_power_play_points', 'player_assists', 'player_blocked_shots', 'player_shots_on_goal', 'player_total_saves', 'h2h_p1', 'h2h_p2', 'h2h_p3', 'spreads_p1', 'spreads_p2', 'spreads_p3', 'totals_p1', 'totals_p2', 'totals_p3'],
    }

    self.featured_betting_markets = [
       'h2h', 
       'spreads', 
       'totals', 
       'outrights', 
       'h2h_lay', 
       'outrights_lay'
       ]

    self.additional_markets = [
       'alternate_spreads', 
       'alternate_totals', 
       'btts', 
       'draw_no_bet', 
       'team_totals'
       ] #h2h_3_way

    self.game_period_markets = [
       'h2h_q1', 'h2h_q2', 'h2h_q3', 'h2h_q4', 'h2h_h1', 'h2h_h2', 'h2h_p1',
       'h2h_p2', 'h2h_p3', 'spreads_q1', 'spreads_q2', 'spreads_q3', 'spreads_q4',
       'spreads_h1', 'spreads_h2', 'spreads_p1', 'spreads_p2', 'spreads_p3', 'totals_q1', 'totals_q2', 'totals_q3', 'totals_q4', 'totals_h1', 'totals_h2', 'totals_p1', 'totals_p2', 'totals_p3'
       ]

    self.nfl_ncaaf_player_props_markets = [
        'player_pass_tds',
        'player_pass_yds', 
        'player_pass_completions', 
        'player_pass_attempts', 
        'player_pass_interceptions', 
        'player_pass_longest_completion', 
        'player_rush_yds', 
        'player_rush_attempts', 
        'player_rush_longest', 
        'player_receptions', 
        'player_reception_yds', 
        'player_reception_longest', 
        'player_kicking_points', 
        'player_field_goals', 
        'player_tackles_assists', 
        'player_1st_td', 
        'player_last_td', 
        'player_anytime_td'
        ]

    self.nba_ncaab_wnba_player_props_markets = [
       'player_points', 
       'player_rebounds', 
       'player_assists', 
       'player_threes', 
       'player_double_double', 
       'player_blocks', 
       'player_steals', 
       'player_turnovers', 
       'player_points_rebounds_assists', 
       'player_points_rebounds', 
       'player_points_assists', 
       'player_rebounds_assists'
       ]

    self.nhl_player_props_markets = [
       'player_points', 
       'player_power_play_points', 
       'player_assists', 
       'player_blocked_shots', 
       'player_shots_on_goal', 
       'player_total_saves', 
       'player_goal_scorer_first', 
       'player_goal_scorer_last', 
       'player_goal_scorer_anytime'
       ]

    self.afl_player_props_markets=[
       'player_disposals', 
       'player_disposals_over', 
       'player_goal_scorer_first', 
       'player_goal_scorer_last', 
       'player_goal_scorer_anytime', 
       'player_goals_scored_over'
       ]

    self.market_type_dict = {
       'h2h': 'moneyline',
       'spreads': 'brown',
       'totals': 'spreads_and_totals',
       'alternate_totals': 'spreads_and_totals',
       'alternate_spreads': 'brown',
       'team_totals': 'green',
       'player_pass_tds': 'green',
       'player_pass_yds': 'green',
       'player_pass_completions': 'green',
       'player_pass_attempts': 'green',
       'player_pass_interceptions': 'green',
       'player_pass_longest_completion': 'green',
       'player_rush_yds': 'green',
       'player_rush_attempts': 'green',
       'player_rush_longest': 'green',
       'player_receptions': 'green',
       'player_reception_yds': 'green',
       'player_reception_longest': 'green',
       'player_kicking_points': 'green',
       'player_field_goals': 'green',
       'player_tackles_assists': 'green',
       'player_points': 'green', 
       'player_rebounds': 'green', 
       'player_assists': 'green',
       'player_threes': 'green', 
       'player_double_double': 'green',
       'player_blocks': 'green', 
       'player_steals': 'green', 
       'player_turnovers': 'green', 
       'player_points_rebounds_assists': 'green', 
       'player_points_rebounds': 'green', 
       'player_points_assists': 'green', 
       'player_rebounds_assists': 'green',
       'player_points': 'green',
       'player_power_play_points': 'green',
       'player_blocked_shots' : 'green',
       'player_shots_on_goal' : 'green',
       'player_total_saves': 'green',
       'h2h_q1': 'moneyline',
       'h2h_q2': 'moneyline',
       'h2h_q3': 'moneyline',
       'h2h_q4': 'moneyline',
       'h2h_h1': 'moneyline',
       'h2h_h2': 'moneyline',
       'h2h_p1': 'moneyline',
       'h2h_p2': 'moneyline',
       'h2h_p3': 'moneyline',
       'spreads_q1': 'brown',
       'spreads_q2': 'brown',
       'spreads_q3': 'brown', 
       'spreads_q4': 'brown',
       'spreads_h1': 'brown', 
       'spreads_h2': 'brown', 
       'spreads_p1': 'brown', 
       'spreads_p2': 'brown', 
       'spreads_p3': 'brown', 
       'totals_q1': 'spreads_and_totals', 
       'totals_q2': 'spreads_and_totals', 
       'totals_q3': 'spreads_and_totals', 
       'totals_q4': 'spreads_and_totals', 
       'totals_h1': 'spreads_and_totals',
       'totals_h2': 'spreads_and_totals', 
       'totals_p1': 'spreads_and_totals', 
       'totals_p2': 'spreads_and_totals', 
       'totals_p3': 'spreads_and_totals'
    }

  def get_list_of_sporting_events(self, sport):
      API_KEY = self.API_KEY
      SPORT = sport
    
      response = requests.get(
         f'https://api.the-odds-api.com/v4/sports/{SPORT}/events/?apiKey={API_KEY}'
                                   )

      if response.status_code != 200:
          print(f'Failed to get odds: status_code {response.status_code}, response body {response.text}')
      else:
        response_json = response.json()

        event_list = []

        for item in response_json:
           event_list.append(item['id'])
        
        return event_list
    
  def get_list_of_sports(self):
      API_KEY = self.API_KEY

      response = requests.get(
          f'https://api.the-odds-api.com/v4/sports?apiKey={API_KEY}',
          params={
              'api_key': API_KEY,
          }
      )

      if response.status_code != 200:
          print(f'Failed to get odds: status_code {response.status_code}, response body {response.text}')
      else:
        response_json = response.json()
        sport_list = []
        for item in response_json:
           sport_list.append(item['key'])
        
        return sport_list
     
  def get_odds(self, sport, game_id, market):
    
      API_KEY = self.API_KEY
      SPORT = sport
      REGIONS = 'us,us2,eu'
      MARKETS = market
      ODDS_FORMAT = 'decimal'
      DATE_FORMAT = 'iso'
      GAME_ID = game_id

      odds_response = requests.get(
          f'https://api.the-odds-api.com/v4/sports/{SPORT}/events/{GAME_ID}/odds?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}',
          params={
              'api_key': API_KEY,
              'regions': REGIONS,
              'markets': MARKETS,
              'oddsFormat': ODDS_FORMAT,
              'dateFormat': DATE_FORMAT,
              'events':game_id
          }
      )

      if odds_response.status_code != 200:
          print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
      else:
        odds_json = odds_response.json()

        return odds_json
    
  def digest_market_odds(self, sport, game_id, market):
     
     odds_df = pd.DataFrame(columns=['wagers'])

     odds_df['wagers'] = ''

     odds = self.get_odds(sport, game_id, market)

     game_date = odds['commence_time']

     for bookmaker in odds['bookmakers']:
        odds_df[bookmaker['key']] = 0
        for line in bookmaker['markets']:
           for each in line['outcomes']:
              if 'point' not in each:
                 wager_key = f"{each['name']}"
                 bet_type = self.market_type_dict.get(market)

              elif 'description' not in each:
                 wager_key = f"{each['name']}_{str(each['point'])}"
                 bet_type = self.market_type_dict.get(market)

              else:
                 wager_key = f"{each['description']}_{each['name']}_{str(each['point'])}"
                 bet_type = self.market_type_dict.get(market)
                 
              if wager_key not in odds_df['wagers'].values:
                new_row = pd.DataFrame({'wagers': [wager_key]})
                odds_df = pd.concat([odds_df, new_row], ignore_index=True)
            
              odds_df.loc[odds_df['wagers'] == wager_key, bookmaker['key']] = each['price']

     odds_df.fillna(0, inplace=True)

     if len(odds_df) > 0:

      odds_df['average_market_odds'] = (odds_df.iloc[:, 1:].sum(axis=1) / (odds_df.iloc[:, 1:] != 0).sum(axis=1).replace(0, np.nan))

      odds_df = self.check_for_bad_data(odds_df)

      odds_df['average_market_odds'] = (odds_df.iloc[:, 1:].sum(axis=1) / (odds_df.iloc[:, 1:] != 0).sum(axis=1).replace(0, np.nan))

      bettable_books = ['betclic', 'betfair_ex_au', 'betfair_ex_eu', 'betfair_ex_uk', 'betfair_sb_uk', 'betmgm', 'betonlineag', 'betparx', 'betr_au', 'betrivers', 'betsson', 'betus', 'betvictor', 'betway', 'bluebet', 'bovada', 'boylesports', 'casumo', 'coolbet', 'coral', 'draftkings', 'espnbet', 'everygame', 'fanduel', 'fliff', 'grosvenor', 'ladbrokes_au', 'ladbrokes_uk', 'leovegas', 'livescorebet', 'livescorebet_eu', 'lowvig', 'marathonbet', 'matchbook', 'mrgreen', 'mybookieag', 'neds', 'nordicbet', 'paddypower', 'pinnacle', 'playup', 'pointsbetau', 'pointsbetus', 'sisportsbook', 'skybet', 'sport888', 'sportsbet', 'superbook', 'suprabets', 'tipico_us', 'topsport', 'twinspires', 'unibet', 'unibet_eu', 'unibet_uk', 'unibet_us', 'virginbet', 'williamhill', 'williamhill_us', 'windcreek', 'wynnbet']

      selected_columns = [col for col in bettable_books if col in odds_df.columns]

      odds_df['highest_bettable_odds'] = odds_df[selected_columns].max(axis=1)

      odds_df, arb_df, market_view_df = self.calc_evs(odds_df, bet_type)

      odds_df.sort_values(by='ev', ascending=False, inplace=True)

      if len(odds_df) > 0:
         odds_df['sport_title'] = sport
         odds_df['game_id'] = game_id
         odds_df['market'] = market
         odds_df['wager'] = odds_df['wagers']
         odds_df['game_date'] = game_date
         odds_df['home_team'] =odds['home_team']
         odds_df['away_team'] =odds['away_team']
         odds_df = self.map_display_data('sport_title', odds_df)
         odds_df = self.map_display_data('market', odds_df)
         odds_df = self.map_display_data('wager', odds_df)
         self.handle_positive_ev_observations(odds_df)

         
      if len(arb_df) > 0:
         arb_df['sport_title'] = sport
         arb_df['game_id'] = game_id
         arb_df['market'] = market
         arb_df['wager'] = arb_df['wagers']
         arb_df['game_date'] = game_date
         arb_df['home_team'] = odds['home_team']
         arb_df['away_team'] = odds['away_team']
         arb_df = self.map_display_data('sport_title', arb_df)
         arb_df = self.map_display_data('market', arb_df)
         arb_df = self.map_display_data('wager', arb_df)
         self.handle_arb_observations(arb_df)

      if len(market_view_df) > 0:
         market_view_df['sport_title'] = sport
         market_view_df['game_id_market'] = game_id + market
         market_view_df['game_id'] = game_id
         market_view_df['market'] = market
         market_view_df['wager'] = market_view_df['wagers']
         market_view_df['game_date'] = game_date
         market_view_df['home_team'] = odds['home_team']
         market_view_df['away_team'] = odds['away_team']
         market_view_df = self.map_display_data('sport_title', market_view_df)
         market_view_df = self.map_display_data('market', market_view_df)
         market_view_df = self.map_display_data('wager', market_view_df)
         self.handle_market_view_observations(market_view_df)


      elif len(market_view_df) == 0:
         self.clear_market_view_observations(game_id, market)

     
  def calc_evs(self, df, type):
     if type == "moneyline":
        df = self.get_other_side_moneyline(df)
     elif type == "spreads_and_totals":
        df = self.get_other_side_pink(df)
     elif type == "brown":
        df = self.get_other_side_brown(df)
     elif type == "green":
        df = self.get_other_side_green(df)

     ev_df = self.calc_ev(df)

     arb_df = self.calc_arb(df)
     
     return ev_df, arb_df, df
  
  def calc_ev(self, df):
     df['no_vig_prob_1'] = (1 / df['average_market_odds']) / ((1 / df['average_market_odds']) + (1 / df['other_average_market_odds']))

     df['ev'] = ((df['highest_bettable_odds'] - 1) * df['no_vig_prob_1']) - (1 - df['no_vig_prob_1'])

     df['ev'] = df['ev'] * 100

     df = df[df['ev'] > 0]

     return df
  
  def calc_arb(self, df):
     df['implied_1'] = 1/df['highest_bettable_odds']
     df['implied_2'] = 1/df['highest_bettable_odds_other_X']
     df['implied_sum'] = df['implied_1'] + df['implied_2']

     df['arb_perc'] = (1 - df['implied_sum']) / df['implied_sum']

     df = df[df['arb_perc'] > 0]

     return df

  def get_other_side_moneyline(self, df):
      
      df = df[df['wagers'] != "Draw"]
      df['other_average_market_odds'] = 0
      df.loc[0, 'other_average_market_odds'] = df.loc[1, 'average_market_odds']
      df.loc[1, 'other_average_market_odds'] = df.loc[0, 'average_market_odds']

      df.loc[0, 'wagers_other'] = df.loc[1, 'wagers']
      df.loc[1, 'wagers_other'] = df.loc[0, 'wagers']

      result = pd.merge(df, df.copy(), left_on='wagers', right_on="wagers_other", suffixes=('', '_other_X'))

      return result
  
  def get_other_side_pink(self, df):
    df['value'] = df['wagers'].str.split('_').str[1]

    unique_names = df['wagers'].str.split('_').str[0].unique()

    name_0_rows = df[df['wagers'].str.startswith(unique_names[0])]
    name_1_rows = df[df['wagers'].str.startswith(unique_names[1])]

    merged = pd.merge(name_0_rows, name_1_rows, on='value', suffixes=(f"_{unique_names[0]}", f"_{unique_names[1]}"), how='inner')

    merged[f'other_average_{unique_names[0]}'] = merged[f'average_market_odds_{unique_names[1]}']
    merged[f'other_average_{unique_names[1]}'] = merged[f'average_market_odds_{unique_names[0]}']

    index_match_df = pd.DataFrame()

    index_match_df['wagers'] = pd.concat([merged[f'wagers_{unique_names[0]}'], merged[f'wagers_{unique_names[1]}']])

    index_match_df['wagers_other'] = pd.concat([merged[f'wagers_{unique_names[1]}'], merged[f'wagers_{unique_names[0]}']])

    index_match_df['other_average_market_odds'] = pd.concat([merged[f'other_average_{unique_names[0]}'], merged[f'other_average_{unique_names[1]}']])

    result = pd.merge(df, index_match_df, on='wagers', how='inner')

    result = pd.merge(result, result.copy(), left_on='wagers', right_on="wagers_other", suffixes=('', '_other_X'))

    return result
     
  def get_other_side_brown(self, df):
    df['value'] = df['wagers'].str.split('_').str[1]

    unique_names = df['wagers'].str.split('_').str[0].unique()
    unique_points = df['wagers'].str.split('_').str[1].unique()

    split_values = df['wagers'].str.split('_')

    df['other_side_of_bet'] = np.where(
      split_values.str[0] == unique_names[0],
      unique_names[1] + '_' + (split_values.str[1].astype(float) * -1).astype(str),
      unique_names[0] + '_' + (split_values.str[1].astype(float) * -1).astype(str)
    )

    name_0_rows = df[df['wagers'].str.startswith(unique_names[0])]
    name_1_rows = df[df['wagers'].str.startswith(unique_names[1])]

    merged = pd.merge(name_0_rows, name_1_rows, left_on='wagers', right_on='other_side_of_bet', suffixes=(f"_{unique_names[0]}", f"_{unique_names[1]}"), how='inner')

    merged[f'other_average_{unique_names[0]}'] = merged[f'average_market_odds_{unique_names[1]}']
    merged[f'other_average_{unique_names[1]}'] = merged[f'average_market_odds_{unique_names[0]}']

    index_match_df = pd.DataFrame()
    index_match_df['wagers'] = pd.concat([merged[f'wagers_{unique_names[0]}'], merged[f'wagers_{unique_names[1]}']])

    index_match_df['other_average_market_odds'] = pd.concat([merged[f'other_average_{unique_names[0]}'], merged[f'other_average_{unique_names[1]}']])

    result = pd.merge(df, index_match_df, on='wagers', how='inner')

    merged_df = pd.merge(result, result.copy(), left_on='wagers', right_on='other_side_of_bet', suffixes=('', '_other_X'))

    merged_df['wagers_other'] = merged_df['other_side_of_bet']

    merged_df.drop(columns='other_side_of_bet', inplace=True)

    return merged_df
  
  def get_other_side_green(self, df):
    df['value'] = df['wagers'].str.split('_').str[1]

    unique_names = df['wagers'].str.split('_').str[0].unique()
    unique_wagers = df['wagers'].str.split('_').str[1].unique()
    unique_points = df['wagers'].str.split('_').str[2].unique()

    split_values = df['wagers'].str.split('_')

    df['other_side_of_bet'] = np.where(
      split_values.str[1] == unique_wagers[0],
      split_values.str[0] + '_' + unique_wagers[1] + '_' + split_values.str[2],
      split_values.str[0] + '_' + unique_wagers[0] + '_' + split_values.str[2]
    )

    df1 = df.copy()
    df2 = df.copy()

    merged = pd.merge(df1, df2, left_on='wagers', right_on='other_side_of_bet', suffixes=(f"_{unique_wagers[0]}", f"_{unique_wagers[1]}"), how='inner')
    
    merged[f'other_average_{unique_wagers[0]}'] = merged[f'average_market_odds_{unique_wagers[1]}']

    merged[f'other_average_{unique_wagers[1]}'] = merged[f'average_market_odds_{unique_wagers[0]}']

    index_match_df = pd.DataFrame()
    index_match_df['wagers'] = pd.concat([merged[f'wagers_{unique_wagers[0]}'], merged[f'wagers_{unique_wagers[1]}']])

    index_match_df['wagers_other'] = pd.concat([merged[f'wagers_{unique_wagers[1]}'], merged[f'wagers_{unique_wagers[0]}']])

    index_match_df['other_average_market_odds'] = pd.concat([merged[f'other_average_{unique_wagers[0]}'], merged[f'other_average_{unique_wagers[1]}']])

    result = pd.merge(df, index_match_df, on='wagers', how='inner')

    result = pd.merge(result, result.copy(), left_on='wagers', right_on="wagers_other", suffixes=('', '_other_X'))

    result.drop(columns='other_side_of_bet', inplace=True)

    result.drop_duplicates(inplace=True)

    return result

  def get_other_side_spread_or_total(self, df):

    df['value'] = df['wagers'].str.split('_').str[1]

    over_rows = df[df['wagers'].str.startswith('Over_')]
    under_rows = df[df['wagers'].str.startswith('Under_')]

    merged = pd.merge(over_rows, under_rows, on='value', suffixes=('_Over', '_Under'), how='inner')

    merged['other_average_Over'] = merged['average_market_odds_Under']
    merged['other_average_Under'] = merged['average_market_odds_Over']

    index_match_df = pd.DataFrame()
    index_match_df['wagers'] = pd.concat([merged['wagers_Over'], merged['wagers_Under']])
    index_match_df['other_average_market_odds'] = pd.concat([merged['other_average_Over'], merged['other_average_Under']])

    result = pd.merge(df, index_match_df, on='wagers', how='inner')

    result = pd.merge(result, result.copy(), left_on='wagers', right_on="wagers_other", suffixes=('', '_other_X'))

    return result
  
  def find_matching_columns(self, row, bettable_books):
    matching_cols = [col.title() for col in bettable_books if row[col] == row['highest_bettable_odds']]
    return list(set(matching_cols))
  
  def find_matching_columns_other(self, row, bettable_books):
    matching_cols = [col.split("_other_X")[0].title() for col in bettable_books if row[col] == row['highest_bettable_odds_other_X']]
    return list(set(matching_cols))

  def handle_positive_ev_observations(self, df):
     
     bettable_books_full = ['betclic', 'betfair_ex_au', 'betfair_ex_eu', 'betfair_ex_uk', 'betfair_sb_uk', 'betmgm', 'betonlineag', 'betparx', 'betr_au', 'betrivers', 'betsson', 'betus', 'betvictor', 'betway', 'bluebet', 'bovada', 'boylesports', 'casumo', 'coolbet', 'coral', 'draftkings', 'espnbet', 'everygame', 'fanduel', 'fliff', 'grosvenor', 'ladbrokes_au', 'ladbrokes_uk', 'leovegas', 'livescorebet', 'livescorebet_eu', 'lowvig', 'marathonbet', 'matchbook', 'mrgreen', 'mybookieag', 'neds', 'nordicbet', 'paddypower', 'pinnacle', 'playup', 'pointsbetau', 'pointsbetus', 'sisportsbook', 'skybet', 'sport888', 'sportsbet', 'superbook', 'suprabets', 'tipico_us', 'topsport', 'twinspires', 'unibet', 'unibet_eu', 'unibet_uk', 'unibet_us', 'virginbet', 'williamhill', 'williamhill_us', 'windcreek', 'wynnbet']

     bettable_books = [col for col in df.columns if col in bettable_books_full]

     df['sportsbooks_used'] = df.apply(lambda row: self.find_matching_columns(row, bettable_books), axis=1)

     df['snapshot_time'] = pd.to_datetime(datetime.now())

     with open(self.file_output_path, 'r') as f:
         lock = flock.Flock(f, flock.LOCK_SH)
         with lock:
            full_df = pd.read_csv(f)

     all_columns = full_df.columns

     df = df.reindex(columns=all_columns, fill_value=0)

     result = pd.concat([full_df, df], ignore_index=True).fillna(0)

     with open(self.file_output_path, 'w') as f:
         lock = flock.Flock(f, flock.LOCK_EX)
         with lock:
            result.to_csv(self.file_output_path, index= False)
 
  def handle_arb_observations(self, df):
     
     bettable_books_full = ['betclic', 'betmgm', 'betonlineag', 'betparx', 'betr_au', 'betrivers', 'betus', 'betvictor', 'betway', 'bluebet', 'bovada', 'boylesports', 'casumo', 'coolbet', 'coral', 'draftkings', 'espnbet', 'everygame', 'fanduel', 'fliff', 'grosvenor', 'ladbrokes_au', 'ladbrokes_uk', 'leovegas', 'mrgreen', 'mybookieag', 'neds', 'nordicbet', 'paddypower', 'pinnacle', 'playup', 'pointsbetau', 'pointsbetus', 'sisportsbook', 'skybet', 'sport888', 'sportsbet', 'superbook', 'suprabets', 'tipico_us', 'topsport', 'twinspires', 'unibet', 'unibet_eu', 'unibet_uk', 'unibet_us', 'virginbet', 'williamhill', 'williamhill_us', 'windcreek', 'wynnbet']

     bettable_books = [col for col in df.columns if col in bettable_books_full]

     bettable_books_other = [col + "_other_X" for col in df.columns if col in bettable_books_full]

     df['sportsbooks_used'] = df.apply(lambda row: self.find_matching_columns(row, bettable_books), axis=1)

     df['sportsbooks_used_other_X'] = df.apply(lambda row: self.find_matching_columns_other(row, bettable_books_other), axis=1)

     df['snapshot_time'] = pd.to_datetime(datetime.now())

     with open(self.arb_file_output_path, 'r') as f:
         lock = flock.Flock(f, flock.LOCK_SH)
         with lock:
            full_df = pd.read_csv(f)

     all_columns = full_df.columns

     df = df.reindex(columns=all_columns, fill_value=0)

     result = pd.concat([full_df, df], ignore_index=True).fillna(0)

     with open(self.arb_file_output_path, 'w') as f:
         lock = flock.Flock(f, flock.LOCK_EX)
         with lock:
            result.to_csv(self.arb_file_output_path, index=False)

  def handle_market_view_observations(self, df):
     df['concatenated'] = np.where(df['wagers'] < df['wagers_other'], df['wagers'] + df['wagers_other'], df['wagers_other'] + df['wagers'])

     df.drop_duplicates(subset=['concatenated'], keep='first', inplace=True)
     
     df['market_reduced'] = df['market'].copy()
     
     df['market_reduced'] = df['market'].replace('alternate_totals', 'totals')

     df['market_reduced'] = df['market_reduced'].replace('alternate_spreads', 'spreads')

     df['market_reduced'] = np.where(df['market_reduced'].str.contains('player'), 
                                df['market_reduced'] + df['wager'], 
                                df['market_reduced'])
     def count_non_zero(row):
        return (row != 0).sum()
     
     grouped = df.groupby('market_reduced')

     max_non_zero_idxs = grouped.apply(lambda group: group.apply(count_non_zero, axis=1).idxmax())

     df['is_most'] = False
     for group, max_idx in max_non_zero_idxs.items():
         group_mask = df['market_reduced'] == group
         df.loc[group_mask, 'is_most'] = df.loc[group_mask].index == max_idx

     df['is_most'] = df['is_most'].astype(int)

     df['hashable_id'] = df['game_id'] + df['concatenated']

     df['snapshot_time'] = pd.to_datetime(datetime.now())

     with open(self.market_view_file_output_path, 'r') as f:
         lock = flock.Flock(f, flock.LOCK_SH)
         with lock:
            stored_data = pd.read_csv(f)

     stored_data_without_market = stored_data[stored_data['game_id_market'] != df['game_id_market'].iloc[0]]

     new_df = pd.concat([stored_data_without_market, df], ignore_index=True)

     new_df.fillna(0, inplace=True)

     with open(self.market_view_file_output_path, 'w') as f:
         lock = flock.Flock(f, flock.LOCK_EX)
         with lock:
            new_df.to_csv(self.market_view_file_output_path, index=False)

     return

  def clear_market_view_observations(self, game_id, market):
     
     with open(self.market_view_file_output_path, 'r') as f:
         lock = flock.Flock(f, flock.LOCK_SH)
         with lock:
            stored_data = pd.read_csv(f)

     game_id_market = game_id + market

     stored_data_without_market = stored_data[stored_data['game_id_market'] != game_id_market]

     with open(self.market_view_file_output_path, 'w') as f:
         lock = flock.Flock(f, flock.LOCK_EX)
         with lock:
            stored_data_without_market.to_csv(self.market_view_file_output_path, index=False)

     return
     
  def remove_event_obs(self, game_id):

   with open(self.file_output_path, 'r') as f:
         lock = flock.Flock(f, flock.LOCK_SH)
         with lock:
            df = pd.read_csv(f)
   df = df[df['game_id'] != game_id]

   with open(self.file_output_path, 'w') as f:
         lock = flock.Flock(f, flock.LOCK_EX)
         with lock:
            df.to_csv(self.file_output_path, index= False)

   with open(self.arb_file_output_path, 'r') as f:
         lock = flock.Flock(f, flock.LOCK_SH)
         with lock:
            df = pd.read_csv(f)
   df = df[df['game_id'] != game_id]
   with open(self.arb_file_output_path, 'w') as f:
         lock = flock.Flock(f, flock.LOCK_EX)
         with lock:
            df.to_csv(self.arb_file_output_path, index= False)

   return 
   
  def make_live_dash_data(self):

     # for each sport
     for sport in self.sports:
        print(sport)
        
        event_list = self.get_list_of_sporting_events(sport)

        # for each event
        for event in event_list:
          print(event)
          try:
            # Remove all listings of this event from our EV and Arb files, recalculate and refill
            self.remove_event_obs(event)
            # for each market
            for market in self.markets_sports.get(sport):
              print(market)
              try:
               #  print(market)
                self.digest_market_odds(sport, event, market)

              except Exception as e:
                  print(e)
                  pass
          except:
             pass
     
     return

  def map_display_data(self, column_name, df):
     if column_name == 'sport_title':
        sports = {
           'icehockey_nhl': 'Ice Hockey',
           'americanfootball_ncaaf': 'College Football',
           'americanfootball_nfl': 'Pro Football',
           'basketball_nba': 'Pro Basketball',
           'basketball_ncaab': 'College Basketball',
           'basketball_euroleague':'Pro Basketball'
        }
        leagues = {
           'icehockey_nhl': 'NHL',
           'americanfootball_ncaaf': 'NCAAF',
           'americanfootball_nfl': 'NFL',
           'basketball_nba': 'NBA',
           'basketball_ncaab': 'NCAAB',
           'basketball_euroleague':'Euroleague'
        }
        try:
         df['sport_title_display'] = df['sport_title'].map(sports)
         df['sport_league_display'] = df['sport_title'].map(leagues)
        except:
            df['sport_title_display'] = 0
            df['sport_league_display'] = 0
           
        return df
     
     elif column_name == 'market':
        markets = {
           'h2h': 'Moneyline',
           'spreads': 'Spread',
           'totals': 'Game Total',
           'alternate_spreads': 'Spread',
           'alternate_totals': 'Game Total',
           'team_totals': 'Team Total',
           'player_points':'Player Points',
           'player_rebounds':'Player Rebounds',
           'player_assists':'Player Assists',
           'player_threes':'Player Threes',
           'player_double_double':'Player Double Double',
           'player_blocks':'Player Blocks',
           'player_steals':'Player Steals',
           'player_turnovers':'Player Turnovers',
           'player_points_rebounds_assists':'Player Points + Rebounds + Assists',
           'player_points_rebounds':'Player Points + Rebounds',
           'player_points_assists':'Player Points + Assists',
           'player_rebounds_assists':'Player Rebounds + Assists',
           'player_pass_tds':"Player Passing TD's",
           'player_pass_yds':"Player Passing Yards",
           'player_pass_completions':"Player Pass Completions",
           'player_pass_attempts':"Player Pass Attempts",
           'player_pass_interceptions':"Player Interceptions",
           'player_pass_longest_completion':"Player Longest Completion",
           'player_rush_yds':"Player Rushing Yards",
           'player_rush_attempts':"Player Rushing Attempts",
           'player_rush_longest':"Player Longest Rush",
           'player_receptions':"Player Receptions",
           'player_reception_yds':"Player Receiving Yards",
           'player_reception_longest':"Player Longest Reception",
           'player_kicking_points':"Player Kicking Points",
           'player_field_goals':"Player Field Goals",
           'player_tackles_assists':"Player Tackles + Assists",
           'player_power_play_points':"Player Power Play Points",
           'player_blocked_shots':"Player Blocked Shots",
           'player_shots_on_goal': "Player Shots on Goal", 
           'player_total_saves': "Player Total Saves", 
           'player_total_saves': "Player Total Saves", 
           'h2h_q1': '1Q Moneyline',
            'h2h_q2': '2Q Moneyline',
            'h2h_q3': '3Q Moneyline',
            'h2h_q4': '4Q Moneyline',
            'h2h_h1': '1H Moneyline',
            'h2h_h2': '2H Moneyline',
            'h2h_p1': '1P Moneyline',
            'h2h_p2': '2P Moneyline',
            'h2h_p3': '3P Moneyline',
            'spreads_q1': '1Q Spread',
            'spreads_q2': '2Q Spread',
            'spreads_q3': '3Q Spread', 
            'spreads_q4': '4Q Spread',
            'spreads_h1': '1H Spread', 
            'spreads_h2': '2H Spread', 
            'spreads_p1': '1P Spread', 
            'spreads_p2': '2P Spread', 
            'spreads_p3': '3P Spread', 
            'totals_q1': '1Q Total', 
            'totals_q2': '2Q Total', 
            'totals_q3': '3Q Total', 
            'totals_q4': '4Q Total', 
            'totals_h1': '1H Total',
            'totals_h2': '2H Total', 
            'totals_p1': '1P Total', 
            'totals_p2': '2P Total', 
            'totals_p3': '3P Total'
        }

        try: 
         df['market_display'] = df['market'].map(markets)
        except:
          df['market_display'] = 0

        return df
     
     elif column_name == 'wager':
         # Define a function to check for "over" or "under" in a row
         def check_string(row):
               wager_parts = row['wager'].split("_")
               # Moneylines 
               if len(wager_parts) == 1:
                  return f'{row["wager"]}'
               
               elif len(wager_parts) == 2:
                  if row['wager'].split("_")[1][0] != '-':
                     return f'{row["wager"].split("_")[0]} +{row["wager"].split("_")[1]}'
                  else:
                     return f'{row["wager"].split("_")[0]} {row["wager"].split("_")[1]}'
                  
               elif len(wager_parts) == 3:
                  # Player props, team totals
                  if 'over' in row['wager'].split("_")[0].lower() or 'under' in row['wager'].split("_")[0].lower():
                     return f'{row["wager"].split("_")[0]} {row["wager"].split("_")[1]}'
                  if 'over' in row['wager'].split("_")[1].lower() or 'under' in row['wager'].split("_")[1].lower():
                     return f'{row["wager"].split("_")[0]} {row["wager"].split("_")[1]} {row["wager"].split("_")[2]}'
         def check_string_other(row):
               wager_parts = row['wagers_other'].split("_")
               
               # Moneylines 
               if len(wager_parts) == 1:
                  return f'{row["wagers_other"]}'
               
               elif len(wager_parts) == 2:
                  if row['wagers_other'].split("_")[1][0] != '-':
                     return f'{row["wagers_other"].split("_")[0]} +{row["wagers_other"].split("_")[1]}'
                  else:
                     return f'{row["wagers_other"].split("_")[0]} {row["wagers_other"].split("_")[1]}'
                  
               elif len(wager_parts) == 3:
                  # Player props, team totals
                  if 'over' in row['wagers_other'].split("_")[0].lower() or 'under' in row['wagers_other'].split("_")[0].lower():
                     return f'{row["wagers_other"].split("_")[0]} {row["wagers_other"].split("_")[1]}'
                  if 'over' in row['wagers_other'].split("_")[1].lower() or 'under' in row['wagers_other'].split("_")[1].lower():
                     return f'{row["wagers_other"].split("_")[0]} {row["wagers_other"].split("_")[1]} {row["wagers_other"].split("_")[2]}'
                  
                  # Team spreads  
         try:        
            df['wager_display'] = df.apply(check_string, axis=1)
         except:
            df['wager_display'] = 0
         try:
            df['wager_display_other'] = df.apply(check_string_other, axis=1)
         except:
            df['wager_display_other'] = 0
         return df
     
  def check_for_bad_data(self, df):

   # Check to make sure some oddsarent 500% greater one place than the market average
   for col in df.columns:
      try:
         mask = df[col] > df['average_market_odds'] * 5
      
         df.loc[mask, col] = 0
      except:
         pass

   return df