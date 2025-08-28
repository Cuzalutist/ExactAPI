import requests
import json
import webbrowser
import os
from urllib.parse import urlparse, parse_qs
import time

def get_exact_oauth_response():
    """
    Get response from Exact Online OAuth2 authentication URL
    """
    # OAuth2 authentication URL
    oauth_url = "https://start.exactonline.nl/api/oauth2/auth"
    
    # Query parameters
    params = {
        'client_id': '8059c106-9dac-4e8a-8611-937adfcae815',
        'redirect_uri': 'https://vrb.rijsoort.nl/',
        'response_type': 'code',
        'force_login': '0'
    }
    
    try:
        print("Making GET request to Exact Online OAuth2 endpoint...")
        print(f"URL: {oauth_url}")
        print(f"Parameters: {params}")
        print("-" * 50)
        
        # Make GET request
        response = requests.get(oauth_url, params=params, timeout=30)
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response URL: {response.url}")
        print("-" * 50)
        
        # Check if request was successful
        if response.status_code == 200:
            print("Request successful! HTML login page received.")
            print("Response Content Preview:")
            print(response.text[:500])  # Print first 500 characters
            
            # Open HTML response directly in browser using data URL
            print("\nOpening login page in browser...")
            import base64
            html_data = base64.b64encode(response.text.encode('utf-8')).decode('utf-8')
            data_url = f'data:text/html;base64,{html_data}'
            webbrowser.open(data_url)
            
            # Wait for user to complete login
            print("\n" + "="*60)
            print("PLEASE COMPLETE THE LOGIN PROCESS IN THE BROWSER")
            print("After login, copy the final URL from the browser address bar")
            print("="*60)
            
            # Get final URL from user
            final_url = input("\nEnter the final URL from browser after login (or press Enter to skip): ").strip()
            
            if final_url:
                # Save final URL to file
                with open('final_response_url.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Final URL after login: {final_url}\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                print(f"\nFinal URL saved to 'final_response_url.txt'")
                
                # Parse the final URL for authorization code
                try:
                    parsed_url = urlparse(final_url)
                    query_params = parse_qs(parsed_url.query)
                    
                    if 'code' in query_params:
                        auth_code = query_params['code'][0]
                        print(f"Authorization Code found: {auth_code}")
                        
                        # Save authorization code
                        with open('auth_code.txt', 'w') as f:
                            f.write(auth_code)
                        print("Authorization code saved to 'auth_code.txt'")
                    else:
                        print("No authorization code found in final URL")
                        
                except Exception as e:
                    print(f"Error parsing final URL: {e}")
            else:
                print("No final URL provided.")
            
        elif response.status_code == 302:
            print("Redirect response detected!")
            redirect_url = response.headers.get('Location')
            if redirect_url:
                print(f"Redirect URL: {redirect_url}")
                
                # Save redirect URL
                with open('redirect_url.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Redirect URL: {redirect_url}\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print("Redirect URL saved to 'redirect_url.txt'")
                
                # Parse redirect URL for authorization code
                parsed_url = urlparse(redirect_url)
                query_params = parse_qs(parsed_url.query)
                
                if 'code' in query_params:
                    auth_code = query_params['code'][0]
                    print(f"Authorization Code: {auth_code}")
                    
                    # Save authorization code
                    with open('auth_code.txt', 'w') as f:
                        f.write(auth_code)
                    print("Authorization code saved to 'auth_code.txt'")
                else:
                    print("No authorization code found in redirect URL")
                    
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def save_response_to_json(response):
    """
    Save response details to JSON file
    """
    if response is None:
        return
    
    response_data = {
        'status_code': response.status_code,
        'url': response.url,
        'headers': dict(response.headers),
        'content_length': len(response.content),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save to JSON file
    with open('response_details.json', 'w', encoding='utf-8') as f:
        json.dump(response_data, f, indent=2, ensure_ascii=False)
    
    print("Response details saved to 'response_details.json'")

if __name__ == "__main__":
    print("Exact Online OAuth2 Response Getter")
    print("=" * 40)
    
    # Get response from OAuth2 endpoint
    response = get_exact_oauth_response()
    
    # Save response details to JSON
    save_response_to_json(response)
    
    print("\nProgram completed!")
