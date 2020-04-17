#!/bin/python3

#Xhulio Hasani
#21 janvier 2018 
 
import sys
import json

with open('data_clark.json', encoding='utf-8-sig') as data_file:
    data = json.loads(data_file.read())

def getStats():
    posters = []
    counts =[]
    for item in data.get('feed').get('data'):
        dude = item.get('from').get('name')
        if(posters.count(dude)!=0):
            counts[posters.index(dude)] = counts[posters.index(dude)] + 1
        else:
            posters.append(dude)
            counts.append(1)
    
    for dude in posters:
        print( dude , " : " , counts[posters.index(dude)], " posts.")
    print(len(data.get('feed').get('data')) , "posts au total")
    print(len(getYoutubeLinks()) , "liens youtube")

def cprint(arr):
    for s in arr:
        print(s)
def getLinks():
    links = []
    for item in data.get('feed').get('data'):
        lnk = item.get('link')
        if(links.count(lnk) == 0):
            links.append(lnk)
    return links

def getYoutubeLinks():
    links = getLinks()
    youtubeLinks = []
    rejected = []
    nothing  = []
   
    for lnk in links:
        if(type(lnk) != type("str")):
            #print("WEIRD")
            #print(lnk)
            nothing.append(lnk)
        else:
            if("youtu" in lnk):
                youtubeLinks.append(lnk)
            else:
                rejected.append(lnk) 
    print("ACCEPTED : " ,len(youtubeLinks))
    print("REJECTED : ",len(rejected))
    print("EMPTY : " , len(nothing))
    return youtubeLinks


#################################################################################################

# -*- coding: utf-8 -*-

import os

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
CLIENT_SECRETS_FILE = "./.env/your_secret_key"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl','https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/youtubepartner']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def print_response(response):
  print(response)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def playlist_items_insert(client, properties, **kwargs):
  resource = build_resource(properties)
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.playlistItems().insert(
    body=resource,
    **kwargs
  ).execute()

  return print_response(response)

def getVideoId(link):
    idLen  = 11
    idStart = link.find("?v=")
    #maybe other form
    if(idStart == -1):
        idStart = link.find("&v=")
    #if fails...no id
    if(idStart == -1):
        return
    #offset
    idStart = idStart + 3

    ID = link[idStart:idStart+idLen]
    return ID


def sendRequest(link):
    playlist_items_insert(client, 
        {'snippet.playlistId': 'your-playlist-id',
        'snippet.resourceId.kind': 'youtube#video',
        'snippet.resourceId.videoId': getVideoId(link),
        'snippet.position': ''},
        part='snippet',
        onBehalfOfContentOwner='')

def getEm(ytLinks):
    if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    #os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    #client = get_authenticated_service()
    
        ytLinks = getYoutubeLinks()
        for link in ytLinks:
            print(getVideoId(link) , type(getVideoId(link)))
            if(type(link) == type("str")):
                try:
                    sendRequest(link)
                except Exception as e:
                    print(e)
    
getStats()