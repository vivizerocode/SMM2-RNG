# File path
input_file = "timestamps.txt"

# Read timestamps from file
timestamps = []

with open(input_file, "r") as file:
    for line in file:
        parts = line.strip().split(" -> ")
        if len(parts) == 2:
            data_id, timestamp = parts
            timestamps.append(int(timestamp))

# Calculate time differences
time_differences = []
for i in range(1, len(timestamps)):
    diff = timestamps[i] - timestamps[i - 1]
    time_differences.append(diff)
    print(f"Difference between {timestamps[i-1]} and {timestamps[i]}: {diff} seconds")

# Compute average time difference
if time_differences:
    average_diff = sum(time_differences) / len(time_differences)
    print(f"\nAverage time difference: {average_diff:.2f} seconds")
else:
    print("Not enough timestamps to calculate differences.")
