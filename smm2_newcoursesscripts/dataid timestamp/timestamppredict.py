import time
import requests

# File paths
input_file = "1.txt"
output_file = "timestamps.txt"
api_url = "https://tgrcode.com/mm2/level_info/"

# Read input file and extract Data IDs and Course IDs
data_entries = []
with open(input_file, "r") as file:
    for line in file:
        parts = line.strip().split(" <-> ")
        if len(parts) == 2:
            data_id, course_id = parts
            data_entries.append((data_id, course_id))

# Process each entry with a 5-second delay
timestamps = []
for data_id, course_id in data_entries:
    response = requests.get(api_url + course_id)
    
    if response.status_code == 200:
        json_data = response.json()
        uploaded_timestamp = json_data.get("uploaded")

        if uploaded_timestamp:
            timestamps.append(f"{data_id} -> {uploaded_timestamp}")
            print(f"Fetched: {data_id} -> {uploaded_timestamp}")
        else:
            print(f"Warning: No 'uploaded' field for {data_id}")
    
    else:
        print(f"Error fetching {course_id}, status code: {response.status_code}")

    time.sleep(5)  # Wait 5 seconds before the next request

# Save timestamps to output file
with open(output_file, "w") as file:
    file.write("\n".join(timestamps))

print("Done! Timestamps saved to timestamps.txt.")
