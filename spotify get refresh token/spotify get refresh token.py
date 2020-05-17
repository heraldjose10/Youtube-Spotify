# -*- coding: utf-8 -*-
"""
Created on Sat May  9 16:39:11 2020

@author: herald jose
"""

import requests
url1='https://accounts.spotify.com/api/token'
encoded_secret=''
client_id = '[SPOTIFY_CLIENT_ID]'
client_secret = '[SPOTIFY_CLIENT_SCRET]'
         
data1={
       'grant_type' : 'authorization_code',
       'code' : '[CODE_FOR_REFRESH_TOKEN]',
       'redirect_uri' : 'https://github.com',     

       }
r1=requests.post(url=url1,data=data1,auth = (client_id, client_secret))
if r1.ok==True:
    res=r1.json()
    access_token=res.get('access_token')
    refresh_token=res.get('refresh_token')
    print('access_token :',res.get('access_token'))
    print('refresh_token :',res.get('refresh_token'))
else:
    print('Error Occured')
    print(r1.text)

