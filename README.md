# Reddit Image Downloader

This project is a Python script that automates the downloading of image posts from specified subreddits using the Reddit API. It supports fetching images from various listing types (hot, new, top, rising, controversial) and time filters for the 'top' and 'controversial' listings (day, week, month, year, all). The script ensures that only new images are downloaded by keeping track of previously processed posts.

## Features

- Download images from specific subreddits
- Supports various listings and time filters
- Avoids re-downloading images by tracking processed posts
- Graceful shutdown handling

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- PRAW (Python Reddit API Wrapper)
- Requests library
- dotenv library for environment variable management

## Installation

To install the required Python libraries, run the following command:

pip install praw requests python-dotenv


## Configuration

To configure the Reddit Image Downloader, you will need to obtain your Reddit API credentials and create a `.env` file to securely store these credentials. Follow the steps below:

### Step 1: Obtaining Reddit API Credentials

1. Log in to your Reddit account.
2. Go to [the Reddit app creation page](https://www.reddit.com/prefs/apps).
3. Click on the "create app" or "create another app" button at the bottom.
4. Fill out the form:
   - **name:** Your application's name.
   - **application type:** Choose "script".
   - **description:** (Optional) A brief description of your application.
   - **about url:** (Optional)
   - **permissions:** (Optional)
   - **redirect uri:** Use `http://localhost:8080` for a script application.
5. Click "create app" or "update app" to save your changes.

After creating the app, you will be provided with a `client_id` and a `client_secret`. Note these down as you will need them for your `.env` file.

### Step 2: Creating a .env File

1. In the root directory of your project, create a new file named `.env`.
2. Open the `.env` file with a text editor of your choice.
3. Add your Reddit API credentials to the file in the following format:



REDDIT_CLIENT_ID=your_client_id_here

REDDIT_CLIENT_SECRET=your_client_secret_here

REDDIT_USERNAME=your_reddit_username_here

REDDIT_PASSWORD=your_reddit_password_here



## Usage

To use the Reddit Image Downloader, follow these steps:

1. Modify the `subreddit_name` variable in the script to the subreddit you wish to download images from.
2. Adjust the `listings` and `top_time_filters` variables if necessary to specify the listings and time filters you're interested in.
3. Run the script with:

python scraper.py

The script will start downloading images to the `output` directory, organizing them by subreddit name.

Make sure you replace the placeholder text (like your_client_id_here, your_reddit_username_here, etc.) with your actual Reddit API credentials and other specific details. 
