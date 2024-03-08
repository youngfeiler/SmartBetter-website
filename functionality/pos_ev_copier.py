import datetime
import pandas as pd
import time
import shutil

source_csv = './users/positive_ev_dash_data.csv'

destination_csv = './pos_ev_data.csv'

def copy_csv(source, destination):
    df = pd.read_csv(source)
    df.to_csv(destination, index=False)

while True:
    current_datetime = datetime.datetime.now()

    formatted_datetime = current_datetime.strftime("%d%m%Y_%H_%M_%S")
    
    destination_csv = f'./pos_ev_data_{formatted_datetime}.csv'
    
    copy_csv(source_csv, destination_csv)

    print(f"CSV copied successfully to {destination_csv}.")
    
    time.sleep(5 * 60)

    