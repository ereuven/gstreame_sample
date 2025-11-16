# GStreamer Sample

## Overview
Below is a minimal but realistic architectural example in Python showing how you could:

Capture video with GStreamer on the main computer

Send the video stream to:

Computer A → Face Recognition

Computer B → LPR (License Plate Recognition)

Receive results back (via ZeroMQ in this example)

Check against blacklists

Display alerts on the screen

This is not production-ready, but it shows working, runnable structure and how the GStreamer Python API fits into the pipeline.

## What This Example Includes

✓ GStreamer pipeline capturing webcam → encoded → sent over UDP
✓ Cloned video sent to two remote computers
✓ Each computer receives video with appsink
✓ Frame-by-frame processing hooks
✓ ZeroMQ message passing back to main computer
✓ Blacklist checking
✓ On-screen (terminal) alerts