from .model_runner import model_runner
from .database import database
from .live_dashboard_runner import live_dashboard_runner
from .live_nfl_dashboard_runner import live_nfl_dashboard_runner
from .live_nba_dashboard_runner import live_nba_dashboard_runner
from .live_nhl_dashboard_runner import live_nhl_dashboard_runner
from .pregame_nhl_dashboard_runner import pregame_nhl_dashboard_runner
from .pregame_nba_dashboard_runner import pregame_nba_dashboard_runner
from .pregame_mlb_dashboard_runner import pregame_mlb_dashboard_runner


import time 
from collections import OrderedDict
from celery import Celery
from .result_updater import result_updater
from .observation_compiler import observation_compiler

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    task_serializer='json'
)

@celery.task
def make_strategy(name, min_ev, min_odds, max_odds, min_min_com, max_min_com, num_epochs, bettable_books):
  # TODO: Check if this strategy already exists

  strat_params_dict = OrderedDict({
            'min_minutes_since_commence':min_min_com,
            'max_minutes_since_commence':max_min_com,
            'min_ev':min_ev,
            'min_avg_odds':min_odds,
            'max_avg_odds':max_odds,
            'bettable_books': bettable_books
        })

  my_db = database()

  if my_db.check_if_strategy_exists_and_handle_duplicate(name, strat_params_dict):
    return

  strat_maker = strategy_maker(
    name=name,
    min_ev=min_ev,
    min_avg_odds=min_odds,
    max_avg_odds=max_odds,
    min_minutes_since_commence=min_min_com,
    max_minutes_since_commence=max_min_com,
    num_epochs=num_epochs,
    bettable_books=bettable_books
  )
  
  return
  
@celery.task
def start_model_runner():

  my_db = database()

  mr = model_runner()

@celery.task
def start_dashboard_runner():
  
    live_nba_dashboard_runner_instance = live_nba_dashboard_runner()
    live_nhl_dashboard_runner_instance = live_nhl_dashboard_runner()

    pregame_nhl_dashboard_runner_instance = pregame_nhl_dashboard_runner()
    pregame_nba_dashboard_runner_instance = pregame_nba_dashboard_runner()
    pregame_mlb_dashboard_runner_instance = pregame_mlb_dashboard_runner()

    # pregame_nfl_dashboard_runner_instance = pregame_nfl_dashboard_runner()

    result_updater_instance = result_updater()

    observation_compiler_instace = observation_compiler()
    observation_compiler_instace.compile_observations()

    while True:

      try: 
        # result_updater_instance.update_results('baseball_mlb')
        result_updater_instance.update_results('americanfootball_nfl')

        result_updater_instance.update_results('basketball_nba')

        result_updater_instance.update_results('baseball_mlb')

        result_updater_instance.update_results('icehockey_nhl')

        pregame_nhl_dashboard_runner_instance.make_live_dash_data()

        pregame_nba_dashboard_runner_instance.make_live_dash_data()

        pregame_mlb_dashboard_runner_instance.make_live_dash_data()

        live_nba_dashboard_runner_instance.make_live_dash_data()

        observation_compiler_instace.compile_observations()

        observation_compiler_instace.compile_observations()

        live_nhl_dashboard_runner_instance.make_live_dash_data()

        live_nba_dashboard_runner_instance.make_live_dash_data()

        observation_compiler_instace.compile_observations()
        
        observation_compiler_instace.update_completed_observations()

      except Exception as e:
        print(e)

  
