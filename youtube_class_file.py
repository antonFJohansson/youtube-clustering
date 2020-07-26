# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:03:51 2020

@author: johaant
"""

import os, io
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaIoBaseDownload
import pickle
from youtube_transcript_api import YouTubeTranscriptApi
import csv, sys, time


class youtube_class():
    
    def __init__(self, download_folder, video_channel_id):
        
        if not os.path.isdir(download_folder):
            os.mkdir(download_folder)
        self.download_folder = download_folder
        self.video_channel_id = video_channel_id
        self.video_id_store = []
        self.description_store = []
        
        ## Just for printing purpose
        self.print_prog_id = 0
        
        ## Already downloaded subs
        #self.downloaded_subs = [sub_txt.split('_')[2].rstrip('.txt') for sub_txt in os.listdir(download_folder)]
        
        ## TO save the info
        self.video_id_save_name = 'video_id.pickle'
        self.description_save_name = 'description_name.pickle'
        
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
        
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        
    def retrieve_channel_info(self):
        ## Does retrieve channel information cost credits and thus I cannot retrive the subtitles later?
        
        def download_info(channel_id):

            res = self.youtube.channels().list(id = channel_id,
                                        part = 'contentDetails').execute()
            playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            store_all_info = []
            next_page_token = None
            
            ## Can I only get 50 results here ever?
            num_videos_seen = 0
            num_videos_stored = 0
            
            
            while True:
                
                res = self.youtube.playlistItems().list(playlistId = playlist_id,
                                                   part = 'snippet',
                                                   maxResults = 50,
                                                   pageToken = next_page_token).execute()
                
                information_list = res['items']
        
                for video_info in information_list:
                      
                    ## Does the video have subtitles
                    time.sleep(0.05) ## Might improve the amount of subs that we can download
                    try:
                        
                        video_id = video_info['snippet']['resourceId']['videoId']
                        
                        video_capt = YouTubeTranscriptApi.get_transcript(video_id)
                        
                        
                        dict_store = {'title': '', 'description': '', 'video_id': '', 'subs': ''}
                    
                        dict_store['title'] = video_info['snippet']['title'].replace('\n', ' ')
                        dict_store['description'] = video_info['snippet']['description'].replace('\n', ' ')
                        
                        
                        
                        dict_store['video_id'] = video_id
                        
                        store_text = ''
                        for subs in video_capt:
                            clean_text = subs['text'].replace('\n', ' ')
                            store_text = store_text + clean_text
                        dict_store['subs'] = store_text
                        store_all_info.append(dict_store)
                        num_videos_seen = num_videos_seen + 1
                        num_videos_stored = num_videos_stored + 1
                    ## If not hen ignore it
                    except:
                        num_videos_seen = num_videos_seen + 1
                    self.print_progress()

                next_page_token = res.get('nextPageToken')
                
                
                if next_page_token is None:
                    break
            
            if len(store_all_info) == 0:
                no_information_stored = 'No information could be retrieved. Most likely due to youtube blocking repeated access attempts.'
                raise Exception(no_information_stored)
            else:
                print('\n Information for {}/{} videos could be retrieved'.format(num_videos_stored, num_videos_seen))
                return store_all_info
            
        
        self.all_information_store = download_info(self.video_channel_id)
        self.save_channel_info(self.download_folder)
        
    def save_channel_info(self, save_folder = 'saved_channel_info'):
        
       ## So we just save it as a csv or something similar here I guess?
       if len(self.all_information_store) != 0:
        csv_columns = [col_name for col_name in self.all_information_store[0].keys()]
        csv_file = "stored_information.csv"
        csv_file = os.path.join(save_folder, csv_file)
        try:
              with io.open(csv_file, "w", newline = '', encoding="utf-8") as csvfile:
              #with open(csv_file, 'w',newline='') as csvfile:
                  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                  writer.writeheader()
                  for data in self.all_information_store:
                      writer.writerow(data)
              print('\nInformation has been retrieved.')
        except IOError:
              print("I/O error")
       else:
         print('\n Information could not be retrieved.')

    def print_progress(self):
        
        sys.stdout.write('\r')
        print_line = 'Retrieving Information' + self.print_prog_id*'.'
        sys.stdout.write(print_line)
        sys.stdout.flush()
        self.print_prog_id += 1
        if self.print_prog_id == 5:
            self.print_prog_id = 1
            sys.stdout.write('\r')
            sys.stdout.write(len(print_line)*' ')
            sys.stdout.write('\r')
            sys.stdout.write('Retrieving Information' + self.print_prog_id*'.')
            sys.stdout.flush()
        











