import os
import praw
import requests
import signal
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Setup Reddit API Credentials from environment variables
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
username = os.getenv('REDDIT_USERNAME')
password = os.getenv('REDDIT_PASSWORD')

# Initialize Reddit client with PRAW
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='platform:appID:versionString (by /u/yourRedditUsername)',
                     username=username,
                     password=password,
                     requestor_kwargs={'timeout': 30})

def get_image_posts(subreddit_name, processed_posts, listing='top', time_filter='all'):
    """
    Generator function to get image posts from a subreddit.
    
    :param subreddit_name: Name of the subreddit
    :param processed_posts: Set of post IDs that have been processed
    :param listing: Type of listing to fetch (e.g., 'hot', 'new', 'top')
    :param time_filter: Time filter for posts (e.g., 'day', 'week', 'month')
    :yield: posts with images
    """
    subreddit = reddit.subreddit(subreddit_name)
    posts_method = {'hot': subreddit.hot, 'new': subreddit.new, 'top': subreddit.top,
                    'rising': subreddit.rising, 'controversial': subreddit.controversial}
    if listing in ['top', 'controversial']:
        posts = posts_method[listing](time_filter=time_filter, limit=None)
    else:
        posts = posts_method[listing](limit=None)
    
    for post in posts:
        if post.id not in processed_posts and post.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            yield post

def sanitize_filename(filename):
    """
    Sanitizes the filename by removing or replacing characters that are invalid for file names.
    
    :param filename: Original filename
    :return: Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_image(image_url, timeout=10):
    """
    Attempts to download an image from the provided URL.
    
    :param image_url: URL of the image to download
    :param timeout: Timeout in seconds for the network request
    :return: Content of the image if successful, None otherwise
    """
    try:
        response = requests.get(image_url, stream=True, allow_redirects=False, timeout=timeout)
        if response.status_code == 200 and 'image/' in response.headers['Content-Type']:
            return response.content
        elif response.status_code in [301, 302, 303, 307]:
            print(f"Image has been removed or is unavailable: {image_url}")
        else:
            print(f"Failed to download or not an image {image_url}, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_url}: {e}")
    return None

def download_images(posts, output_dir, processed_posts_file):
    """
    Downloads images from a list of posts, ensuring they haven't been processed before.
    
    :param posts: Iterable of posts to process
    :param output_dir: Directory where images will be saved
    :param processed_posts_file: File storing IDs of processed posts
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    processed_posts = load_processed_posts(processed_posts_file)
    downloaded_count = 0

    for post in posts:
        if post.id in processed_posts:
            continue

        image_url = post.url
        image_filename = image_url.split("/")[-1]
        image_filename = sanitize_filename(image_filename)
        image_name = os.path.join(output_dir, image_filename)

        if not os.path.exists(image_name):
            content = download_image(image_url)
            if content:
                with open(image_name, 'wb') as f:
                    f.write(content)
                downloaded_count += 1
                print(f"Downloaded: {image_name}")

        processed_posts.add(post.id)
        save_processed_posts(processed_posts, processed_posts_file)  # Save after each post is processed

    print(f"Total images downloaded: {downloaded_count}")

def save_processed_posts(processed_posts, filename):
    """
    Saves IDs of processed posts to a file.
    
    :param processed_posts: Set of post IDs that have been processed
    :param filename: File to save the IDs to
    """
    with open(filename, 'w') as file:
        for post_id in processed_posts:
            file.write(post_id + '\n')

def load_processed_posts(filename):
    """
    Loads IDs of previously processed posts from a file.
    
    :param filename: File containing the IDs
    :return: Set of post IDs
    """
    if not os.path.exists(filename):
        return set()
    with open(filename, 'r') as file:
        return set(file.read().splitlines())

# Graceful shutdown handler to ensure the program can be interrupted
def graceful_shutdown(signum, frame):
    print("\nGracefully shutting down...")
    os._exit(0)

# Attach signal handlers for graceful shutdown
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

def fetch_and_download(subreddit_name, listing, time_filter=None):
    """
    Orchestrates the fetching and downloading of images from a subreddit.
    
    :param subreddit_name: Name of the subreddit to process
    :param listing: Type of listing to fetch
    :param time_filter: Time filter for the listing
    """
    output_dir = os.path.join('output', subreddit_name)
    processed_posts_file = f'{subreddit_name}_processed_posts.txt'
    processed_posts = load_processed_posts(processed_posts_file)
    posts = get_image_posts(subreddit_name, processed_posts, listing=listing, time_filter=time_filter)
    download_images(posts, output_dir, processed_posts_file)
    print(f"Completed downloading for {listing} listing {'' if not time_filter else 'for ' + time_filter}.")

if __name__ == "__main__":
    subreddit_name = "EnterSubredditNameHere"  # Example subreddit name for demonstration purposes
    
    listings = ['hot', 'new', 'rising']
    top_time_filters = ['day', 'week', 'month', 'year', 'all']

    for listing in listings:
        fetch_and_download(subreddit_name, listing)
    
    for time_filter in top_time_filters:
        fetch_and_download(subreddit_name, 'top', time_filter=time_filter)
        fetch_and_download(subreddit_name, 'controversial', time_filter=time_filter)
    
    print("Images downloaded successfully from all listings and time filters!")
