
import os
import json
import List
import pandas as pd

project_folder = r'D:\GitHub\Projects\Uber_Movement_Travel_Times'
os.chdir(project_folder)

import utilities.custom_functions as cf

data_files_loc = os.path.join(project_folder, 'sample_data')

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
        location_info_ls.append(cf.retrieve_data_from_json(loc_dict))

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

col_names_updated = {'display_name_x': 'source_name', 
                    'display_name_y': 'destination_name',
                    'la_name_x': 'source_la_name',
                    'la_name_y': 'destination_la_name',
                    'coordinates_x': 'source_coordinates',
                    'coordinates_y': 'destination_coordinates'}

df_enhanced.rename(columns=col_names_updated, inplace=True)
df_enhanced.drop(columns=['movement_id_x', 'movement_id_y'], inplace=True)

# are the combinations unique?
df_enhanced.groupby(['sourceid','dstid']).size()




class Trip:
    '''
    Class corresponding to a specific trip and it's statistics. A trip has
    a starting and an end point. Between these two points the gps is sending 
    a different amount of pings per zone.
    
    Each ping is described in the format [latitude, longitude].
    '''
    
    def __init__(self, series: pd.core.series.Series):
        self.series = series
        
    def number_of_gps_pings(self, geom_point: str) -> int:
        num_gps_pings = len(self.series[geom_point][0][0])
        return num_gps_pings
    
    def split_pings_to_list(self, geom_point: str) -> list:
        gps_pings = [x for x in self.series[geom_point][0][0]]
        return gps_pings
    

    
    
x = Trip(df_enhanced.iloc[0])
x.number_of_gps_pings(geom_point='source_coordinates') # 40
x.number_of_gps_pings(geom_point='destination_coordinates') # 60
    


