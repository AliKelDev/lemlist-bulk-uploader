# Lemlist Bulk Campaign Manager

Python scripts to automate Lemlist campaign creation and lead uploads via the Lemlist API.

## Features

- **Create Multiple Campaigns**: Bulk create campaigns with custom names
- **Upload Leads in Bulk**: Add leads to campaigns from a CSV file
- **Custom Variables**: Support for personalized opening lines and other custom fields
- **Error Handling**: Robust validation and error reporting
- **Rate Limiting**: Respectful API usage with built-in delays

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install requests python-dotenv
```

### 2. Configure API Key

```bash
cp .env.example .env
```

Edit `.env` and add your Lemlist API key:
```
LEMLIST_API_KEY=your_api_key_here
```

Get your API key from: https://app.lemlist.com/settings/integrations

### 3. Prepare Your Data

Edit `Prospects.csv` with your lead data. The file includes example entries with fictional data to show you the required format.

## Usage

### Creating Campaigns

1. Edit `createsequence.py` and modify the `campaign_names` list
2. Run the script:
```bash
python createsequence.py
```
3. Note the campaign IDs returned - you'll need these for uploading leads

### Uploading Leads

1. Ensure your CSV file has the required columns:
   - `email` (required)
   - `firstName` (required)
   - `lastName` (optional)
   - `companyName` (optional)
   - `campaignId` (required - from step above)
   - `customOpeningLine` (required)

2. **Important**: Create the `customOpeningLine` variable in your Lemlist campaign:
   - Go to your campaign in Lemlist
   - Settings → Variables
   - Add custom variable named exactly `customOpeningLine`

3. Run the upload script:
```bash
python launch_campaign.py
```

## CSV Format

See `Prospects.csv` for the required format (includes example data):

```csv
email,firstName,lastName,companyName,campaignId,customOpeningLine
john.doe@example.com,John,Doe,Example Corp,cam_ABC123xyz,"Your personalized opening line here"
```

## Scripts

- **createsequence.py**: Creates multiple campaigns in Lemlist
- **launch_campaign.py**: Uploads leads from CSV to their respective campaigns

## API Documentation

- [Lemlist API Docs](https://developer.lemlist.com/)
- [Create Campaign](https://developer.lemlist.com/#create-a-campaign)
- [Add Lead to Campaign](https://developer.lemlist.com/#add-a-lead-in-a-campaign)

## Security Notes

- Never commit your `.env` file with real API keys
- The `.gitignore` is configured to exclude the `.env` file
- Always use environment variables for API keys
- Replace the example data in `Prospects.csv` with your actual leads before running

## License

MIT