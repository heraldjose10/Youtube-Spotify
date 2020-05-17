# -*- coding: utf-8 -*-
"""
Created on Wed May 13 22:10:46 2020

@author: herald jose
"""

import requests
import json


#Input refresh token to get refresh access token
def GetYTAccessToken():
    url1='https://accounts.google.com/o/oauth2/token'
    data1={
            'client_id' : '[YT_CLIENT_ID]',
            'client_secret' : '[YT_CLIENT_SECRET]',
            'refresh_token' : '[YT_REFRESH_TOKEN]',
            'grant_type' : 'refresh_token'
            }
    r1=requests.post(url=url1 ,data=data1)
    text1=r1.json()
    return(text1.get('access_token'))
    

#Make youtube playlist with same name as spotify playlist and return playlist id
def MakePlaylist(acc_token,api_key,name):
    url=('https://www.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&key={}'.format(api_key))
    head={
            'Authorization' : 'Bearer {}'.format(acc_token),
            'Content-Type' : 'application/json',
    
            }
    data1={
  "snippet": {
          "status": {
    "privacyStatus": "public"
  },
    "title": "{}".format(name)
    }
  }
    r=requests.post(url,data=json.dumps(data1),headers=head)
    res=r.json()
    if r.ok==True:
        print('Playlist {} made'.format(name))
        return(res.get('id'))
    else:
        print('Error making playlist')
    

#input spotify refresh token to get refreshed access token    
def SpotifyToken():
    client_id = '[SPOTIFY_CLIENT_ID]'
    client_secret = '[SPOTIFY_CLIENT_SECRET]'
    refresh_token = '[SPOTIFY_REFRESH_TOKEN]'
    url1 = 'https://accounts.spotify.com/api/token'
    data1 = {
            'grant_type' : 'refresh_token',
            'refresh_token' : '{}'.format(refresh_token)
            }

    r1=requests.post(url=url1,data=data1,auth = (client_id, client_secret))
    res=r1.json()
    return(res.get('access_token'))  


#Returns the existing users spotify playlists and select a playlist
def GetSpotifyPlaylists(access_token):
    url2='https://api.spotify.com/v1/me/playlists'
    head={
            'Content-Type' : 'application/json',
            "Authorization": "Bearer {}".format(access_token)
            }
    r2=requests.get(url=url2,headers=head)
    res=r2.json()
    spotify_playlists={}
    for i in range(len(res.get('items'))):
        spotify_playlists[res.get('items')[i].get('name').lower()]=res.get('items')[i].get('id')
    
    print('List of Playlists :')
    for key in spotify_playlists:
        print(key)    
    desired_playlist=str(input('Enter the name of desired Playlist :')).lower()


    if desired_playlist in spotify_playlists:
        return(desired_playlist,spotify_playlists[desired_playlist])
    else:
        print('Check for Spellng Errors')
        

#Returns name of songs in given spotify playlist        
def GetSongInfos(playlist_id,spotifytoken):
    url='https://api.spotify.com/v1/playlists/{}/tracks?limit=10'.format(playlist_id)
    head={
            'Content-Type' :'application/json',
            'Authorization' :'Bearer {}'.format(spotifytoken)
            }
    r=requests.get(url,headers=head)
    print(r.ok)
    res=r.json()
    songlist=[]
    for i in range(len(res.get('items'))):
        songlist.append(res.get('items')[i].get('track').get('name'))
        print('added song : {} '.format(res.get('items')[i].get('track').get('name')))
    return(songlist)
 

#uses names returned to search for video id in youtube and returns video id    
def SearchYT(api_key,songs_list,acc_token):
    url='https://www.googleapis.com/youtube/v3/search?key={}'.format(api_key)
    head={
          'Authorization' :'Bearer {}'.format(acc_token),
          'Accept' :'application/json'
            }
    videoids=[]
    for i in songs_list:
        para={
            'part' : 'snippet',
            'q' : '{}'.format(i),
            'type' : 'video',
            'safeSearch' : 'none'
                }
        r=requests.get(url,params=para,headers=head)
        res=r.json()
        print(r.ok)
        videoids.append(res.get('items')[0].get('id').get('videoId'))
    return(videoids)


#takes playlist id and video ids to insert videos to playlist
def Insert_Videos(acc_token,apikey,playlist_id,video_ids):
    url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&key={}'.format(apikey)
    head={
          'Authorization' :'Bearer {}'.format(acc_token),
          'Accept' :'application/json',
          'Content-Type' :'application/json'
            }
    for i in video_ids:
        data1={"snippet":{"playlistId":"{}".format(playlist_id),
                          "resourceId":{
                                  "kind": "youtube#video",
                                  "videoId":"{}".format(i)}}}
        r=requests.post(url,data=json.dumps(data1),headers=head)
        res=r.json()
        print('Added Video : {}'.format(res.get('snippet').get('title')))


def main():
    api_key='[YT_API_KEY]'
    access_token=GetYTAccessToken()
    spotifytoken=SpotifyToken()
    try:
        name,playlist_uri=GetSpotifyPlaylists(spotifytoken)
        songs=GetSongInfos(playlist_uri,spotifytoken)
        video_ids=SearchYT(api_key,songs,access_token)
        playlist_id=MakePlaylist(access_token,api_key,name)
        Insert_Videos(access_token,api_key,playlist_id,video_ids)

    except:
        pass

    
if __name__=='__main__':
    main()