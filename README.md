# youtube-clustering

This is a Python program to automatically create youtube playlists given a channel. The program uses Latent Dirichlet Allocation to create the playlists.
For a more in depth explanation, click [here](https://antonfjohansson.github.io/blog/youtube-clustering/).

If you want to use the program, you first need to get authorization access to the youtube-api. You can follow the instructions [here](https://developers.google.com/youtube/registering_an_application) to obtain it.

The program is used as follows:
1.  Go to the youtube channel where you want to create the playlists.
2.  Find the channel id for that channel. This can either be the last part of the URL or you can find it by right clicking the webpage, press "Inspect" and find "externalID". The code next to "externalID" is the channel-id.
3.  Open main.py, insert the channel-id into "video_channel_id". Choose the number of playlists with "num_playlists".
4.  Run the program and wait. The result will be saved down in the designated folder.







