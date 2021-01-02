
def capture_data_from_json(input_dict: dict) -> list:
    '''
    Given a dictionary from a json file, retrieve only the relevant information
    of interest
    '''
    movement_id = int(input_dict['properties']['MOVEMENT_ID'])
    display_name = str(input_dict['properties']['DISPLAY_NAME'])
    la_name = str(input_dict['properties']['la_name'])
    coordinates = input_dict['geometry']['coordinates']
    
    return [movement_id, display_name, la_name, coordinates]

