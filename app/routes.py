from flask import Blueprint, render_template, request
from .services import post_tweet, get_twitter_metrics, post_to_facebook, get_facebook_posts, get_facebook_metrics, post_to_instagram, get_instagram_metrics

bp = Blueprint("routes", __name__)

# Home route
@bp.route("/")
def index():
    return render_template("index.html")

# Twitter route
@bp.route("/twitter", methods=["GET", "POST"])
def twitter():
    tweet_response = None
    metrics = None

    if request.method == "POST":
        if "tweet_content" in request.form:
            tweet_content = request.form["tweet_content"]
            tweet_response = post_tweet(tweet_content)
        elif "tweet_id" in request.form:
            tweet_id = request.form["tweet_id"]
            metrics = get_twitter_metrics(tweet_id)

    return render_template("twitter.html", tweet_response=tweet_response, metrics=metrics)

# Facebook route
@bp.route("/facebook", methods=["GET", "POST"])
def facebook():
    fb_response = None
    fb_metrics = None
    posts = get_facebook_posts()

    if request.method == "POST":
        fb_content = request.form["fb_content"]
        fb_response = post_to_facebook(fb_content)

    post_id = request.args.get("post_id")
    
    if post_id:
        fb_metrics = get_facebook_metrics(post_id)

    return render_template("facebook.html", fb_response=fb_response, fb_metrics=fb_metrics, posts=posts)

#instagram

@bp.route("/instagram", methods=["GET", "POST"])
def instagram():
    instagram_response = None
    instagram_metrics = None

    if request.method == "POST":
        content = request.form["ig_content"]
        image_url = request.form.get("ig_image_url", None)
        instagram_response = post_to_instagram(content, image_url)

    post_id = request.args.get("post_id")
    if post_id:
        instagram_metrics = get_instagram_metrics(post_id)

    return render_template("instagram.html", instagram_response=instagram_response, instagram_metrics=instagram_metrics)
