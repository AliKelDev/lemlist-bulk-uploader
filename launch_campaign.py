"""
Lemlist Bulk Lead Uploader
--------------------------
This script uploads leads from a CSV file to their respective Lemlist campaigns.

SETUP:
1. Copy .env.example to .env
2. Add your Lemlist API key to .env (get it from: https://app.lemlist.com/settings/integrations)
3. Prepare your CSV file with the required columns (see Prospects.csv.example)
4. Update CSV_FILE_PATH below if your file has a different name
5. Run: python launch_campaign.py

CSV FORMAT REQUIRED:
- email: Lead's email address (required)
- firstName: Lead's first name (required)
- lastName: Lead's last name (optional)
- companyName: Lead's company (optional)
- campaignId: The Lemlist campaign ID to add this lead to (required)
- customOpeningLine: Your personalized opening line (required)

IMPORTANT: The 'customOpeningLine' variable must be created in your Lemlist campaign settings first.
Go to your campaign → Settings → Variables → Add custom variable named exactly "customOpeningLine"

API Documentation: https://developer.lemlist.com/#add-a-lead-in-a-campaign
"""

import requests
import base64
import json
import os
import csv
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ------------------- CONFIGURATION -------------------
API_KEY = os.getenv("LEMLIST_API_KEY")

# Path to your CSV file containing lead data
# Modify this if your CSV file has a different name
CSV_FILE_PATH = "Prospects.csv"
# -----------------------------------------------------

# Validation: Ensure required configuration is present
if not API_KEY:
    print("FATAL ERROR: LEMLIST_API_KEY not found in .env file.")
    print("Please create a .env file with your API key (see .env.example)")
    exit()

if not os.path.exists(CSV_FILE_PATH):
    print(f"FATAL ERROR: CSV file not found at '{CSV_FILE_PATH}'")
    print("Please create your CSV file with lead data (see Prospects.csv.example for format)")
    exit()

# Lemlist API endpoint template for adding leads to campaigns
ENDPOINT_TEMPLATE = "https://api.lemlist.com/api/campaigns/{campaignId}/leads"

# Prepare authentication headers
# Lemlist uses Basic Authentication with the API key as password (username is empty)
credentials = f":{API_KEY}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json"
}

print("--- Starting Lemlist Lead Upload ---\n")

# Process CSV file and upload each lead
with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Track statistics
    total_processed = 0
    successful = 0
    failed = 0

    for i, row in enumerate(csv_reader):
        # Extract data from CSV row
        email = row.get("email")
        first_name = row.get("firstName")
        last_name = row.get("lastName")
        company_name = row.get("companyName")
        campaign_id = row.get("campaignId")
        custom_line = row.get("customOpeningLine")

        # Validate required fields
        if not all([email, first_name, campaign_id, custom_line]):
            print(f"⚠ SKIPPING ROW {i+2}: Missing required fields (email, firstName, campaignId, or customOpeningLine)")
            failed += 1
            continue

        total_processed += 1
        print(f"[{total_processed}] Processing: {email} → Campaign: {campaign_id}")

        # Build API endpoint for this campaign
        endpoint = ENDPOINT_TEMPLATE.format(campaignId=campaign_id)

        # Construct payload with lead data
        payload = {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "companyName": company_name,
            # Custom variables are merged into the campaign template
            # Variable names must match exactly what you created in Lemlist campaign settings
            "customVariables": {
                "customOpeningLine": custom_line
            }
        }

        # Upload lead to Lemlist
        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raises exception for 4xx/5xx status codes

            print(f"  ✓ SUCCESS: Lead added to campaign\n")
            successful += 1

        except requests.exceptions.RequestException as e:
            print(f"  ✗ ERROR: Failed to add lead")
            if e.response is not None:
                print(f"  Status Code: {e.response.status_code}")
                print(f"  Response: {e.response.text}")
            else:
                print(f"  Exception: {e}")
            print()
            failed += 1

        # Rate limiting: Add delay between requests to respect API limits
        time.sleep(0.5)

# Print summary
print("\n--- Upload Complete ---")
print(f"Total processed: {total_processed}")
print(f"Successful: {successful}")
print(f"Failed: {failed}")