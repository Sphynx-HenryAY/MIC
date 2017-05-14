# MultimediaInCommunication
Goal: Throw away Browsers, Contents Only.

This project is to develop a platform that let user break the wall between human, machine, and network. Let user reach/read their target information directly in their daily messaging app. 
It is started with WeChat, with the use of graceful API created by ItChat and you can reach that through my repository. :)

-*-Progress-*-
This project is developed under Python3, with the newest version 3.7

The program is still under development. Currently provides the search of web site links of:
- Baidu (the biggest Chinese Searching engine)
- Youku (one of the biggest video sharing platform in China)
Links are fetched directly in the searching page using Python Regex module. Searching modules are included in folder "search".

As there is a file transmission limitation of 20 MB in WeChat; and normally only video files transmission would reach this limit, a basic video processing module is included: video.VideoAccess. This module provides two ways to access to video file:
- Provides the name of video for manual control
- Provides a dictionary containing output setting for automation usage
This module based on opencv and ffmpeg and provides only basic function at the stage. Other functions are palnned and under development.
