import sys
#from gpiozero import Button
import spotipy
import spotipy.util as util
import time
import json

#button = Button(pin=12)

username = 'xxxYourUserNamexxx'
password = 'xxxYourPasswordxxx'
playlist = 'xxxYourPlayListURIfromSpotifyxxx'
spotconnect_device_name = 'xxxYourTargetSpotifyConnectDeviceNamexxx'

SP_CLIENT_ID = 'xxxClientIDofYourAppxxx'
SP_CLIENT_SECRET = 'xxxClientSecretofYourAppxxx'
SP_REDIRECT_URI = 'http://localhost/'

global token
global playing
global device

token = ''
playing = False
device = ''
scope = 'user-library-read, user-read-playback-state, user-modify-playback-state'

def spotStart():
    global token
    token = util.prompt_for_user_token(username, scope,client_id=SP_CLIENT_ID,client_secret=SP_CLIENT_SECRET,redirect_uri=SP_REDIRECT_URI)

def spotDevices():
    global token
    print "Get Devices"
    if token:
        global device
        sp = spotipy.Spotify(auth=token)
        devices = sp.devices()
        devices = devices['devices']
        dictionary = {}
        for item in devices:
            dictionary[item['name']] = item['id']
        print dictionary
        device = dictionary[spotconnect_device_name]
    else:
        #print "Can't get token for", username
        token = ''

def spotPlay():
    global token
    global playing
    print "Play"
    if token:
        if playing == True:
            # if we're already playing, skip to a new track
            sp = spotipy.Spotify(auth=token)
            sp.next_track()
        else:
            # if we're not playing, play the playlist, turn on shuffle and skip to a new (random) track
            sp = spotipy.Spotify(auth=token)
            sp.start_playback(device_id=device,context_uri=playlist)
            sp.shuffle(True)
            sp.next_track()
            playing = True
    else:
        #print "Can't get token for", username
        token = ''
    
def spotStop():
    global token
    global playing
    print "Stop"
    if token:
        if playing == False:
            # if playback is already paused/stopped, do nothing
            pass
        else:
            # stop (pause) playing
            sp = spotipy.client.Spotify(auth=token)
            sp.pause_playback()
            playing = False
    else:
        #print "Can't get token for", username
        token = ''
        
while True:
    if not token:
        spotStart()
        spotDevices()
    if True:
        if playing == True:
            # long press script
            spotStop()
            time.sleep(5)
        else:
            # short press script
            spotPlay()
            time.sleep(5)
    else:
        time.sleep(5)