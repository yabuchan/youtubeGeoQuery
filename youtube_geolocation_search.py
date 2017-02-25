#!/usr/bin/python
from flask import Flask
from flask import request

from apiclient.discovery import build
from apiclient.errors import HttpError
#from oauth2client.tools import argparser
import argparse
import json

app = Flask(__name__)


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyAXYHQkdWS56MHZsIXWuxpQ2n-iHXOQMgE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    type="video",
    location=options.location,
    locationRadius=options.location_radius,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  search_videos = []

  # Merge video ids
  for search_result in search_response.get("items", []):
    search_videos.append(search_result["id"]["videoId"])
  video_ids = ",".join(search_videos)

  # Call the videos.list method to retrieve location details for each video.
  video_response = youtube.videos().list(
    id=video_ids,
    part='snippet, recordingDetails'
  ).execute()

  videos = []

  # Add each result to the list, and then display the list of matching videos.
  for video_result in video_response.get("items", []):
    videos.append("%s, (%s,%s)" % (video_result["snippet"]["title"],
                              video_result["recordingDetails"]["location"]["latitude"],
                              video_result["recordingDetails"]["location"]["longitude"]))
  #videos.append(video_result)
#  print (video_response)
#  for video_result in video_response.get("items", []):
#    videos.append({
#      title: video_result["snippet"]["title"]
#      })
#  print ("Videos:\n", "\n".join(videos), "\n")
  return video_response


####### rest api wrapper ##########
#lat
#lng
#keywords
@app.route("/broker/list")
def listBrokerApi():
  lat = request.args.get('lat')
  lng = request.args.get('lng')
  keywords = request.args.get('keywords')
  location = lng + ',' + lat
  print (keywords)
  print (location)
  argparser = argparse.ArgumentParser()
  argparser.add_argument("--q", help="Search term", default=keywords)
  argparser.add_argument("--location", help="Location", default=location)
  argparser.add_argument("--location-radius", help="Location radius", default="5km")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args2 = argparser.parse_args()
  print (args2)
#  try:
  videos = youtube_search(args2)
#  print (videos[0].id)
  return json.dumps(videos)


if __name__ == "__main__":
    # Start flask
    app.run(host= '0.0.0.0')

