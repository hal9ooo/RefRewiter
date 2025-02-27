import telegram
from telegram.ext import Updater, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import os
import re
import json

# Telegram Bot API Token (replace with your actual token)
BOT_TOKEN = "your_api_token_here"  # Placeholder token

# Your Amazon Referral Tag
REFERRAL_TAG = "your_referral_tag"

def shorten_url(url):
    """Shortens a URL using the TinyURL API."""
    api_url = f"http://tinyurl.com/api-create.php?url={url}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error shortening URL: {e}")
        return url  # Return original URL on error

def modify_amazon_link(link):
    """
    Opens the Amazon link, replaces the referral tag, and returns the modified link.
    """
    try:
        response = requests.get(link)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the original URL (handle different redirect methods)
        original_url = response.url
        
        # Use regex to find and replace the referral tag
        modified_url = re.sub(r"tag=[^&]+", f"tag={REFERRAL_TAG}", original_url)
        
        return modified_url

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def handle_message(update, context):
    """
    Handles incoming messages, identifies Amazon links, and replaces them with shortened, modified links in the original message.
    """
    text = update.message.text
    
    # Regex to find Amazon shortened links (e.g., amzn.to/xxxx)
    amazon_link_pattern = r"https?:\/\/amzn\.to\/[a-zA-Z0-9]+"
    
    amazon_links = re.findall(amazon_link_pattern, text)

    modified_text = text  # Start with the original text
    
    for link in amazon_links:
        modified_link = modify_amazon_link(link)
        if modified_link:
            shortened_link = shorten_url(modified_link)  # Shorten the modified link
            modified_text = modified_text.replace(link, shortened_link)  # Replace the original link with the shortened link
        else:
            print(f"Could not process the Amazon link: {link}") # Log the error

    update.message.reply_text(modified_text)  # Send the modified message


def main():
    """
    Main function to start the bot.
    """
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add message handler to process text messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()