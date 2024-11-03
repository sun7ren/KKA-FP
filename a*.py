import pandas as pd
import heapq
import numpy as np
from math import sin, cos, acos, radians


file_path = "/FP_KKA/District_Data.csv"  
df = pd.read_csv(file_path)

df["Average House Price (IDR)"] = df["Average House Price (IDR)"].replace(',', '', regex=True).astype(float)


target_lat = float(input("Enter target latitude: "))
target_lon = float(input("Enter target longitude: "))

w_crime = float(input("Enter weight for Crime Rate: "))
w_distance = float(input("Enter weight for Distance: "))
w_price = float(input("Enter weight for House Price: "))
max_crime_rate = float(input("Enter maximum allowed Crime Rate (percentage): "))
max_distance = float(input("Enter maximum allowed Distance (km): "))
max_price = float(input("Enter maximum allowed House Price (IDR): "))

# Calculate distance between two points
def distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])  
    return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R

# Calculate distance and cumulative heuristic cost for each district
priority_queue = []
for index, row in df.iterrows():
    distance = distance(target_lat, target_lon, row["Latitude"], row["Longitude"])
    g_cost = w_crime * row["Crime Rate (Percent)"] + w_distance * distance + w_price * row["Average House Price (IDR)"]
    h_cost = distance
    f_cost = g_cost + h_cost #heuristic function

    # Only consider districts meeting the threshold criteria
    if row["Crime Rate (Percent)"] <= max_crime_rate and distance <= max_distance and row["Average House Price (IDR)"] <= max_price:
        heapq.heappush(priority_queue, (f_cost, row["District"], distance, row["Average House Price (IDR)"], row["Crime Rate (Percent)"]))

# Retrieve the district with the lowest cost
if priority_queue:
    lowest_heurCost_district = heapq.heappop(priority_queue)
    print("Best district based on A* Search:")
    print(f"District: {lowest_heurCost_district[1]}, Cost: {lowest_cost_district[0]:,.0f}")
    print(f"Distance: {lowest_heurCost_district[2]:.2f} km, Avg House Price: {lowest_heurCost_district[3]:,.0f} IDR, Crime Rate: {lowest_heurCost_district[4]}%")
else:
    print("No suitable districts found that meet all criteria.")
