# KKA-FP
Group 4 - Search for Suitable Houses

## Problem Statement
- Finding the right house location is increasingly difficult due to the need to balance three factors: distance to essential places, housing costs, and neighbourhood safety (crime rates). Affordable housing is usually located far from workplaces, while safer neighbourhoods and more convincing areas are typically more expensive. This creates a complex decision-making process for individuals and families. We chose this problem to provide a solution to help simplify the search by considering these factors together.

## Data Collected
We have attained 196 rows of data which entails on Districts/Quarters, its respective latitude and longitude coordinates, average house prices, and average crime rate percentages.

References are as follows: 
1. Districts/Quarters data: https://www.citypopulation.de/en/indonesia/kotasurabaya/admin/
2. Latitude and Longitude: Right clicking the middle of the area in Google Maps
3. Average House Prices: https://www.dotproperty.id/
4. Average Crime Rate Percentages: https://www.researchgate.net/publication/371511639_The_Utilization_of_Information_System_for_Crime_Rate_Modelling_in_Surabaya_Using_K-means

## Code Implementations
### 1. Informed Search (Uniform Cost Search)

 **Initialization**
```py
import pandas as pd
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
```py
target_lat = float(input("Enter target latitude: "))
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
```py
# Calculate distance between two points
def distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])  
    return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R
```
- Explanation
  
  This function, distance, determines the great-circle distance between two geographic locations on the Earth's surface (identified by lat1, lon1, and lat2, {lon2}). Using the Spherical Law of Cosines, it first converts latitude and longitude information from degrees to radians. The shortest route between the locations is then determined using the formula, where R = 6371.0 is the Earth's radius in kilometers. The final result is the distance in kilometers between the two places. Implementation for determining the ideal neighborhood based on average home price, distance to a target place, and crime rate.
 
```py
# Calculate distance and cumulative cost for each district
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
```py
# Retrieve the district with the lowest cost
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

### 2. Informed Search (A* Algorithm)
```py
# Calculate distance and cumulative heuristic cost for each district
priority_queue = []
for index, row in df.iterrows():
    distance = calculate_distance(target_lat, target_lon, row["Latitude"], row["Longitude"])
    g_cost = w_crime * row["Crime Rate (Percent)"] + w_distance * distance + w_price * row["Average House Price (IDR)"]
    h_cost = distance
    f_cost = g_cost + h_cost #heuristic function

    # Only consider districts meeting the threshold criteria
    if row["Crime Rate (Percent)"] <= max_crime_rate and distance <= max_distance and row["Average House Price (IDR)"] <= max_price:
        heapq.heappush(priority_queue, (f_cost, row["District"], distance, row["Average House Price (IDR)"], row["Crime Rate (Percent)"]))
```
The algorithm for A* Search is virtually the same as Uniform-Cost Search, with the addition of `f(n)` being our argument instead of cost, where `f(n) = cost + distance`.

Above is the modification done to Uniform-Cost Search to make it into an A* Search. Previously defined `cost` in UCS is redefined as `g_cost`, while two new variables `h_cost` representing distance and `f_cost` representing the whole heuristic function is added.
Now we push the heap using `f_cost` instead of `cost`

### 3. Local Search (Simulated Annealing)

```py
initial_temp = 1000
cooling_rate = 0.01

while temperature > 1e-3:

    neighbor_index = random.choice(df.index)
    neighbor_row = df.loc[neighbor_index]
    neighbor_distance = distance(target_lat, target_lon, neighbor_row["Latitude"], neighbor_row["Longitude"])

    
    if (neighbor_row["Crime Rate (Percent)"] <= max_crime_rate and
        neighbor_distance <= max_distance and
        neighbor_row["Average House Price (IDR)"] <= max_price):
        
        neighbor_cost = calculate_cost(neighbor_row, neighbor_distance)
        delta_cost = neighbor_cost - current_cost
        
        
        if delta_cost < 0 or np.random.rand() < exp(-delta_cost / temperature):
            current_index, current_row, current_cost, current_distance = neighbor_index, neighbor_row, neighbor_cost, neighbor_distance
            
        
            if current_cost < best_cost:
                best_row, best_cost = current_row, current_cost


    temperature *= (1 - cooling_rate)
```
For Simulated Annealing, it is the same as Uniform-Cost Search. The difference is only in how the search is conducted. It starts using a while loop until the temperature is smaller than 0.001.

`if delta_cost < 0 or np.random.rand() < exp(-delta_cost / temperature)` is a condition to check whether the neighbor cost is lower than the current cost. Additionally, if the delta cost is greater than 0, it also has an acceptance probability for a worse solution by comparing it with a randomly generated number. This allows the algorithm to explore other solutions and escape from local minima.
