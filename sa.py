import pandas as pd
import numpy as np
from math import sin, cos, acos, radians, exp
import random

# Load data
file_path = "C:\Code\District_Data.csv"
df = pd.read_csv(file_path)

# Data cleaning
df["Average House Price (IDR)"] = df["Average House Price (IDR)"].replace(',', '', regex=True).astype(float)

# Input parameters
target_lat = float(input("Enter target latitude: "))
target_lon = float(input("Enter target longitude: "))
w_crime = float(input("Enter weight for Crime Rate: "))
w_distance = float(input("Enter weight for Distance: "))
w_price = float(input("Enter weight for House Price: "))
max_crime_rate = float(input("Enter maximum allowed Crime Rate (percentage): "))
max_distance = float(input("Enter maximum allowed Distance (km): "))
max_price = float(input("Enter maximum allowed House Price (IDR): "))
initial_temp = 10
cooling_rate = 0.01


# Distance calculation function
def distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R

# Cost function
def calculate_cost(row, dist):
    return (w_crime * row["Crime Rate (Percent)"] +
            w_distance * dist +
            w_price * row["Average House Price (IDR)"])

# Simulated Annealing algorithm
current_index = random.choice(df.index)
current_row = df.loc[current_index]
current_distance = distance(target_lat, target_lon, current_row["Latitude"], current_row["Longitude"])
current_cost = calculate_cost(current_row, current_distance)
best_row, best_cost = current_row, current_cost

temperature = initial_temp

while temperature > 1e-3:
    # Get a random neighbor within the neighborhood radius
    neighbor_index = random.choice(df.index)
    neighbor_row = df.loc[neighbor_index]
    neighbor_distance = distance(target_lat, target_lon, neighbor_row["Latitude"], neighbor_row["Longitude"])

    # Check if the neighbor meets the criteria
    if (neighbor_row["Crime Rate (Percent)"] <= max_crime_rate and
        neighbor_distance <= max_distance and
        neighbor_row["Average House Price (IDR)"] <= max_price):
        
        neighbor_cost = calculate_cost(neighbor_row, neighbor_distance)
        delta_cost = neighbor_cost - current_cost
        
        # Determine if we should accept the neighbor
        if delta_cost < 0 or np.random.rand() < exp(-delta_cost / temperature):
            current_index, current_row, current_cost, current_distance = neighbor_index, neighbor_row, neighbor_cost, neighbor_distance
            
            # Update best solution if the new one is better
            if current_cost < best_cost:
                best_row, best_cost = current_row, current_cost

    # Cool down the temperature
    temperature *= (1 - cooling_rate)

# Output results
print("Best district based on Simulated Annealing:")
print(f"District: {best_row['District']}, Cost: {best_cost:,.0f}")
print(f"Distance: {current_distance:.2f} km, Avg House Price: {best_row['Average House Price (IDR)']:,.0f} IDR, Crime Rate: {best_row['Crime Rate (Percent)']}%")
