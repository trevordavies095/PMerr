from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import html
import pytz
import requests

# Define your API sources in a dictionary
api_sources = [
    {
        "name": "",
        "base_url": "",
        "inbox_endpoint": "",
        "api_key": ""
    }
    # Add more API sources as needed
]

# Function to fetch data from the API
def fetch_inbox_messages(base_url, inbox_endpoint, api_key):
    headers = {
        'Authorization': api_key,  # Assuming a Bearer token; adjust based on API
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{base_url}{inbox_endpoint}", headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()["response"]["messages"]  # Return parsed JSON data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {base_url}: {e}")
        return None

# Function to send a message to Discord
def post_to_discord(webhook_url, source_name, message, message_url):
    webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
    embed = DiscordEmbed(description=html.unescape(message["subject"]), color="03b2f8")

    embed.set_author(name=f"New {source_name} PM!", url=message_url)
    webhook.add_embed(embed)
    webhook.execute()

# Main function to fetch data from multiple APIs and post to Discord
def process_inbox_messages(api_sources, webhook_url):
    # Set both server and message time zones to UTC
    utc_tz = pytz.timezone('UTC')
    current_time = datetime.now(utc_tz)

    for source in api_sources:
        # Fetch inbox messages from the API
        messages = fetch_inbox_messages(source['base_url'], source['inbox_endpoint'], source['api_key'])

        # If there are messages, process each one
        if messages:
            for message in messages:
                # Check if the message is unread and was received within the last minute
                msg_received_time = datetime.strptime(message["date"], "%Y-%m-%d %H:%M:%S")
                msg_received_time = utc_tz.localize(msg_received_time)

                # Calculate the time difference in seconds (now both are timezone-aware)
                time_diff = (current_time - msg_received_time).total_seconds()

                if message["unread"] and time_diff <= 60:
                    message_url = f"{source['base_url']}inbox.php?action=viewconv&id={message['convId']}"

                    # Send the message details to Discord
                    post_to_discord(webhook_url, source['name'], message, message_url)

if __name__ == "__main__":
    # Replace this with your Discord webhook URL
    DISCORD_WEBHOOK_URL = ""
    
    # Call the main function with your API sources and webhook
    process_inbox_messages(api_sources, DISCORD_WEBHOOK_URL)
