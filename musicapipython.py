from flask import Flask, request, jsonify
from pytube import YouTube
import requests

app = Flask(__name__)

def search_video(song_name):
    query = song_name.replace(' ', '+')
    url = f"https://apis.deepjyoti30.dev/v2/ytmdl/search?q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            video_url = data[0]["url"]
            return video_url
        return None
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return None

def extract_audio(video_url):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            return audio_stream.url
        return None
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None
#Host it in Vercel.com
@app.route('/apiurl', methods=['GET'])
def download_audio():
    song_name = request.args.get('songname')
    if not song_name:
        return jsonify({"error": "Please provide a song name"}), 400

    video_url = search_video(song_name)
    if not video_url:
        return jsonify({"error": "No video found or video is blocked"}), 404

    audio_url = extract_audio(video_url)
    if not audio_url:
        return jsonify({"error": "Audio extraction failed"}), 500

    return jsonify({"download_link": audio_url})

if __name__ == '__main__':
    app.run(debug=True)