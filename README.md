Parrot.PY tryout pack
-----

This folder contains a set of files to get a first glimpse of what Parrot can do without having to do all the training, setup and so on that making your own personalized model requires you to do.
Inside there is noise model ( tested on Parrot v0.12.0 ) and a mode that allows you to click, right click and scroll using noises.

The noise model is trained on my voice alone using one microphone, so your mileage will vary. 
Personal models trained on your voice and microphone will vastly improve your experience.

Setup
----

After you have installed Parrot.PY according to the setup instructions, select all the files inside this folder, copy them and then paste them inside the data folder in Parrot.
When you next run play.py, you should be able to get it up and running.

Usage
----

- Left click: Make a clucking sound with your tongue.
- Right click: Make a tut-tut sound ( press the tip of your tongue up against the back of your teeth and pull back )

To enable scrolling for a short period, make the following clicking sound: Press the tip of your tongue against the middle of the roof of your mouth, and pull down.

- Scroll down: Use a shushing sound
- Scroll up: Make an F sound ( blowing through your teeth )

You can stop scrolling at any time by making any click sound.

You can change the sounds around to your liking by changing code/mode_starter.py.

Trouble shooting
----

If you need to make really loud sounds to make the clicks work, try setting the POWER_SCALING value on line 6 in code/mode_starter.py to a lower value than 1000.
I recommend setting it to 900, then trying it out again. If it still doesn't pick sounds up, lower it again. 
But note that every time you make it lower, you also increase the risk of clicks being fired when you do not want to.

If the scrolling is too fast, try changing the SCROLL_SCALING value on line 10 of code/mode_starter.py to something lower than 20. 
On Linux I did manage to make the scroll work, but it does have a litte jank on the tail end of scrolling.