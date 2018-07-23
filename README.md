#Pi Zero Snowboy
Complete guide to setting up voice activated software with Raspberry Pi Zero. 1.0 22/07/2018
##HARDWARE
Raspberry Pi Zero W
USB Sound Card Adapter (BENGOO)
3.5mm lavalier lapel mic (AGPtEK)
1W 8Ohm speakers with 3.5mm connection
8GB micro SD card
USB Micro to USB adapter (Tiny OTG)
##HARDWARE VARIATIONS
It is possible to use different hardware variations for the Pi Zero, but this setup was the easiest for me. You can go with a Raspberry Pi Zero without WiFi to save $5, but it's a very convenient feature for SSH logins. I would recommend not going with more powerful speakers if you can avoid it and especially if you want to go mobile. P=I^2(R)  1=I^2(8)  I^2=1/8  I=sqrt(1/8)  I~354mA. 354mA is going to be a big drain on a mobile setup and more powerful speakers will require an external source of power. I went with a USB sound card because of the ability to adjust the volume outside of software. There are of course cheaper USB sound cards, but this solution seems to work best for Pi Zero because there is no audio jack and there is only one micro USB available for IO. You can potentially go with a mic in on the micro usb port and audio out on HDMI if that is cheaper or if you have a HDMI audio out adapter lying around just make sure you force enable HDMI audio out under raspi-config and adjust the .asoundrc accordingly. 
##SNOWBOY SETUP
Fresh set up for Pi Zero. Skip down to update if you already know how to do this.
Sketch Lite - download raspbian sketch lite. Flash image of sketch lite onto micro SD with Etcher or favorite image flasher and put into Pi Zero. Use command
```
sudo raspi-config
```
Turn on SSH in interfacing options and change password if needed. **IF** your project needs to run on system boot change to Console Auto Login under Boot Options and then exit. Find IP address with command 
```
ifconfig
```
Connect with PuTTY or SSH client of your choosing. Login and update with command
```
sudo apt update && sudo apt -y upgrade && sudo apt-get -y auto-remove && sudo reboot
```
Install dependencies with command
```
sudo apt -y install python-pyaudio python3-pyaudio sox python3-pip python-pip libatlas-base-dev
```
Install PortAudio’s Python bindings with commands
```
sudo pip install pyaudio
sudo pip3 install pyaudio
```
Figure out what the card, device and subdevice numbers are with command
```
cat /proc/asound/modules
```
**OR** figure out what the card, device and subdevice numbers are with commands
```
aplay -l
arecord -l
```
Then create .asoundrc with command
```
sudo nano ~/.asoundrc
```
You can copy the code from the attached .asoundrc file. I'm using "hw:1,0" for both input and output because it mic and speakers are connecting both through a usb sound card. The lavalier mic needed to have the gain boosted, so you may need to delete those lines depending on your sound setup.
RESTful API Calls via python script (per snowboy instructions) need to install "requests" module for python with command
```
pip install requests
```
Download pre-packaged Snowboy binaries and their Python wrappers for Raspberry Pis with command 
```
wget https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/rpi-arm-raspbian-8.0-1.1.1.tar.bz2
```
Uncompress with command 
```
tar xvjf rpi-arm-raspbian-8.0-1.1.1.tar.bz2
```
Rename rpi-arm-raspbian-8.0-1.1.1 folder to snowboy with command 
```
mv rpi-arm-raspbian-8.0-1.1.1 snowboy
```
Make sure you are now working within your newly created snowboy folder with command
```
cd snowboy
```
Test audio out with command
```
speaker-test -c 2 
```
**OR** try audio out test with command
```
aplay /usr/share/sounds/alsa/Front_Center.wav
```
Record a 3 second test clip with command
```
arecord -d 3 test.wav
```
Verify your test audio with command
```
aplay test.wav
```
**IF** you need to tweak some alsa settings because of sound volume issues use command 
```
sudo alsamixer 
```
Make sure you press F5 to view all settings (your shortcut key might be different). And after changing settings exit and use the following command to keep the settings
```
sudo alsactl store
```
##CUSTOMIZING SNOWBOY THROUGH SNOWBOY WEBSITE
I found this method easier since I was using multiple models and callbacks. Log into https://snowboy.kitt.ai/ and create your personal models or find a universal model for your hotwords. Use FileZilla or FTP client of your choosing to login to your pi (similar to PuTTY but can't use the command line) and transfer your custom files into the proper directories. Transfer snowboy.py and snowboydecoder.py into ~/snowboy directory. Make sure your three .wav files for your personal models are in the ~/snowboy directory too. Your response sounds, .pmdl, and/or .umdl should be in the ~/snowboy/resources directory.
You will need to use and edit the attached snowboy.py and snowboydecoder.py for this to work. Run this command in snowboy directory to test out your completed setup:
```
python2 snowboy.py 
```
##CUSTOMIZING SNOWBOY IN COMMAND LINE
Copy training_service.py to the snowboy directory. Log into https://snowboy.kitt.ai, click on “Profile settings”, and copy your API token. You will need to modify some lines of code in training_service.py with your own token, hotword, etc. Use the following command to record 3 wav files of your hotword to the same directory
```
rec -r 16000 -c 1 -b 16 -e signed-integer FILENAME.wav
```
Run the following command to generate a pmdl
```
python training_service.py 1.wav 2.wav 3.wav saved_model.pmdl
```
Move saved_model.pmdl to ~/snowboy/resources/ (rename for easier recall later) with command
```
mv saved_model.pmdl ~/snowboy/resources/ 
```
Run the demo to ensure it is working properly with command
```
python demo.py ~/snowboy/resources/saved_model.pmdl
```
##ADDITIONAL NOTES
IF you need to run snowboy automatically on system boot like me the best way was to use crontab http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/ .bashrc and systemd were not working for me. You might have better luck, but crontab worked for this project and settings. This guide
##TROUBLESHOOTING
I experienced a sampling error IOError -9777 when trying to run snowboy on system boot. This is most likely caused by using the Raspberry Pi Zero's usb for mic in and audio out. This was fixed by editing alsa config file with command 
```
sudo nano /usr/share/alsa/alsa.conf
```
And changing the lines
```    
    defaults.ctl.card 0
    defaults.pcm.card 0
```
to 1's.
I mostly followed wanleg's snowboyPi guide https://github.com/wanleg/snowboyPi and referenced the official Snowboy site http://docs.kitt.ai/snowboy/ so you can reference these too if you run into trouble. I was not able to find a guide to get an offline voice detection software like Snowboy running on a Raspberry Pi Zero so I decided to document my own process.

######To do
- [ ] Find way to stop crontab service once in command line in order to work on project
- [ ] Take out "stop" verbal command or find way to make it actually stop the audio playback
- [ ] Get GPIO activating with each song (for personal project)
- [ ] Get GPIO dewdrop customized lightshow for each voice command (for personal project)
- [ ] Solder LIP SHIM to accompanying pins (for personal project)