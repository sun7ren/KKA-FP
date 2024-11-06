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
import time
import tracemalloc


file_path = "/FP_KKA/District_Data.csv"  
df = pd.read_csv(file_path)

df["Average House Price (IDR)"] = df["Average House Price (IDR)"].replace(',', '', regex=True).astype(float)
```
- Explanation
  
  The code imports the required libraries for data handling, calculations, and performance tracking. It reads the district data from a CSV file into a DataFrame and prepares the "Average House Price (IDR)" column for numerical operations by removing commas.

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
  
  This function calculates the distance between the target location and each district using the spherical law of cosines. It converts latitude and longitude from degrees to radians for accurate distance calculation in kilometers, considering the Earth’s curvature.

   **Start Time and Memory Allocating**
```py
start_time = time.time()
tracemalloc.start()
```
 - Explanation
  
  The program begins tracking execution time and memory usage. time.time() records the start time, and tracemalloc.start() enables memory monitoring. These measurements provide insights into the program’s efficiency.

    **Search Loop with Cost Allocation**
```py
priority_queue = []
for index, row in df.iterrows():
    distance = distance(target_lat, target_lon, row["Latitude"], row["Longitude"])
    cost = (w_crime/100) * row["Crime Rate (Percent)"] + (w_distance/100) * distance + 
    (w_price/100) * (row["Average House Price (IDR)"]/1000000000)

    if row["Crime Rate (Percent)"] <= max_crime_rate and distance <= max_distance and row["Average House Price (IDR)"] <= max_price:
        heapq.heappush(priority_queue, (cost, row["District"], distance, row["Average House Price (IDR)"], row["Crime Rate (Percent)"]))
```
- Explanation
  
  This loop iterates over each district, calculating the distance to the target location and a weighted "cost" based on the user’s criteria. Only districts meeting the maximum thresholds for crime rate, distance, and house price are considered. The calculated cost is a combination of crime rate, distance, and price, adjusted by their respective weights, and eligible districts are added to the priority queue.

 **Prints out the results**
```py
if priority_queue:
    lowest_cost_district = heapq.heappop(priority_queue)
    print("Best district based on Uniform-Cost Search:")
    print(f"District: {lowest_cost_district[1]}, Cost: {lowest_cost_district[0]:,.0f}")
    print(f"Distance: {lowest_cost_district[2]:.2f} km, Avg House Price: {lowest_cost_district[3]:,.0f} IDR, Crime Rate: {lowest_cost_district[4]}%")
else:
    print("No suitable districts found that meet all criteria.")
```
- Explanation

  The program retrieves the district with the lowest cost from the priority queue. It displays the selected district’s name, cost, distance, average house price, and crime rate. If no district meets the criteria, it notifies the user.

 **Performance Metrics**
```py
execution_time = time.time() - start_time
current, peak = tracemalloc.get_traced_memory()
memory_usage_mb = peak / 10**6
tracemalloc.stop()

print(f"Execution Time: {execution_time:.4f} seconds, Memory Usage: {memory_usage_mb:.2f} MB")
```
- Explanation

  The program calculates and displays the execution time and peak memory usage. Execution time is the difference between the start time and the current time, while memory usage is recorded using tracemalloc. These metrics help assess the program’s resource consumption.

### 2. Informed Search (A* Algorithm)
```py
priority_queue = []
for index, row in df.iterrows():
    dist = calculate_distance(target_lat, target_lon, row["Latitude"], row["Longitude"])
    g_cost = (w_crime/100) * row["Crime Rate (Percent)"] + (w_distance/100) * distance + (w_price/100) * (row["Average House Price (IDR)"]/1000000000)
    h_cost = dist
    f_cost = g_cost + h_cost  # Heuristic function

    # Only consider districts meeting the threshold criteria
    if row["Crime Rate (Percent)"] <= max_crime_rate and dist <= max_distance and row["Average House Price (IDR)"] <= max_price:
        heapq.heappush(priority_queue, (f_cost, row["District"], dist, row["Average House Price (IDR)"], row["Crime Rate (Percent)"]))
```
This loop iterates over each district in the DataFrame, calculates the weighted cost and heuristic distance, and adds eligible districts to the priority queue.

- g_cost represents the weighted cost based on crime rate, distance, and price.
- h_cost is the heuristic value, representing the actual distance to the target location.
- f_cost combines `g_cost` and `h_cost`, aligning with A*’s approach of balancing known costs with heuristic estimates.
Only districts that meet the maximum allowed thresholds for crime rate, distance, and price are considered and added to the priority queue, with the lowest `f_cost` prioritized.

### 3. Local Search (Simulated Annealing)

**Simulated Annealing Setup**
```py
current_index = random.choice(df.index)
current_row = df.loc[current_index]
current_distance = distance(target_lat, target_lon, current_row["Latitude"], current_row["Longitude"])
current_cost = calculate_cost(current_row, current_distance)
best_row, best_cost = current_row, current_cost

temperature = initial_temp
```
The program randomly selects an initial district to begin the Simulated Annealing process. It calculates the initial distance and cost for this district, then sets the initial district as the "current" and "best" solution. The temperature is initialized with the user-defined initial temperature.

**Simulated Annealing Loop**
```py
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
The loop iterates as long as the temperature remains above a small threshold. In each iteration:

- A neighboring district is randomly selected.
- The program checks if this neighboring district meets the maximum thresholds for crime rate, distance, and price.
- If it meets the criteria, the program calculates the neighbor's cost and compares it to the current cost.
    - If the new cost is lower, the neighbor becomes the current district.
    - If the new cost is higher, the program may still accept the neighbor with a probability that decreases as the temperature lowers, allowing exploration of potentially better solutions.
- If the neighbor’s cost is lower than the best cost, the neighbor becomes the best solution.
- The temperature decreases gradually, simulating the cooling process.

**Logging Results to CSV**
```py
with open(output_file, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([best_row['District'], f"{best_cost:,.0f}", f"{current_distance:.2f}", 
                     f"{best_row['Average House Price (IDR)']:,.0f}", f"{best_row['Crime Rate (Percent)']}", 
                     f"{execution_time:.4f}", f"{memory_usage_mb:.2f}"])
```
The final results are appended to the CSV log file. This includes the best district found, along with its cost, distance, average house price, crime rate, execution time, and memory usage, allowing a record of each run.