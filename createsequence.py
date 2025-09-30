"""
Lemlist Campaign Creator
------------------------
This script creates multiple campaigns in your Lemlist account via the API.

SETUP:
1. Copy .env.example to .env
2. Add your Lemlist API key to .env (get it from: https://app.lemlist.com/settings/integrations)
3. Modify the campaign_names list below with your desired campaign names
4. Run: python createsequence.py

API Documentation: https://developer.lemlist.com/#create-a-campaign
"""

import requests
import base64
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ------------------- CONFIGURATION -------------------
# Your Lemlist API key (loaded from .env file)
API_KEY = os.getenv("LEMLIST_API_KEY")

# Modify this list with the campaign names you want to create
# Each campaign will be created sequentially
campaign_names = [
    "FR - jMON - Persona A - C-Suite & Executive",
    "FR - jMON - Persona B - Security Leadership",
    "FR - jMON - Persona C - DevOps & Engineering"
]
# -----------------------------------------------------

# Validation: Ensure API key exists before proceeding
if not API_KEY:
    print("FATAL ERROR: LEMLIST_API_KEY not found in .env file or environment.")
    print("Please create a .env file and add the line: LEMLIST_API_KEY='your_key_here'")
    exit()

# Lemlist API endpoint for campaign creation
ENDPOINT = "https://api.lemlist.com/api/campaigns"

# Prepare authentication headers
# Lemlist uses Basic Authentication with the API key as password (username is empty)
credentials = f":{API_KEY}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json"
}

print("--- Starting Lemlist Campaign Creation ---\n")

# Create each campaign sequentially
for name in campaign_names:
    print(f"Creating campaign: '{name}'...")

    # API payload - only name is required, other settings configured in Lemlist UI
    payload = {
        "name": name
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes

        # Parse response and extract campaign ID
        created_campaign = response.json()
        campaign_id = created_campaign.get('_id')
        print(f"  ✓ SUCCESS: Campaign created with ID: {campaign_id}\n")

    except requests.exceptions.RequestException as e:
        print(f"  ✗ ERROR: Failed to create campaign '{name}'")
        print(f"  Exception: {e}")
        if e.response:
             print(f"  Status Code: {e.response.status_code}")
             print(f"  Response: {e.response.text}")
        print()

print("--- Campaign creation complete ---")