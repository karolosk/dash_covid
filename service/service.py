from service.data_service import get_all_data, get_data
from service.who_service import generate_timeline_dataframe

def get_timeline_dataframe():
    return generate_timeline_dataframe()

def get_global_data():
    return get_all_data()

def get_table_data():
    return get_data()