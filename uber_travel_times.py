
import os
import json
import pandas as pd

project_folder = r'/Users/georgiosspyrou/Desktop/GitHub/Projects/Uber_Travel_Times/Uber_Travel_Times'
os.chdir(project_folder)

import utilities.custom_functions as cf

data_files_loc = os.path.join(project_folder, 'sample_data')

'''
# Sample data

# Merge the files into one common pandas DataFrame
df_merged = pd.DataFrame()
sum_rows = 0
for file in os.listdir(data_files_loc):
    # Pick the country from the file name
    location_name = file.split('_')[2].replace('.csv', '')
    df_new = pd.read_csv(os.path.join(data_files_loc, file), header=[0])
    df_new['Location'] = location_name.upper()
    sum_rows += df_new.shape[0]
    df_merged = pd.concat([df_merged, df_new], sort=False, ignore_index=True)

'''

# London data

london_file_loc = os.path.join(project_folder, 'london_data')
london_filename = 'london-lsoa-2020-1-All-HourlyAggregate.csv'

london_df = pd.read_csv(os.path.join(london_file_loc, london_filename),
                       header=[0], nrows=10000)


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


# Merge the two datasets to get one combined df with all info for source
# and destionation
df_enhanced = pd.merge(london_df, location_data_df, how='inner',
                       left_on=['sourceid'],
                       right_on=['movement_id'])

df_enhanced = df_enhanced.merge(location_data_df, how='inner',
                                left_on=['dstid'], right_on=['movement_id'])

col_names_update = {'display_name_x': 'source_name', 
                    'display_name_y': 'destination_name',
                    'la_name_x': 'source_la_name',
                    'la_name_y': 'destination_la_name',
                    'coordinates_x': 'source_coordinates',
                    'coordinates_y': 'destination_coordinates'}

df_enhanced.rename(columns=col_names_update, inplace=True)
df_enhanced.drop(columns=['movement_id_x', 'movement_id_y'], inplace=True)











