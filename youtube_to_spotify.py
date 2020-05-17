import re
import youtube_dl
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
    print(r1.ok)
    text1=r1.json()
    return(text1.get('access_token'))


#returns list to users yt playlist and select a playlist
def Get_ytPlaylist_id(acc,key):
    url2='https://www.googleapis.com/youtube/v3/playlists'
    para={
            'part' : 'snippet,contentDetails',
            'mine' : 'true',
            'key' : '{}'.format(key),
            'maxResults' : 50
            }
    heads={
            'Authorization' : 'Bearer {}'.format(acc),
            'Accept' : 'Accept'
            }
    r2=requests.get(url=url2,params=para,headers=heads)
    r2data=json.loads(r2.text)
    

    youtube_playlists={}
    for i in range(len(r2data.get('items'))):
        youtube_playlists[r2data.get('items')[i].get('snippet').get('title').lower()]=r2data.get('items')[i].get('id')
        
    print('List of Playlists :')
    for key in youtube_playlists:
        print(key)    
    desired_playlist=str(input('Enter the name of desired Playlist :')).lower()


    if desired_playlist in youtube_playlists:
        return(desired_playlist,youtube_playlists[desired_playlist])
    else:
        print('Check for Spellng Errors')
        

#Resturns links to videos in the playlist as a list        
def GetVidLinks(acc,playlistid,key):
    url='https://www.googleapis.com/youtube/v3/playlistItems'
    para={
            'part' : 'snippet,contentDetails',
            'playlistId' : '{}'.format(playlistid),
            'key' : '{}'.format(key),
            'maxResults'  : 50
            }
    heads={
            'Authorization' : 'Bearer {}'.format(acc),
            'Accept' : 'Accept'
            }
    r2=requests.get(url,params=para,headers=heads)
    r2data=json.loads(r2.text)
    videolinks_list=[]
    for i in range(len(r2data.get('items'))):
        videolinks_list.append('https://www.youtube.com/watch?v='+r2data.get('items')[i].get('contentDetails').get('videoId'))
    return(videolinks_list)


#Uses youtube_dl to extract information from video
def GetVideoDetails(videolist,apotify_access_token):
    spotify_uris=[]
    for i in videolist:
        video=youtube_dl.YoutubeDL().extract_info(i, download=False)


        try:
            if video["categories"][0]=='Music':
                if video["track"]!= None :
                    track=(re.sub("[\(\[].*?[\)\]]", "", video["track"]))#Removes everything inside quotes
                else:
                    track=(re.sub("[\(\[].*?[\)\]]", "", video["title"]))
            artist=(video["artist"])

        except:
            pass
        
        try:
            if artist!=None and track!=None:
                spotify_uris.append(songsearch1(apotify_access_token,track,artist))
            else:
                spotify_uris.append(songsearch(apotify_access_token,track))
        except:
            pass
    return(spotify_uris)
            

#returns refreshed spotify access token          
def spotifytokens():
    url1='https://accounts.spotify.com/api/token'
    client_id = '[SPOTIFY_CLIENT_ID]'
    client_secret = '[SPOTIFY_CLIENT_SECRET]'
    refresh_token ='[SPOTIFY_REFRESH_TOKEN]' 
    data1={
            'grant_type' : 'refresh_token',
            'refresh_token' : '{}'.format(refresh_token)     
            }
    r1=requests.post(url=url1,data=data1,auth = (client_id, client_secret))
    res=r1.json()
    access_token = res.get('access_token')
    return(access_token)


#Uses spotify API to search for a video name
def songsearch(spotify_token,track):

      url='https://api.spotify.com/v1/search'
      head={
            'Accept':'application/json',
            'Content-Type':'application/json',
            "Authorization": "Bearer {}".format(spotify_token)
      
            }
      para={
            'q':'{}'.format(track),
            'type':'track',
            'limit':1,
            'offset':0
      
            }
      r = requests.get(url,params=para,headers=head)
      data=r.json()
      return(data.get('tracks').get('items')[0].get('uri'))


#Uses spotify API to search for a video name and artist name
def songsearch1(spotify_token,track,artist):

 
      url='https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=1'.format(track,artist)
      head={
            'Accept':'application/json',
            'Content-Type':'application/json',
            "Authorization": "Bearer {}".format(spotify_token)
      
            }
      
      r = requests.get(url,headers=head)
      data=r.json()
      return(data.get('tracks').get('items')[0].get('uri'))
      

#Creates a new playlist for user      
def MakeNewPlaylist(user_id,spotify_token,playlist_name):
    url='https://api.spotify.com/v1/users/{}/playlists'.format(user_id)
    request_body = json.dumps({
            "name": "{}".format(playlist_name),
            "description": "All Liked Youtube Videos",
            "public": True
        })
    head1={
            'Content-Type':'application/json',
            "Authorization": "Bearer {}".format(spotify_token)
            }
    r=requests.post(url,data=request_body,headers=head1)
    return(r.json().get('id'))


#Adds list of song to newly created playlist
def AddSongtoPlaylist(song_uri,playlist_id,spotify_token):
    url='https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
    for i in song_uri:
        request_body = json.dumps(['{}'.format(i)])
        head={
                'Accept':'application/json',
                'Content-Type':'application/json',
                "Authorization": "Bearer {}".format(spotify_token)
                
                }
        r=requests.post(url,data=request_body,headers=head)
        if r.ok==True:
            print('Added Song {} to Playlist'.format(i+1))    
        else:
            print('Could not add song to playlist')


def main():
    key='[YOUTUBE_API_KEY]'
    spotify_userid='[SPOTIFY_USER_ID]'
    yt_access_token=GetYTAccessToken()
    try:
        name,yt_playlist_id=Get_ytPlaylist_id(yt_access_token,key)
        videolinks_list=GetVidLinks(yt_access_token,yt_playlist_id,key)
        apotify_access_token=spotifytokens()
        uris_list=GetVideoDetails(videolinks_list,apotify_access_token)
        playlistid=MakeNewPlaylist(spotify_userid,apotify_access_token,name)
        AddSongtoPlaylist(uris_list,playlistid,apotify_access_token)
    except:
        pass

      
    
    
if __name__=='__main__':
    main()
    


    
    
