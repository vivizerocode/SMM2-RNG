from datetime import datetime, timedelta, timezone

# Ask the user for the timestamp
timestamp_input = input("Enter your timestamp: ")

# Convert the input to an integer
try:
    timestamp = int(timestamp_input)
except ValueError:
    print("Invalid timestamp. Please enter a valid integer.")
    exit()

# Get the current time in UTC (timezone-aware)
current_time = datetime.now(timezone.utc)

# Convert the timestamp to a timezone-aware datetime object
uploaded_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)

# Calculate the difference between the current time and the uploaded time
time_difference = current_time - uploaded_time

# Extract the difference in milliseconds, seconds, and minutes
milliseconds = int(time_difference.total_seconds() * 1000)
seconds = int(time_difference.total_seconds())
minutes = int(time_difference.total_seconds() // 60)

# Format the output
if minutes > 0:
    print(f"{minutes} minutes ago")
elif seconds > 0:
    print(f"{seconds} seconds ago")
else:
    print(f"{milliseconds} milliseconds ago")