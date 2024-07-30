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
import re
app = Flask(__name__)


def get_spotify_download_link(query):
  def get_download_link(songurl):
    try:
      initial_url = "https://spotifymate.com/"
      response_initial = requests.get(initial_url)
      response_initial.raise_for_status()
      cookies = response_initial.cookies
      soup_initial = BeautifulSoup(response_initial.text, 'html.parser')
      hidden_inputs = soup_initial.select('form#get_video input[type=hidden]')
      input_data = {}
      for input_field in hidden_inputs:
        input_name = input_field.get('name')
        input_value = input_field.get('value')
        if input_name and input_value:
          input_data[input_name] = input_value
      url_second = 'https://spotifymate.com/action'
      data_second = {'url': songurl, **input_data}
      response_second = requests.post(url_second,cookies=cookies,data=data_second)
      response_second.raise_for_status()
      second_soup = BeautifulSoup(response_second.text, 'html.parser')
      download_div = second_soup.find('div', {'class': 'abuttons mb-0'})
      if download_div and download_div.a:
        download_link = download_div.a.get('href')
        return download_link
      else:
        return None
    except Exception as e:
      return None
  try:
    url = "https://open.spotify.com/"
    response = requests.get(url)
    response.raise_for_status()
    cookies = response.cookies
    access_token = ''
    if response.status_code == 200:
      match = re.search(r'"accessToken":"([^"]+)"', response.text)
      if match:
        access_token = match.group(1)
      else:
        return None
    else:
      return None
    url = "https://api-partner.spotify.com/pathfinder/v1/query"
    headers = {"Content-Type": "application/json","Authorization": "Bearer " + access_token}
    data = {"operationName": "searchDesktop","variables": {"searchTerm": search_term,"offset": 0,"limit": 10,"numberOfTopResults": 5,"includeAudiobooks": True},"extensions": {"persistedQuery": {"version":1,"sha256Hash":"a04b1320754996f10f3b4ceea825fa7c4ba5c76b7d1c8603a0be350783d8f709"}}}
    response = requests.post(url, json=data, headers=headers, cookies=cookies)
    response.raise_for_status()
    match = re.search(r'"spotify:track:(.*?)"', response.text)
    uri_value = match.group(1)
    max_attempts = 2
    url = 'https://open.spotify.com/track/' + uri_value
    for attempt in range(1, max_attempts + 1):
      download_link = get_download_link(url)
      text_to_remove = 'SpotifyMate.com%20-%20'
      if text_to_remove in download_link:
        download_link = download_link.replace(text_to_remove, '')
      if download_link:
        return download_link
  except Exception as e:
    return None
  return None
#Host it in Vercel.com
@app.route('/yagami', methods=['GET'])
    query = "Hello"
download_link = get_spotify_download_link(query)
jsonify({"download_url": download_link,"By": "t.me/Yagami_xlight"})
    if not song_name:
        return jsonify({"error": "Please provide a song name"}), 400

    

if __name__ == '__main__':
    app.run(debug=True)
