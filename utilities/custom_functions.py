import numpy as np

def retrieve_data_from_json(input_dict: dict) -> list:
    '''
    Parameters
    ----------
    input_dict : dict
        The json file contains irrelevant information. Pick only the relevant
        columns and cast them to the appropriate data type.

    Returns
    -------
    list
        A list of the columns of interest.

    '''
    movement_id = np.int64(input_dict['properties']['MOVEMENT_ID'])
    display_name = str(input_dict['properties']['DISPLAY_NAME'])
    la_name = str(input_dict['properties']['la_name'])
    coordinates = input_dict['geometry']['coordinates']
    
    return [movement_id, display_name, la_name, coordinates]
