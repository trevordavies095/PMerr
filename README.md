# PMerr

This Python script checks for unread Private Messages (PMs) from Gazelle-based trackers and sends notifications to a specified Discord channel via a webhook.

## How It Works

The script uses the Gazelle API's `ajax.php?action=inbox` endpoint to fetch your private messages and checks for unread messages received within the last 60 seconds. If any are found, the script sends a notification to a Discord channel using a webhook.

### Requirements
- The tracker must expose the following endpoints:
  - `ajax.php?action=inbox` - to retrieve messages.
  - `inbox.php?action=viewconv&id=` - to view individual conversations.
  
- You need a Discord webhook URL for posting notifications.

## Getting Started

### Prerequisites

1. **Python 3.x** installed.
2. Install the required dependencies:

   ```bash
   pip install requests discord-webhook
   ```

### Configuration

1. **Gazelle Tracker API Details**:
   Add your tracker details in the `api_sources` list inside the script, including:
   - `name`: The name of the tracker.
   - `base_url`: The base URL of the tracker.
   - `inbox_endpoint`: The API endpoint for fetching private messages (usually `ajax.php?action=inbox`).
   - `api_key`: Your tracker API key.

2. **Discord Webhook URL**:
   Set your Discord webhook URL in the `DISCORD_WEBHOOK_URL` variable inside the `if __name__ == "__main__":` block.

   Example:
   
   ```python
   DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
   ```

### Running the Script

Run the script using Python:

```bash
python gazelle_pm_notifier.py
```

### Example Notification

The bot sends a message to the configured Discord channel with the following details:
- PM subject
- Link to the conversation on the tracker
- Tracker source

### Customization

You can add as many Gazelle-based trackers as you'd like by extending the `api_sources` list with more entries.

## Contributing

Feel free to submit issues or pull requests for improvements.

## License

This project is licensed under the MIT License.
