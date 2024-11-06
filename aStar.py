import pandas as pd
import heapq
import numpy as np
from math import sin, cos, acos, radians
import time
import tracemalloc

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])  
    return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R

file_path = "District_Data.csv"  
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

start_time = time.time()
tracemalloc.start()

priority_queue = []
for index, row in df.iterrows():
    dist = calculate_distance(target_lat, target_lon, row["Latitude"], row["Longitude"])
    g_cost = (w_crime/100) * row["Crime Rate (Percent)"] + (w_distance/100) * dist + (w_price/100) * (row["Average House Price (IDR)"]/1000000000)
    h_cost = dist
    f_cost = g_cost + h_cost  # Heuristic function

    # Only consider districts meeting the threshold criteria
    if row["Crime Rate (Percent)"] <= max_crime_rate and dist <= max_distance and row["Average House Price (IDR)"] <= max_price:
        heapq.heappush(priority_queue, (f_cost, row["District"], dist, row["Average House Price (IDR)"], row["Crime Rate (Percent)"]))

# Retrieve the district with the lowest cost
if priority_queue:
    lowest_heurCost_district = heapq.heappop(priority_queue)
    print("Best district based on A* Search:")
    print(f"District: {lowest_heurCost_district[1]}, Cost: {lowest_heurCost_district[0]:,.0f}")
    print(f"Distance: {lowest_heurCost_district[2]:.2f} km, Avg House Price: {lowest_heurCost_district[3]:,.0f} IDR, Crime Rate: {lowest_heurCost_district[4]}%")
else:
    print("No suitable districts found that meet all criteria.")

# Calculate execution time and memory usage
execution_time = time.time() - start_time
current, peak = tracemalloc.get_traced_memory()
memory_usage_mb = peak / 10**6
tracemalloc.stop()

print(f"Execution Time: {execution_time:.4f} seconds, Memory Usage: {memory_usage_mb:.2f} MB")
