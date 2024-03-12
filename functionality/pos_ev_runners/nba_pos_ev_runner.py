import requests
import os
import pandas as pd
import numpy as np
from pos_ev_runner_obj import PositiveEVDashboardRunner

if __name__ == '__main__':
   obj = PositiveEVDashboardRunner("NBA")

   while True:
      try:
         obj.make_live_dash_data()
      except Exception as e:
         print(e)