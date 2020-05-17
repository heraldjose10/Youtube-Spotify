# -*- coding: utf-8 -*-
"""
Created on Sat May  9 16:25:42 2020

@author: herald jose
"""

import requests

url1='https://accounts.spotify.com/authorize'
para1={
       'client_id' : '[SPOTIFY_CLIENT_ID]',
       'response_type' : 'code',
       'redirect_uri' : 'https://github.com',
       'scope' : 'playlist-modify-public playlist-modify-private'
       }
r=requests.get(url=url1,params=para1)
#copy and paste the output url in a browser and login
#part after ?code='...' is the code for obtaining refresh token
print(r.ok)
print(r.url)