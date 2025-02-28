from telegram import Bot, Update
from telegram.ext import ContextTypes
import asyncio
import requests
from bs4 import BeautifulSoup
import os
import re
import json
import sqlite3
from datetime import datetime

# Telegram Bot API Token (replace with your actual token)
BOT_TOKEN = "7433012661:AAEEpp3NEoa6SKO3YhPNXBjAvbMB4EsgHDE"  # Placeholder token

# Your Amazon Referral Tag
REFERRAL_TAG = "your_referral_tag"

# Database file
DATABASE_FILE = "amazon_links.db"

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

def extract_asin(url):
    """Extracts the ASIN from an Amazon URL."""
    asin_pattern = r"/dp/([A-Z0-9]{10})|/gp/product/([A-Z0-9]{10})"
    match = re.search(asin_pattern, url)
    if match:
        return match.group(1) or match.group(2)
    return None

def store_link_data(asin, original_url, modified_url):
    """Stores the link data in the SQLite database, refreshing if older than 15 days."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS amazon_links (
                asin TEXT PRIMARY KEY,
                date TEXT,
                original_url TEXT,
                modified_url TEXT
            )
        """)

        # Check if the ASIN exists
        cursor.execute("SELECT date FROM amazon_links WHERE asin = ?", (asin,))
        result = cursor.fetchone()

        if result:
            # ASIN exists, check if it's older than 15 days
            last_update_date = datetime.fromisoformat(result[0])
            time_difference = datetime.now() - last_update_date
            if time_difference.days > 15:
                # Update the date
                cursor.execute("UPDATE amazon_links SET date = ?, original_url = ?, modified_url = ? WHERE asin = ?",
                               (datetime.now().isoformat(), original_url, modified_url, asin))
                print(f"ASIN {asin} updated in the database.")
            else:
                print(f"ASIN {asin} is not older than 15 days, skipping update.")
                conn.close()
                return

        else:
            # ASIN doesn't exist, insert new data
            cursor.execute("INSERT INTO amazon_links (asin, date, original_url, modified_url) VALUES (?, ?, ?, ?)",
                           (asin, datetime.now().isoformat(), original_url, modified_url))
            print(f"ASIN {asin} added to the database.")

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def process_message(bot: Bot, text: str, chat_id: int):
    """
    Processes a message, identifies Amazon links, and sends back the modified message.
    """
    logging.info(f"Received message: {text} from chat ID: {chat_id}")
    print(f"Received message: {text} from chat ID: {chat_id}")

    # Regex to find Amazon shortened links (e.g., amzn.to/xxxx)
    amazon_link_pattern = r"https?:\/\/amzn\.to\/[a-zA-Z0-9]+"
    
    amazon_links = re.findall(amazon_link_pattern, text)

    modified_text = text  # Start with the original text
    
    for link in amazon_links:
        modified_link = modify_amazon_link(link)
        if modified_link:
            shortened_link = shorten_url(modified_link)  # Shorten the modified link
            modified_text = modified_text.replace(link, shortened_link)  # Replace the original link with the shortened link
            
            # Extract ASIN and store data
            asin = extract_asin(modified_link)
            if asin:
                store_link_data(asin, link, modified_link)
            else:
                print(f"Could not extract ASIN from: {modified_link}")

        else:
            print(f"Could not process the Amazon link: {link}") # Log the error

    # Only send a response if the text was modified
    if modified_text != text:
        await bot.send_message(chat_id=chat_id, text=modified_text)

async def main():
    """
    Main function to start the bot.
    """
    bot = Bot(token=BOT_TOKEN)
    
    # Get bot info to verify the token is valid
    print("Starting bot...")
    bot_info = await bot.get_me()
    print(f"Bot started as @{bot_info.username}")
    
    # Simple polling mechanism
    offset = 0
    
    try:
        while True:
            updates = await bot.get_updates(offset=offset, timeout=30)
            print(f"Received updates: {updates}")
             
            for update in updates:
                print(f"Processing update with ID: {update.update_id}")
                offset = update.update_id + 1
                
                # Process only text messages
                if update.message and update.message.text:
                    await process_message(
                        bot,
                        update.message.text,
                        update.message.chat_id
                    )
                else:
                    print("Received non-text message, skipping...")
            # Small delay to prevent high CPU usage
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())