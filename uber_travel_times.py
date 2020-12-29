
import os
import pandas as pd

project_folder = r'D:\GitHub\Projects\Uber_Movement_Travel_Times'
os.chdir(project_folder)

data_files_loc = os.path.join(project_folder, 'sample_data')


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

