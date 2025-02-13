# lastfm-reporter

tl;dr - It's like every other LastFM history tool but this will give me what I want. 

## what's the deal with this?
I started using LastFM and I think it's super cool but I haven't found any tool that really gives me the right combination of what I want to know from all the data. The best example I can give is that I primarily listen to music by listening to albums in completion. It's cool to know how many times I listened to tracks off albums but actually what I really care about is how many times I listened to an album in completion. 

So like any good developer, I said "wow people have made tools before me, I can do it just like them!!" and now I'm making my own history analysis reporter tool or whatever you want to call it 

## what does the desired end state look like?
I want to make an monthly report image that I can share, just like how [Musicorum](https://musicorumapp.com/generate) does it. This is either going to be the thing that feeds that image creator or will create the image itself. Dunno how any of that works just yet, but we'll get there.


## technical stuff
### what are you making it with?
Python + [pyLast](https://github.com/pylast/pylast)

### how do I use it?
TBD, I'm sure it's something like 
```
python3 script.py
```

Make sure you've got a .env file that has the right values. You get key+secret from LastFM, duh.
```
LASTFM_USERNAME=bigdog
PASSWORD_HASH=bigdogbuthashed
API_KEY=bigdogapikey
API_SECRET=bigdogapisecret
```


### anything else?
If you are reading this and you're not me, I'm guessing you're one of two people. You're either a friend who I'm talking to and giving you the runthrough myself, or you're sussing me out for a work related thing like an interview.

If you're the latter, hey I promise my work is usually a lot more higher quality than this but I'd love to talk to you about how I made this because I love to chat! 