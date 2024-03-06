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

Create a `.env` file in the root directory of the project and add your Reddit API credentials and other configurations as follows:

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
