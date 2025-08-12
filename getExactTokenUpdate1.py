# In order to run this python code properly, first create a json file "exact_token_response.json" with the following params:
# {
#     "refresh_token": <Your Latest Refresh Token>,
#     "client_id": <Your client ID>,
#     "client_secret": <Your client secret>,
#     "issue_date_utc": <Issue date ISO>,
#     "expire_date_utc": <Expire Date ISO>
# }

# Example
# {
#     "access_token": "stampNL001.gAAAAAlLc0ZA1a...",
#     "token_type": "bearer",
#     "expires_in": "600",
#     "refresh_token": "stampNL001.jHaG!IAAAAE18Y3xK...",
#     "client_id": "8059c106-9dac-4e8a-8611-937adfcae815",
#     "client_secret": "oK74xnmfBrgn",
#     "issue_date_utc": "2025-08-10T22:10:35.479369+05:45",
#     "expire_date_utc": "2025-08-10T22:20:35.479369+05:45"
# }

import requests
import json
from datetime import datetime, timedelta

def get_exact_token(refresh_token, client_id, client_secret):
    """
    Get a new access token from Exact Online using refresh token
    
    Args:
        refresh_token (str): The refresh token
        client_id (str): The client ID
        client_secret (str): The client secret
    
    Returns:
        dict: Response from the API containing the new access token
    """
    
    # API endpoint
    url = "https://start.exactonline.nl/api/oauth2/token"
    
    # Parameters to be sent as x-www-form-urlencoded
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    # Headers for x-www-form-urlencoded
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        # Make POST request
        response = requests.post(url, data=data, headers=headers)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def get_current_timezone_iso():
    """Get current time in ISO format for local timezone with timezone info"""
    # Get current local time with timezone info
    now_local = datetime.now().astimezone()
    iso_local = now_local.isoformat()
    
    print(f"Current local time (ISO): {iso_local}")
    return now_local


def add_seconds_to_iso(original_datetime, seconds_to_add):
    """Add seconds to datetime and return ISO format"""
    modified_datetime = original_datetime + timedelta(seconds=seconds_to_add)
    iso_modified = modified_datetime.isoformat()
    
    print(f"Time + {seconds_to_add} seconds (ISO): {iso_modified}")
    return modified_datetime

def token_time_expired(expire_date_utc):
    current_iso_datetime = datetime.now().astimezone()
    time_difference = current_iso_datetime - expire_date_utc
    # Check if the difference is positive (expired)
    if time_difference.total_seconds() > 0:
        print(f"Time Difference: {time_difference.total_seconds()}")
        return True
    else:
        print(f"Time Difference: {time_difference.total_seconds()}")
        return False

def main():
    """
    Example usage of the get_exact_token function
    """
    # Read refresh token, client_id, and client_secret from the saved JSON file
    refresh_token = None
    client_id = None
    client_secret = None
    
    try:
        with open('exact_token_response.json', 'r') as json_file:
            saved_data = json.load(json_file)
            refresh_token = saved_data.get('refresh_token')
            client_id = saved_data.get('client_id')
            client_secret = saved_data.get('client_secret')
            issue_date_utc = saved_data.get('issue_date_utc')
            expire_date_utc = saved_data.get('expire_date_utc')
            
            if not refresh_token:
                print("Error: No refresh_token found in exact_token_response.json")
                return
            if not client_id:
                print("Error: No client_id found in exact_token_response.json")
                return
            if not client_secret:
                print("Error: No client_secret found in exact_token_response.json")
                return
            if not issue_date_utc:
                print("Error: No issue_date_utc found in exact_token_response.json")
                return
            if not expire_date_utc:
                print("Error: No expire_date_utc found in exact_token_response.json")
                return
                
            print(f"Using refresh token, client_id, and client_secret from saved file")
            
                
    except FileNotFoundError:
        print("Error: exact_token_response.json file not found. Please run the program first to generate the file.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in exact_token_response.json")
        return
    except Exception as e:
        print(f"Error reading exact_token_response.json: {e}")
        return
    
    expire_date_utc_date = datetime.fromisoformat(expire_date_utc)
    result = None
    
    if token_time_expired(expire_date_utc_date):
        # Get new token
        result = get_exact_token(refresh_token, client_id, client_secret)
    else:
        print("Token not Expired Yet !!")
    
    if result:
        print("Token request successful!!")
        # print(f"New access token: {result.get('access_token', 'Not found')}")
        # print(f"Token type: {result.get('token_type', 'Not found')}")
        # print(f"Expires in: {result.get('expires_in', 'Not found')} seconds")
        print(f"New refresh token: {result.get('refresh_token', 'Not found')}")
        
        # Add client_id and client_secret to the result before saving
        result['client_id'] = client_id
        result['client_secret'] = client_secret

        #Add current iso datetime and expire datetime
        current_iso = get_current_timezone_iso().isoformat()
        expire_iso = add_seconds_to_iso(get_current_timezone_iso(), 600).isoformat()

        # Add iso date for the issue and expiry date
        result['issue_date_utc'] = current_iso
        result['expire_date_utc'] = expire_iso
        
        # Save the result to a JSON file
        try:
            with open('exact_token_response.json', 'w') as json_file:
                json.dump(result, json_file, indent=4)
        except Exception as e:
            print(f"Error saving to JSON file: {e}")
        
        # Create a copy in batch folder with timestamp
        try:
            # Create timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_filename = f"batch/exact_token_response_{timestamp}.json"
            
            with open(batch_filename, 'w') as batch_file:
                json.dump(result, batch_file, indent=4)
            print(f"Token response copied to batch folder: {batch_filename}")
        except Exception as e:
            print(f"Error saving to batch folder: {e}")
    else:
        print("Failed to get token")

if __name__ == "__main__":
    main()
