import requests
import os
import pandas as pd
import numpy as np
from pos_ev_runner_obj import PositiveEVDashboardRunner
pd.options.mode.chained_assignment = None


if __name__ == '__main__':
   obj = PositiveEVDashboardRunner("NCAAB")

   while True:
      try:
         obj.make_live_dash_data()
      except Exception as e:
         print(e)