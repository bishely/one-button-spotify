# one-button-spotify

One-Button-Spotify is a simple Python(2) script which uses [Spotipy](https://github.com/plamere/spotipy/) to access the Spotify Web API and provide basic control (play/skip/pause) of a Spotify Connect Enabled device (eg a Pi running [Raspotify](https://github.com/dtcooper/raspotify) with a single button. 

# Nota Bene

This project is currently under development. It's tested and working, but might throw an error or two if things go wrong that I haven't yet encountered in my own tests. Oh, and there are probably/definitely some inefficiencies in my code - feel free to fork and push improvements or get in touch. Also see my noted quirks section at the bottom of this Readme.

## Quick Explanation
### (for people who know their way around)

#### You need: 
* A Spotify Connect enabled device for playback (eg Amazon Echo Dot)
* A Raspberry Pi with available/accessible GPIO pins
* A button
* A Spotify Premium account

#### Steps:
1. Sign up to [Spotify for Developers](https://beta.developer.spotify.com/) if you haven't already, and create a new app/client id. Note down the Client ID and Client Secret. Set the redirect URL to `http://localhost/` (or, optionally, something of your choosing)
2. Note down the Spotify Connect Device Name for your playback device (eg 'My Echo Dot').
3. In an official Spotify client, create or choose a playlist to use, then find the Share button, and note down the URI.
4. Install Raspbian (or the OS of your choice) on your Pi. NB: you will need a GUI with Web Browser to authorise the script to control your Spotify account, so don't use a 'Lite' version. I can't find a way around this (I've seen scripts that authorise via CLI in the past, but I can't figure out how they did it or if it's still possible).
5. `sudo apt install python-gpiozero`
6. `pip install git+https://github.com/plamere/spotipy.git`
7. grab the one-button-spotify.py script
8. edit the one-button-spotify.py script with the editor of your choice:
    a. replace xxxYourUserNamexxx with your actual username
    b. replace xxxYourPasswordxxx with your actual password
    c. replace xxYourPlayListURIfromSpotifyxxx with your playlist URI from step 3
    d. replace xxxYourTargetSpotifyConnectDeviceNamexxx with your Spotify Connect Device Name from step 2
    e. replace xxxClientIDofYourAppxxx with the Client ID from step 1
    f. replace xxxClientSecretofYourAppxxx with the Client Secret from step 1
    g. if necessary, replace `http://localhost/` with the redirect URL you created in step 1
    h. if necessary, replace `pin=23` with a different BCM pin number
9. connect your button to BCM pin 23 (or whatever you changed it to in the script)
10. `python one-button-spotify.py`
11. the script *should* open your browser at the redirect URL - simply copy the full URL and paste it back into the terminal as instructed - if your browser didn't open automatically, copy the URL shown in the terminal and paste it into your browser, then copy the redirect URL and paste it into the terminal
12. it *should* now be running - (short)press the button to start playback, press it again to skip to a random track. Long press will stop playback.
13. make the script run as a daemon

## Use Case (aka: why did you do this?)

I have a 3 year old daughter. Toddlers are old enough to have their own taste in music, but not yet old enough to use a GUI (mainly because they can't usually read very well, but also due to hand-eye-coordination issues) or necessarily to remember a complex hardware interface. So I wanted to build a way for her to play her own favourite songs from Spotify in her bedroom, in as simple an interface as possible. I could've simply mapped a button to play/skip on a Raspberry Pi, but that would've meant having the speaker within reach, and I know *I* used to enjoy poking speaker cones when I was younger, so...

So the system uses two Raspberry Pis, although one of them could easily be replaced by any Spotify Connect enabled device (eg an Amazon Echo, a Sonos, or a phone or laptop running Spotify). One Pi is a ZeroW hooked up to a speaker via a [Pimoroni PhatDAC](https://shop.pimoroni.com/products/phat-dac), and running [Raspotify](https://github.com/dtcooper/raspotify), configured to login to my daughter's account (we have the Spotify Premium Family plan, so she's just a passenger account on that). I won't explain how to do that here, as the Docs for both the PhatDAC and Raspotify are both comprehensive and readable for novices.

The second Pi is a Pi3, which doubles as our BabyCam (even though she's not a baby anymore). It has a Pimoroni (love those guys) [Pan Tilt Hat](https://shop.pimoroni.com/products/pan-tilt-hat) controlling a NoIR camera. It also (through some grubby physical hacking) has a button attached to BCM pin 23. This one runs the `one-button-spotify.py` script as a daemon when it boots. 

So the Pi-with-a-button runs `one-button-spotify.py`. When you short-press the button, it either starts playback (if paused/stopped) on the Spotify Connect output, or else skips to a random track within a specified playlist. When you long-press (>1 second) the button, it pauses/stops playback (or does nothing if it's not currently playing).

## How To

A detailed explanation for people new to Raspberry Pis, Raspbian, Python, the Spotify API, Spotipy etc etc is on its way. Be patient.

# Noted Quirks

I'm no expert coder, just a tinkerer who likes to play around with things. With that in mind, there are some parts of my code that probably don't operate the way they *should* (ie - the way a more experienced Python coder would do them). I'm listing them here in case you, dear reader, want to take a look and tell me how to do it right.

- [ ] The `spotDevices` function calls Spotipy's `devices` function, then does an overcomplicated bit of jiggery-pokery to get the ID associated with the device name stored in `spot_connect_device_name`. I'm aware that Spotipy's `devices` function already returns a dictionary with all the details I could possibly need, but I couldn't find a clean way of getting `id` for a given `name`, so I ended up using a for loop to create a second dictionary that only stores pairs of those values. I'd really appreciate someone explaining if there's a better way around this.
- [ ] In the `spotStop` function, I should probably rewrite the conditional to `if not playing:` to remove the need for `pass` and `else:`. I might do this at some point.
- [ ] Similarly, in the main `while True:` loop, I suspect there's a better way to switch between short and long presses than simply sleeping for 1.5 seconds before checking `is_held`, but this is my first draft of my first project using the gpiozero library, so forgive me or tell me how to do it better!