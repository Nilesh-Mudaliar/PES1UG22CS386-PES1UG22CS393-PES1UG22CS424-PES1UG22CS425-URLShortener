import os
import string
import random
import redis
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

# Connect to Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

# Domain for shortened URLs
base_url = os.environ.get('BASE_URL', 'http://localhost:5000')

def generate_short_url(length=6):
    """Generate a random short URL with specified length"""
    chars = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(chars) for _ in range(length))
    return short_id

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "URL Shortener API",
        "endpoints": {
            "POST /shorten": "Create a shortened URL",
            "GET /<short_url>": "Redirect to original URL"
        }
    })

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    
    long_url = data['url']
    
    # Check if URL already exists in database
    for key in redis_client.scan_iter("*"):
        if redis_client.get(key).decode('utf-8') == long_url:
            short_url = key.decode('utf-8')
            return jsonify({
                "original_url": long_url,
                "short_url": f"{base_url}/{short_url}"
            })
    
    # Generate a new short URL
    short_url = generate_short_url()
    while redis_client.exists(short_url):
        short_url = generate_short_url()
    
    # Store in Redis
    redis_client.set(short_url, long_url)
    
    return jsonify({
        "original_url": long_url,
        "short_url": f"{base_url}/{short_url}"
    })

@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    long_url = redis_client.get(short_url)
    
    if long_url:
        return redirect(long_url.decode('utf-8'))
    else:
        return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)