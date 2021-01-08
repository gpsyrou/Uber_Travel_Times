
import os
import json
import pandas as pd

json_loc = r'D:\GitHub\Projects\Uber_Movement_Travel_Times\config.json'

with open(json_loc) as json_file:
    config = json.load(json_file)

project_folder = config["project_dir"]
os.chdir(project_folder)

import utilities.custom_functions as cf

data_files_loc = os.path.join(project_folder, 'sample_data')

# London data
london_file_loc = os.path.join(project_folder, 'london_data')
london_filename = 'london-lsoa-2020-1-All-HourlyAggregate.csv'

london_df = pd.read_csv(os.path.join(london_file_loc, london_filename),
                       header=[0], nrows=1000000)

# json file
json_filename = 'london_lsoa.json'

location_info_ls = []
with open(json_filename) as f:
    data = json.load(f)
    for loc_dict in data['features']:
        location_info_ls.append(cf.capture_data_from_json(loc_dict))

col_names = ['movement_id', 'display_name', 'la_name', 'coordinates']
location_data_df = pd.DataFrame.from_records(location_info_ls,
                                             columns=col_names)


df_enhanced = pd.merge(london_df, location_data_df, how='inner',
                       left_on=['sourceid'],
                       right_on=['movement_id'])
