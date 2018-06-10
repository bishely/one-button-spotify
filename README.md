# one-button-spotify

One-Button-Spotify is a simple Python(2) script which uses [Spotipy](https://github.com/plamere/spotipy/) to access the Spotify Web API and provide basic remote control (play/skip/pause) of a Spotify Connect Enabled device (eg a Pi running [Raspotify](https://github.com/dtcooper/raspotify) with a single button. 

# Nota Bene

This project is potentially unreliable, as I'm not much of a coder. It's tested and working, but might throw an error or two if things go wrong that I haven't yet encountered in my own tests. Oh, and there are probably/definitely some inefficiencies in my code - feel free to fork and push improvements or get in touch. Also see my noted quirks section at the bottom of this Readme.

## Quick Explanation
### (for people who know their way around)

#### You need: 
* A Spotify Connect enabled device for playback (eg Amazon Echo Dot)
* A Raspberry Pi with available/accessible GPIO pins
* A button
* A Spotify Premium account

#### Steps:
1. Sign up to [Spotify for Developers](https://beta.developer.spotify.com/) if you haven't already, and create a new app/client id. Note down the `Client ID` and `Client Secret`. Set the redirect URL to `http://localhost/` (or, optionally, something of your choosing)
1. Note down the Spotify Connect Device Name for your playback device (eg 'My Echo Dot')<sup>*</sup>.
1. In an official Spotify client, create or choose a playlist to use, then find the Share button, and note down the URI.
1. Install Raspbian (or the OS of your choice) on your Pi. NB: you will need a GUI with Web Browser to authorise the script to control your Spotify account, so don't use a 'Lite' version. I can't find a way around this (I've seen scripts that authorise via CLI in the past, but I can't figure out how they did it or if it's still possible).
1. `sudo apt install python-gpiozero`
1. `pip install git+https://github.com/plamere/spotipy.git`
1. Grab the `one-button-spotify.py` script
1. Edit the `one-button-spotify.py` script with the editor of your choice:
    1. Replace `xxxYourUserNamexxx` with your actual username
    1. Replace `xxxYourPasswordxxx` with your actual password
    1. Replace `xxYourPlayListURIfromSpotifyxxx` with your playlist URI from step 3
    1. Replace `xxxYourTargetSpotifyConnectDeviceNamexxx` with your Spotify Connect Device Name from step 2
    1. Replace `xxxClientIDofYourAppxxx` with the Client ID from step 1
    1. Replace `xxxClientSecretofYourAppxxx` with the Client Secret from step 1
    1. If necessary, replace `http://localhost/` with the redirect URL you created in step 1
    1. If necessary, replace `pin=10` with a different BCM pin number
1. Connect your button to BCM pin 10 (or whatever you changed it to in the script) and ground
1. `python one-button-spotify.py`
1. The script *should* open your browser at the redirect URL - simply copy the full URL and paste it back into the terminal as instructed - if your browser didn't open automatically, copy the URL shown in the terminal and paste it into your browser, then copy the redirect URL and paste it into the terminal
1. It *should* now be running - (short)press the button to start playback, press it again to skip to a random track. Long press will stop playback.
1. Stop the script (`Ctrl+C`) and (if required) make it run as a daemon.

<sup>*</sup>If you're using (as I am) Raspotify for your playback device, you'll also have to configure Raspotify to log in to the same account you're using for my button script - as far as I can tell, the Spotify Connect API doesn't return Spotify Connect devices on the same LAN as you, they're only detected by official clients.

## Use Case (aka: why did you do this?)

I have a 3 year old daughter. Toddlers are old enough to have their own taste in music, but not yet old enough to use a GUI (mainly because they can't usually read very well, but also due to hand-eye-coordination issues) or necessarily to remember a complex hardware interface. So I wanted to build a way for her to play her own favourite songs from Spotify in her bedroom, in as simple an interface as possible. I could've simply mapped a button to play/skip on a Raspberry Pi, but that would've meant having the speaker within reach, and I know *I* used to enjoy poking speaker cones when I was younger, so...

So the system uses two Raspberry Pis, although one of them could easily be replaced by any Spotify Connect enabled device (eg an Amazon Echo, a Sonos, or a phone or laptop running Spotify). One Pi is a ZeroW hooked up to a speaker via a [Pimoroni PhatDAC](https://shop.pimoroni.com/products/phat-dac), and running [Raspotify](https://github.com/dtcooper/raspotify), configured to login to my daughter's account (we have the Spotify Premium Family plan, so she's just a passenger account on that). I won't explain how to do that here, as the Docs for both the PhatDAC and Raspotify are both comprehensive and readable for novices.

The second Pi is a Pi3, which doubles as our BabyCam (even though she's not a baby anymore). It has a Pimoroni (love those guys) [Pan Tilt Hat](https://shop.pimoroni.com/products/pan-tilt-hat) controlling a NoIR camera. It also (through some grubby physical hacking) has a button attached to BCM pin 23. This one runs the `one-button-spotify.py` script as a daemon when it boots. 

So the Pi-with-a-button runs `one-button-spotify.py`. When you short-press the button, it either starts playback (if paused/stopped) on the Spotify Connect output, or else skips to a random track within a specified playlist. When you long-press (>1 second) the button, it pauses/stops playback (or does nothing if it's not currently playing).

## How To

### Hardware

You will need:
* A Raspberry Pi (any version) with accessible GPIO and either on-board WiFi or a dongle
* A button (I used the arcade-style button and lamp that came with MagPi's free Google AIY kit)
* Wires, wire stripper, soldering iron and solder
* A power supply for your Pi
* An enclosure to house your Pi and button (I used a cardboard gift box for some socks - it was sturdy enough to withstand toddler-bashing, but also easy to cut with a craft knife)
* Tools to cut your enclosure, plus stuff to secure your components (eg hot glue, blu tack, cable ties)

#### Steps
1. Decide where in your enclosure the button and Pi will sit, then cut holes accordingly for the button and power supply
1. Mount the button, secure the Pi
1. Cut, strip and tin two wires to go between the Pi's GPIO and the button
1. Solder one end of your wires to a GPIO pin (I used pin 10 - if you use something different, note it down!) and GND
1. Solder the other end of your wires to opposite sides of your button
1. Run the power supply cable to its correct position, but don't apply power yet.

### Software

You will need:
* An SD card
* A working computer with Internet connection and a VNC Viewer<sup>*</sup>
* A Spotify Premium account

<sup>*</sup>I use [VNC Viewer for Chrome](https://chrome.google.com/webstore/detail/vnc%C2%AE-viewer-for-google-ch/iabmpiboiopbgfabjmgeedhcmjenhbla), but there are many alternatives available

#### Steps
1. Download the latest version of Raspbian (full, not lite)
1. Use Etcher (or similar) to flash Raspbian to the SD card
1. For convenience, follow [these steps](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) to create a `wpa_supplicant.conf` file with your WiFi details, and copy this to the `boot` partition on your newly flashed SD card
1. Also add a blank file with the name `ssh` to the boot partition. The easiest way to do this (on Linux/Unix/Mac) is the terminal command `sudo touch /path/to/boot/partition/ssh`
1. On your 'main' computer, visit [Spotify for Developers](https://developer.spotify.com)
1. Log in, and if you've never used the site before, accept the terms and conditions
1. Once your account is up and running, go to the `Dashboard` and click `Create a Client ID`. 
1. Give your new app a name (eg One Button Spotify) and a short description. 
1. Select relevant boxes for ‘what are you building’ – I think I chose Desktop App and Speakers. Click `Next`.
1. Click `No`: you are not developing a commercial integration.
1. Tick the three boxes to agree with the terms and click `Submit`.
1. You’ll now see your dashboard for your new app. Click `Edit Settings`.
1. In the text field under ‘Redirect URIs’, enter `http://localhost/` then click `Add` and then **IMPORTANT!** scroll down to the bottom and click `Save`. You can change the redirect URI to something else if you prefer, but make sure it’s an address that won’t do anything weird (ie – one you control). 
1. Now click `Show Client Secret`, and note down both your `Client ID` and `Client Secret` for use in the script.
1. Insert your SD card into your Pi and apply power, wait a minute for it to fully boot
1. SSH into your Pi (either with [PuTTY](https://putty.org/) or from a command line on your computer - I'll assume command line): `ssh pi@raspberrypi.local` using the password `raspberry`
1. Once connected to your Pi, run `sudo raspi-config` and make the following changes:
  1. Change `User Password` to something of your choosing
  1. In `Network Options`, change the `Hostname` to something of your choosing
  1. In `Interfacing Options`, `Enable VNC`
  1. When finished, don't reboot yet
1. Run `sudo apt-get update` and `sudo apt-get upgrade`, don't reboot yet
1. Run `sudo apt install python-gpiozero`
1. Run `pip install git+https://github.com/plamere/spotipy.git`
1. Run `git clone https://github.com/bishely/one-button-spotify`
1. `cd one-button-spotify`
1. `nano one-button-spotify`
1. Make the following changes to the script:
    1. Replace `xxxYourUserNamexxx` with your actual username
    1. Replace `xxxYourPasswordxxx` with your actual password
    1. Replace `xxYourPlayListURIfromSpotifyxxx` with your playlist URI from step 3
    1. Replace `xxxYourTargetSpotifyConnectDeviceNamexxx` with your Spotify Connect Device Name from step 2
    1. Replace `xxxClientIDofYourAppxxx` with the Client ID from step 1
    1. Replace `xxxClientSecretofYourAppxxx` with the Client Secret from step 1
    1. If necessary, replace `http://localhost/` with the redirect URL you created in step 1
    1. If necessary, replace `pin=10` with a different BCM pin number
1. Finally, reboot with `sudo reboot now`
1. When the Pi has rebooted, use your VNC Viewer to remote access the desktop
1. Open a terminal window and run `python ~/one-button-spotify/one-button-spotify.py`
1. If you've done everything correctly up to now, this will open a browser window asking you to authorise the app. Go ahead and authorise it, and it will redirect to a non-working webpage (starting with `http://localhost/?`. Copy the entire link for that webpage and paste it into the terminal, then press enter.
1. The script should now be running.
1. Press the button once to start playback, press it again to skip to a new track, and press-and-hold to stop/pause playback.
1. To make the script run in the background even after you disconnect, you can use the command `nohup python ~/one-button-spotify/one-button-spotify.py &`. You can do this from SSH without needing to reauthenticate in a browser.
1. If it doesn't work, make the changes from step 28 to `test.py` and run it with `python test.py` - it should start playing for 5 seconds then stop, wait 5 seconds and start again. If this works as expected, you've probably got a problem with your button soldering. If it doesn't, you've done something wrong when editing the scripts or registering yourself with Spotify for Developers. Go back over the steps slowly, or get in touch!
1. Steps to run the script automatically on boot are coming: the usual method of running it at boot as a systemd service doesn't currently work for me, as it seems to require authenticating in a browser again.


# Noted Quirks

I'm no expert coder, just a tinkerer who likes to play around with things. With that in mind, there are some parts of my code that probably don't operate the way they *should* (ie - the way a more experienced Python coder would do them). I'm listing them here in case you, dear reader, want to take a look and tell me how to do it right.

- [ ] The `spotDevices` function calls Spotipy's `devices` function, then does an overcomplicated bit of jiggery-pokery to get the ID associated with the device name stored in `spot_connect_device_name`. I'm aware that Spotipy's `devices` function already returns a dictionary with all the details I could possibly need, but I couldn't find a clean way of getting `id` for a given `name`, so I ended up using a for loop to create a second dictionary that only stores pairs of those values. I'd really appreciate someone explaining if (as I assume) there is a better way to do this.
