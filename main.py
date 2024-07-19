from flask import Flask, request, jsonify
from pytube import YouTube
import requests

app = Flask(__name__)

def search_video(song_name):
    query = song_name.replace(' ', '+')
    url = f"http://yangtautauaja.xp3.biz/v1/jugger.php?text={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            video_url = data["url"]
            return video_url
#Host it in Vercel.com
@app.route('/ai', methods=['GET'])
def download_audio():
    song_name = request.args.get('prompt')
    if not song_name:
        return jsonify({"error": "Please provide a /ai?prompt=question"}), 400

    return jsonify({"image": video_url})

if __name__ == '__main__':
    app.run(debug=True)
