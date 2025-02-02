import re

# File paths
input_file = "times.txt"
output_file = "predicted_times.txt"

def read_timestamps(file_path):
    timestamps = []
    last_number = None
    
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"(\d+) <-> .* (\d+)", line)
            if match:
                last_number = int(match.group(1))  # Extract number
                timestamps.append(int(match.group(2)))  # Extract timestamp
    
    return last_number, timestamps

def predict_timestamps(last_number, timestamps, num_predictions=100):
    differences = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps) - 1)]
    avg_diff = sum(differences) / len(differences)
    
    predictions = []
    next_timestamp = timestamps[-1]
    
    for i in range(1, num_predictions + 1):
        next_number = last_number + i
        next_timestamp += round(avg_diff)  # Predict using average difference
        predictions.append(f"{next_number} <-> ? {next_timestamp}")
    
    return predictions

def write_predictions(file_path, predictions):
    with open(file_path, "w") as file:
        file.write("\n".join(predictions) + "\n")

# Process data
last_number, timestamps = read_timestamps(input_file)
predictions = predict_timestamps(last_number, timestamps, 100)
write_predictions(output_file, predictions)

print(f"Predictions saved to {output_file}")
