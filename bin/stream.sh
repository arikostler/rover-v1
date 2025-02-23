#!/bin/sh

raspivid -t 0 -w 1280 -h 720 -ih -fps 20 -o - | nc -k -l 2222

# To watch stream on computer...
# mplayer -fps 200 -demuxer h264es ffmpeg://tcp://192.168.0.6:2222
