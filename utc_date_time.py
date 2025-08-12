#!/usr/bin/env python3
"""
Current Timezone ISO Date in Python
Shows the current time in ISO format for the local timezone
"""

from datetime import datetime, timedelta
import json


def get_current_timezone_iso():
    """Get current time in ISO format for local timezone with timezone info"""
    # Get current local time with timezone info
    now_local = datetime.now().astimezone()
    iso_local = now_local.isoformat()    
    return now_local


def add_seconds_to_iso(original_datetime, seconds_to_add):
    """Add seconds to datetime and return ISO format"""
    modified_datetime = original_datetime + timedelta(seconds=seconds_to_add)
    iso_modified = modified_datetime.isoformat()
    return modified_datetime


def save_to_json(current_time, added_time):
    """Save current time and added time to JSON file"""
    data = {
        "CurrentTime": current_time.isoformat(),
        "AddedTime": added_time.isoformat()
    }
    
    with open("test.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Data saved to test.json")


def calculate_time_difference():
    """Read AddedTime from test.json, subtract from current time, and display result"""
    try:
        with open("test.json", "r") as json_file:
            data = json.load(json_file)
        
        added_time = datetime.fromisoformat(data["AddedTime"])
        current_time = datetime.now().astimezone()
        time_difference = current_time - added_time
        
        print(f"Current time: {current_time.isoformat()}")
        print(f"AddedTime   : {added_time.isoformat()}")
        print(f"Difference: {time_difference}")
        
        # Check if the difference is positive (expired)
        if time_difference.total_seconds() > 0:
            print("Expired")
        else:
            print("Not Expired Yet!!")
        
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to show current timezone ISO date"""
    print("Current Timezone ISO Date")
    print("=" * 30)
    
    # Get and display current timezone ISO date
    current_iso = get_current_timezone_iso()
    
    # Add 600 seconds (10 minutes) and display
    modified_iso = add_seconds_to_iso(current_iso, 600)
    
    # Calculate and display time difference
    calculate_time_difference()

    # Save results to JSON file
    # save_to_json(current_iso, modified_iso)
    
    print("=" * 30)
    print("Done!")    


if __name__ == "__main__":
    main()
