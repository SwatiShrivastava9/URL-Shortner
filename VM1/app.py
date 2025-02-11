from flask import Flask, request, jsonify, redirect
import redis
import hashlib
from flask_cors import CORS
import logging


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Connect to Redis (VM2)
redis_client = redis.StrictRedis(host="10.0.2.4", port=6379, decode_responses=True)

# Default homepage route to check if Flask is running
@app.route("/")
def home():
    return "Flask URL Shortener is Running!", 200

# Function to generate short hash
def generate_short_url(long_url):
    return hashlib.md5(long_url.encode()).hexdigest()[:6]

# Route to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get("url")
    if not long_url:
        return jsonify({"error": "URL required"}), 400

    short_url = generate_short_url(long_url)
    redis_client.set(short_url, long_url)
    
    return jsonify({"short_url": f"http://10.0.2.15/{short_url}"})

# Route to redirect short URL to original URL
#@app.route('/<short_url>', methods=['GET'])
#def redirect_url(short_url):
#    long_url = redis_client.get(short_url)
#    print(f"Redirecting {short_url} to {long_url}")  # Debug print
#    if long_url:
#        return redirect(long_url)
#    return jsonify({"error": "URL not found"}), 404

@app.route('/<short_url>')
def redirect_url(short_url):
    original_url = redis_client.get(short_url)
    if original_url:
        logging.debug(f"Redirecting {short_url} → {original_url}")
        print(f"Redirecting {short_url} → {original_url}")
        return redirect(original_url, code=302)
    else:
        logging.warning(f"Short URL {short_url} not found")
        return "URL Not Found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
#     app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))
