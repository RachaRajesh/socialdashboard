import requests
from requests_oauthlib import OAuth1
from config import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_BEARER_TOKEN,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    FACEBOOK_ACCESS_TOKEN,
    FACEBOOK_PAGE_ID,
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_USER_ID
)
from .models import Post, User

# Ensure default user exists
default_user = User.get(User.username == "default_user")

# Twitter: Fetch metrics for a specific tweet with debugging
def get_twitter_metrics(tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    params = {"tweet.fields": "public_metrics"}
    
    response = requests.get(url, headers=headers, params=params)
    print(f"API Response: {response.json()}")  # Debugging: Print API response
    
    if response.status_code != 200:
        return {"error": response.json()}
    
    data = response.json().get("data", {})
    metrics = data.get("public_metrics", {})
    print(f"Parsed Metrics: {metrics}")  # Debugging: Print parsed metrics
    
    return {
        "id": tweet_id,
        "content": data.get("text", "Unknown"),
        "likes": metrics.get("like_count", 0),
        "retweets": metrics.get("retweet_count", 0),
        "views": metrics.get("impression_count", 0)
    }

# Twitter: Post a tweet using OAuth 1.0a
def post_tweet(content):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET,
    )
    payload = {"text": content}
    response = requests.post(url, json=payload, auth=auth)
    if response.status_code != 201:
        return {"error": response.json()}
    data = response.json()
    tweet_id = data.get("data", {}).get("id")
    tweet_url = f"https://twitter.com/user/status/{tweet_id}" if tweet_id else None

    # Save to database using default user
    if tweet_id:
        Post.create(user=default_user, platform="twitter", content=content, post_link=tweet_url)

    return {"tweet_id": tweet_id, "tweet_url": tweet_url}

# Facebook: Post content to a page
def post_to_facebook(content):
    url = f"https://graph.facebook.com/v15.0/{FACEBOOK_PAGE_ID}/feed"
    params = {
        "message": content,
        "access_token": FACEBOOK_ACCESS_TOKEN,
    }
    response = requests.post(url, params=params)
    
    if response.status_code != 200:
        return {"error": response.json()}
    
    post_id = response.json().get("id")
    if post_id:
        page_id, post_id_only = post_id.split('_')
        post_link = f"https://www.facebook.com/{page_id}/posts/{post_id_only}"
        # Save the post to the database using default user
        Post.create(user=default_user, platform="facebook", content=content, post_link=post_link)
    else:
        post_link = None

    return {"post_id": post_id, "post_link": post_link}

# Facebook : Metrics of facebook posts

def get_facebook_metrics(post_id):
    url = f"https://graph.facebook.com/v15.0/{post_id}/insights"
    params = {
        "metric": "post_impressions,post_engaged_users",
        "access_token": FACEBOOK_ACCESS_TOKEN,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {"error": response.json()}

    data = response.json().get("data", [])
    metrics = {item["name"]: item["values"][0]["value"] for item in data}
    return metrics


# Facebook: Fetch recent posts from the page
def get_facebook_posts():
    url = f"https://graph.facebook.com/v15.0/{FACEBOOK_PAGE_ID}/posts"
    params = {"access_token": FACEBOOK_ACCESS_TOKEN}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": response.json()}
    
    return response.json().get("data", [])


# Instagram: Post content

def post_to_instagram(content, image_url=None):
    # Step 1: Create media
    print("Creating Instagram media...")
    create_url = f"https://graph.facebook.com/v15.0/{INSTAGRAM_USER_ID}/media"
    create_params = {
        "caption": content,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    if image_url:
        create_params["image_url"] = image_url

    create_response = requests.post(create_url, params=create_params)
    print(f"Create response: {create_response.json()}")

    if create_response.status_code != 200:
        return {"error": create_response.json()}

    creation_id = create_response.json().get("id")
    if not creation_id:
        return {"error": "Failed to create media."}

    # Step 2: Publish the media
    print("Publishing Instagram media...")
    publish_url = f"https://graph.facebook.com/v15.0/{INSTAGRAM_USER_ID}/media_publish"
    publish_params = {
        "creation_id": creation_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    publish_response = requests.post(publish_url, params=publish_params)
    print(f"Publish response: {publish_response.json()}")

    if publish_response.status_code != 200:
        return {"error": publish_response.json()}

    post_id = publish_response.json().get("id")
    if not post_id:
        return {"error": "Failed to publish media."}

    # Step 3: Fetch the permalink
    print("Fetching permalink...")
    post_details_url = f"https://graph.facebook.com/v15.0/{post_id}"
    post_details_params = {
        "fields": "permalink",
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    post_details_response = requests.get(post_details_url, params=post_details_params)
    print(f"Post details response: {post_details_response.json()}")

    if post_details_response.status_code != 200:
        return {"error": post_details_response.json()}

    permalink = post_details_response.json().get("permalink")
    if not permalink:
        return {"error": "Failed to fetch permalink."}

    # Step 4: Save to the database
    try:
        Post.create(
            user=default_user,
            platform="instagram",
            content=content,
            post_link=permalink,
        )
        print("Instagram post saved successfully.")
    except Exception as e:
        print(f"Error saving to database: {str(e)}")

    return {
        "status": "Post created successfully",
        "post_id": post_id,
        "post_link": permalink,
    }

# Instagram: Fetch metrics
def get_instagram_metrics(post_id):
    url = f"https://graph.facebook.com/v15.0/{post_id}/insights"
    params = {
        "metric": "impressions,reach,likes",
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {"error": response.json()}

    data = response.json().get("data", [])
    metrics = {item["name"]: item["values"][0]["value"] for item in data}
    return metrics
