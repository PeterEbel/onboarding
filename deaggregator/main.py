import pandas as pd
import numpy as np
from utils import data_generation
import random

file_cars = "cars.xlsx"
file_bikes = "bikes.xlsx"
file_others = "trucks.xlsx"

cars = pd.read_excel(file_cars)
bikes = pd.read_excel(file_bikes)
others = pd.read_excel(file_others)

motorbike_map = {
    'Federal State' : 'Federal State',
    'State District': 'State District',
    'County Code' : 'County Code',
    'County' : 'County',
    'Two wheels' : 'Number of Wheels',
    'Three wheels' : 'Number of Wheels',
    'Four wheels' : 'Number of Wheels',
    'Female bike owners': 'Female bike owners',
    'Year': 'Year'
}

car_map = {
    'Federal State' : 'Federal State',
    'State District': 'State District',
    'County Code' : 'County Code',
    'County' : 'County',
    'Engine size' : ['Small','Medium', 'Large', 'Unknown'],
    'Ownership' : ['Commercial','Private'],
    'Convertible':'Convertible Cars',
    'Fourwheel drive':'Fourwheel drive cars',
    'Trailer':'Trailer cars',
    'Ambulance':'Ambulance',
    'Engine Type': ['Petrol', 'Diesel', 'Gas', 'Hybrid', 'Electric', 'Other'],
    'Emission zone' : ['Euro 1', 'Euro 2', 'Euro 3', 'Euro 4', 'Euro 5', 'Euro 6','Other emmission'],
    'Year':'Year',
    'Vehicle type':'Vehicle type'
}

# generate deaggregated table (P.S. this will take a while)
# print('Generating motorbike table...')
# data_motorbikes = data_generation.gen_table(data=bikes,vehicle_type='motorbike',column_dict=motorbike_map)
# print('Saving motorbike CSV file...')
# data_motorbikes.to_csv('bikes.csv', header=False, sep='|' ,index=False)

print('Generating car table...')
data_cars = data_generation.gen_table(data=cars,vehicle_type='car',column_dict=car_map)
data_cars.to_csv('cars.csv', header=False, sep='|' ,index=False)

print('END!')
