# KKA-FP
Group 4 - Search for Suitable Houses

## Problem Statement
- Finding the right house location is increasingly difficult due to the need to balance three factors: distance to essential places, housing costs, and neighbourhood safety (crime rates). Affordable housing is usually located far from workplaces, while safer neighbourhoods and more convincing areas are typically more expensive. This creates a complex decision-making process for individuals and families. We chose this problem to provide a solution to help simplify the search by considering these factors together.

## Data Collected


### 1. Informed Search (Uniform Cost Search)

 **Initialization**
```import pandas as pd
import heapq
import numpy as np
from math import sin, cos, acos, radians

file_path = "/FP_KKA/District_Data.csv"  
df = pd.read_csv(file_path)

df["Average House Price (IDR)"] = df["Average House Price (IDR)"].replace(',', '', regex=True).astype(float)
```
- Explanation
  
  Reads data from a CSV file (District_Data.csv), imports the required libraries, then converts the Average House Price column to a numeric (float) format after removing commas. In later stages of the software, this gets the data ready for additional computations like cost and distance analysis.

 **User Inputs**
```target_lat = float(input("Enter target latitude: "))
target_lon = float(input("Enter target longitude: "))

w_crime = float(input("Enter weight for Crime Rate: "))
w_distance = float(input("Enter weight for Distance: "))
w_price = float(input("Enter weight for House Price: "))
max_crime_rate = float(input("Enter maximum allowed Crime Rate (percentage): "))
max_distance = float(input("Enter maximum allowed Distance (km): "))
max_price = float(input("Enter maximum allowed House Price (IDR): "))
```
- Explanation
  
  Gathers user input regarding the latitude and longitude of the target place, gives weights to the criteria of house price, distance, and crime rate, and establishes upper limits for each: the maximum permitted house price (in IDR), distance (in kilometers), and crime rate (in percentage). By weighing the relative relevance of each criterion and eliminating inappropriate possibilities, these inputs will direct the search process.

 **Distance Calculation between the Target Location and currently assessed district**
```# Calculate distance between two points
def distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])  
    return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R
```
- Explanation
  
  This function, distance, determines the great-circle distance between two geographic locations on the Earth's surface (identified by lat1, lon1, and lat2, {lon2}). Using the Spherical Law of Cosines, it first converts latitude and longitude information from degrees to radians. The shortest route between the locations is then determined using the formula, where R = 6371.0 is the Earth's radius in kilometers. The final result is the distance in kilometers between the two places. Implementation for determining the ideal neighborhood based on average home price, distance to a target place, and crime rate.
 
```# Calculate distance and cumulative cost for each district
priority_queue = []
for index, row in df.iterrows():
    distance = distance(target_lat, target_lon, row["Latitude"], row["Longitude"])
    cost = w_crime * row["Crime Rate (Percent)"] + w_distance * distance + w_price * row["Average House Price (IDR)"]

    # Only consider districts meeting the threshold criteria
    if row["Crime Rate (Percent)"] <= max_crime_rate and distance <= max_distance and row["Average House Price (IDR)"] <= max_price:
        heapq.heappush(priority_queue, (cost, row["District"], distance, row["Average House Price (IDR)"], row["Crime Rate (Percent)"]))
```
- Explanation
  
  Using user-defined weights, it iterates through each district in the dataset, computing a cumulative "cost" that includes the house price, distance, and crime rate. Each district is added to a priority queue, where entries are arranged by cumulative cost, provided that it satisfies the designated maximum thresholds for price, distance, and crime rate. From this priority queue, the district that best fits the requirements and has the lowest cost is then selected as the best option.

 **Prints out the results**
```# Retrieve the district with the lowest cost
if priority_queue:
    lowest_cost_district = heapq.heappop(priority_queue)
    print("Best district based on Uniform-Cost Search:")
    print(f"District: {lowest_cost_district[1]}, Cost: {lowest_cost_district[0]:,.0f}")
    print(f"Distance: {lowest_cost_district[2]:.2f} km, Avg House Price: {lowest_cost_district[3]:,.0f} IDR, Crime Rate: {lowest_cost_district[4]}%")
else:
    print("No suitable districts found that meet all criteria.")
```
- Explanation

  Obtains and shows the district from the priority_queue—which was constructed using Uniform-Cost Search—with the lowest cumulative cost. The district with the lowest cost is returned using heapq.heappop, which prints information such as the district name, cumulative cost, distance, average house price, and crime rate, if the priority_queue has any entries. It prints a message saying that no acceptable districts were discovered if the queue is empty, which indicates that no districts fit the requirements.

### 2. Uninformed Search (A* Algorithm)

### 3. Local Search
