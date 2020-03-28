from service.data_service import get_all_data, get_data
from service.who_service import generate_timeline_dataframe

def get_timeline_dataframe():
    return generate_timeline_dataframe()

def get_global_data():
    return get_all_data()

def get_table_data():
    return get_data()

def get_percentage_labels(data_list):
    labels = []
    
    # adding label for all cases
    cases = data_list[1][0]
    labels.append(cases)

    num_cases = cases.replace(',','')

    for value in data_list[1][1:]:

        num_value = value.replace(',','')
        labels.append(value +' ('+ str(round(100 * (float(num_value)/float(num_cases)) ,2)) +  '%)')

    return labels