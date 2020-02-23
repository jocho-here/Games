# Gamble
Gambling money tracking server in Korean

# How did I start this project?
My family and I were traveling Seoul for several days.  One night, we decided to play the game  
Hoolah (훌라) with a deck of cards, as usual.  While we had the cards, we didn't have enough  
coins to gamble (by the way, we don't gamble seriously.  We normally play with coins so we have  
that feeling of actually earning some tangible items).  My dad started to ask for some ideas but  
none had any good idea.  I realized I brought my laptop so I started coding this gambling  
tracker with Python and Flask.  
It started off with set of users and set of money they started out with.  Nothing was  
configurable nor scalable since I just needed a quick solution.  Not a great UI either.  
However, my family enjoyed playing with this cyber money with the tracker and asked me to  
enhance some visibility and functionality so I decided to just open source this and let others  
to use it as well.

# How to use this
My original way of using this Flask server was by having each player's smartphone to be  
connected to the same network as the laptop that's running the server.  Then, with the laptop's  
local IP, access the server from each player's smartphone (e.g. go to http://172.0.0.1:8000/).  
Then, start playing!

# Bug
- Experienced repeated request made from a smartphone's web browser.  It was fixed when the  
player played in incognito.

# TODO
- This repository will be removed as soon as byeolook goes alive
