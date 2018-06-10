import sys
from gpiozero import Button
import spotipy
import spotipy.util as util
import time
import json

button = Button(pin=10,hold_time=0.75) # Change '10' to the BCM pin number required, as needed

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
    print 'spotStart called'
    global token
    token = util.prompt_for_user_token(username, scope,client_id=SP_CLIENT_ID,client_secret=SP_CLIENT_SECRET,redirect_uri=SP_REDIRECT_URI)
    print 'token created as ' + token

def spotDevices():
    print 'spotDevices called'
    global token
    try:
        global device
        sp = spotipy.Spotify(auth=token)
        devices = sp.devices()
        devices = devices['devices']
        dictionary = {}
        for item in devices:
            dictionary[item['name']] = item['id']
        device = dictionary[spotconnect_device_name]
        print 'device resolved as ' + device
    except:
        # empty token
        print 'something is not right - emptying token'
        token = ''

def spotPlay():
    print 'spotPlay called'
    global token
    global playing
    try:
        if playing:
            print 'already playing - skip'
            # if we're already playing, skip to a new track
            sp = spotipy.Spotify(auth=token)
            sp.next_track()
            time.sleep(1)
        else:
            # if we're not playing, play the playlist, turn on shuffle and skip to a new (random) track
            print 'not playing - trying to start'
            sp = spotipy.Spotify(auth=token)
            sp.start_playback(device_id=device,context_uri=playlist)
            sp.shuffle(True)
            sp.next_track()
            playing = True
            time.sleep(1)
    except:
        # empty token
        print 'something is not right - emptying token'
        token = ''

def spotStop():
    print 'spotStop called'
    global token
    global playing
    try:
        if playing:
            # stop(pause) playing
            print 'currently playing - trying to stop'
            sp = spotipy.client.Spotify(auth=token)
            sp.pause_playback()
            playing = False
            time.sleep(1)
        else:
            # if not playing, do nothing
            print 'not playing - doing nothing'
            pass
    except:
        # empty token
        print 'something is not right - emptying token'
        token = ''

idle = 0

while True:
    if not token:
        spotStart()
        spotDevices()
    if idle == 14400: # roughly every hour (14400*0.25secs = 60 mins) empty token
        idle = 0
        token = ''
    else:
        idle += 1
        time.sleep(0.25)
    button.when_pressed = spotPlay
    button.when_held = spotStop