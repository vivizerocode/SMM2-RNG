import os
import json
import requests
import time
from datetime import datetime, timezone

# Create directories if they don't exist
os.makedirs('jsonsaved', exist_ok=True)

# Load the output.txt file into a dictionary
course_map = {}
with open('output.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(' <-> ')
        if len(parts) == 2:
            course_map[parts[0].strip()] = parts[1].strip()

# Default wait time in seconds
DEFAULT_WAIT_TIME = 7.2

def get_time_ago(timestamp):
    current_time = datetime.now(timezone.utc)
    uploaded_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    time_difference = current_time - uploaded_time
    seconds = int(time_difference.total_seconds())
    mins, secs = divmod(seconds, 60)
    return mins, secs, seconds

def parse_upload_time_pretty(upload_time_pretty):
    """Parse the upload time in pretty format (e.g., '12m 30s')"""
    time_parts = upload_time_pretty.split(' ')
    minutes = 0
    seconds = 0
    for part in time_parts:
        if 'm' in part:
            minutes = int(part.replace('m', ''))
        elif 's' in part:
            seconds = int(part.replace('s', ''))
    return minutes * 60 + seconds

def get_increment_based_on_seconds_elapsed(seconds):
    """Determine the increment based on how many seconds ago the level was uploaded."""
    if seconds <= 10:
        return 1  # Increment by 1 if 10 seconds ago or less
    return (seconds // 8) + 1  # Increment every 8 seconds

def process_course(num, course_id, consecutive_400s):
    url = f"https://tgrcode.com/mm2/level_info/{course_id}"
    response = None
    try:
        print(f"\nRequesting API for course {num} now...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Save JSON
        with open(f'jsonsaved/{num}_{course_id}.txt', 'w') as f:
            json.dump(data, f, indent=2)

        if 'uploaded' in data and 'upload_time_pretty' in data:
            uploaded = data['uploaded']
            upload_time_pretty = data['upload_time_pretty']
            mins, secs, seconds_ago = get_time_ago(uploaded)
            upload_seconds = parse_upload_time_pretty(upload_time_pretty)

            # Extract additional details
            name = data.get("name", "Unknown")
            description = data.get("description", "No description available.")
            tags = ', '.join(data.get("tags_name", []))
            game_style = data.get("game_style_name", "Unknown")
            theme = data.get("theme_name", "Unknown")

            print(f"\nName: {name}")
            print(f"Description: {description}")
            print(f"Tags: {tags}")
            print(f"Game Style: {game_style}")
            print(f"Theme: {theme}")
            print(f"\nCourse {num} ({course_id}):")
            print(f"Uploaded {mins} minutes and {secs} seconds ago")
            print(f"Upload time: {upload_time_pretty}")
            print(f"Seconds ago: {seconds_ago}")
            print(f"Incrementing by {get_increment_based_on_seconds_elapsed(seconds_ago)} based on time difference.")
            return 'increment', get_increment_based_on_seconds_elapsed(seconds_ago)

        return 'error', None
    
    except requests.exceptions.RequestException as e:
        if response is not None:
            if response.status_code == 429:
                print(f"Error 429: Rate limit reached. Waiting 6 seconds.")
                time.sleep(6)
                return 'retry', None
            elif response.status_code == 400:
                consecutive_400s += 1
                print(f"Error 400: Bad request. Skipping course {course_id}. Will subtract 1 and try again.")
                time.sleep(5)
                return 'skip', None

        print(f"Error processing {course_id}: {str(e)}")
        return 'error', None

def main_loop(start_num):
    current_num = start_num
    consecutive_400s = 0
    skipped_courses = set()  # Set to track courses that have been skipped permanently

    while True:
        str_num = str(current_num)
        course_id = course_map.get(str_num)

        if not course_id:
            print(f"No course ID found for {current_num}")
            return current_num

        # Skip if the course has been skipped permanently due to 400 errors
        if current_num in skipped_courses:
            print(f"Skipping permanently ignored course {current_num}.")
            current_num -= 1  # Decrease by 1 to try the next course
            continue

        status, increment = process_course(str_num, course_id, consecutive_400s)

        if status == 'increment':
            time.sleep(DEFAULT_WAIT_TIME)
            print(f"Incrementing by {increment} for course {current_num}")
            current_num += increment
        elif status == 'retry':
            time.sleep(DEFAULT_WAIT_TIME)
        elif status == 'skip':
            skipped_courses.add(current_num)  # Add to skipped courses set
            current_num -= 1  # Decrease by 1 to try a lower course number

def main():
    start_num = input("Enter starting 53xxxx number: ").strip()
    if not start_num.isdigit():
        print("Invalid input. Please enter a number.")
        return
    
    current_num = int(start_num)
    main_loop(current_num)

if __name__ == "__main__":
    main()
