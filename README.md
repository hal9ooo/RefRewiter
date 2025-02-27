# Amazon Referral Rewriter

## Description

The Amazon Referral Rewriter is a Python-based Telegram bot that automatically modifies Amazon reseller links in a Telegram channel, replacing the original referral tag with your own. It also shortens the modified links using the TinyURL API, making them more presentable.

## Features

*   **Automatic Referral Tag Replacement:** Replaces the referral tag in Amazon links with your specified tag.
*   **Link Shortening:** Uses the TinyURL API to shorten the modified Amazon links.
*   **Message Preservation:** Outputs the same message it received, but with the Amazon links replaced with the modified and shortened versions.
*   **Easy Setup:** Simple installation and configuration process.

## Prerequisites

*   Python 3.6 or higher
*   Telegram Bot API token

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository_url]
    cd amazon-referral-rewriter
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   On Windows:

        ```bash
        venv\Scripts\activate
        ```

    *   On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Install the required libraries:**

    ```bash
    pip install requests beautifulsoup4 python-telegram-bot
    ```

## Configuration

1.  **Obtain a Telegram Bot API token:**

    *   Talk to the BotFather on Telegram (@BotFather).
    *   Use the `/newbot` command to create a new bot.
    *   Follow the instructions to choose a name and username for your bot.
    *   BotFather will provide you with an API token.

2.  **Configure the `bot.py` file:**

    *   Open the `bot.py` file in a text editor.
    *   Replace `"your_random_token_here"` with your actual Telegram Bot API token.
    *   Ensure that the `REFERRAL_TAG` variable is set to your Amazon referral tag (default: `"lanjpoiwer123"`).

## Usage

1.  **Run the bot:**

    ```bash
    python bot.py
    ```

2.  **Add the bot to your Telegram channel:**

    *   Add the bot as an administrator to the Telegram channel where you want it to modify Amazon links.
    *   Ensure that the bot has the necessary permissions to read messages and send messages.

3.  **Send messages containing Amazon links to the channel:**

    *   The bot will automatically identify Amazon links, replace the referral tag, shorten the links, and output the entire message with the modified links.

## Example

**Input Message:**

```
Check out this awesome product on Amazon! https://amzn.to/abcd
```

**Output Message:**

```
Check out this awesome product on Amazon! http://tinyurl.com/xxxx
```

## Error Handling

The bot includes basic error handling to catch potential issues like invalid links or network errors. If an error occurs, it will be logged to the console.

## Potential Improvements

*   **More Robust Link Detection:** Improve the link detection regex to handle a wider variety of Amazon link formats.
*   **Configuration File:** Move the bot's configuration (API token, referral tag) to a separate configuration file.
*   **Logging:** Implement more comprehensive logging to track the bot's activity and errors.
*   **Customizable Shortener:** Allow the user to choose a different link shortener service.
*   **Asynchronous Operations:** Use asynchronous operations to improve the bot's performance.

## License

[Choose a license, e.g., MIT License]