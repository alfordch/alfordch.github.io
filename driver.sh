#!/bin/bash

# argv[1] : season #
# argv[2] : archive #
# argv[3] : Google Drive main folder ID
# argv[2:] : recipient_1 recipient_2 ... recipient_n
python3 playlist_main.py 4 42 1kwPUJgdmGOel56ipOVQtL7MKaeauZRPz charles.alfordiv@gmail.com 

# Run cleanup to get rid of the recording and playlist locally
bash clean_up
