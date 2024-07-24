from flask import Flask, request, jsonify
from pytube import YouTube
import requests
import random
import pyfiglet
import sys
import time
from random import randint
from fake_useragent import UserAgent  # Use fake_useragent for user agent generation
from bs4 import BeautifulSoup
import json
import os
app = Flask(__name__)

def search_video(song_name):
    query = song_name.replace(' ', '+')
    ua = UserAgent()
url = "https://savetik.co/api/ajaxSearch"
payload = f"q={query}&lang=en"


session = requests.Session()

headers = {
    'User-Agent': ua.random,  # Use a random user agent from fake_useragent
    'Content-Type': "application/x-www-form-urlencoded",
    'sec-ch-ua': "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
    'dnt': "1",
    'sec-ch-ua-mobile': "?1",
    'x-requested-with': "XMLHttpRequest",
    'sec-ch-ua-platform': "\"Android\"",
    'origin': "https://savetik.co",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://savetik.co/en2",
    'accept-language': "ar,en-US;q=0.9,en;q=0.8"
}



    try:
        response = session.post(url, data=payload, headers=headers)
if response.status_code == 200:
        data = response.json()
        soup = BeautifulSoup(data['data'], 'html.parser')
        links = soup.find_all('a', class_='tik-button-dl')
        if len(links) >= 2:
            link = links[1]['href']
         
        else:
            print("Error: No valid download link found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
else:
    jsonify({"error":"Request failed with status code {response.status_code}").400

#Host it in Vercel.com
@app.route('/apiurl', methods=['GET'])
def download_audio():
    song_name = request.args.get('songname')
    if not song_name:
        return jsonify({"error": "Please provide a song name"}), 400

    link = search_video(song_name)
    if not link:
        return jsonify({"error": "No video found or video is blocked"}), 404


    return jsonify({"download_link": link})

if __name__ == '__main__':
    app.run(debug=True)
