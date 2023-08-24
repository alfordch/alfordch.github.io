# Main script to Upload WCBN 'Live from the Dungeon' Playlists and Recordings to Personal Google Drive 

from __future__ import print_function
from datetime import datetime
from bs4 import BeautifulSoup
import playlist_util as util
import site_update as sup
import requests


# Date/Season info
season = "(4) "


# WCBN archive login:
# Note: This is incredibly insecure and would be mocked by any cybersecurity nerd. I, however, am not one such nerd and anticipate that noone is trying to hack into WCBN archives
floyd_login = util.getFloydLogin()


# Drive info: 
New_folder_ID = ''


# Connect to spinitron public and get playlists links and dates
url_spinitron = 'https://spinitron.com/WCBN/show/249781/Live-from-the-Dungeon'


# Establish initial soup connection
response = requests.get(url_spinitron)
if response.status_code == 200:
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
else:
    print(f"Failed to fetch the URL. Status code: {response.status_code}")


# Content holds the episode dates in string form
content = util.getEpisodeDates(soup)


# Get links to public pages of all shows
playlist_links = util.getEpisodeLinks(soup, url_spinitron)


# Get the link to the most recent show
# (Make the string)
year = str(content[0].year)
month = str(content[0].month)
day = str(content[0].day)
time = content[0].hour * 100
time = str(time)
date = month + "/" + day + "/" + year

if int(month) < 10:
     month = "0" + month

if int(day) < 10:
     day = "0" + day

url_playlist = "https://floyd.wcbn.org/arc/" + year + "/" + year + "-" + month + "/" + year + "-" + month + "-" + day + "/wcbn-" + year + "-" + month + "-" + day + "-" + time + "-EDT.mp3"
mp3_filename = "./wcbn-" + year + "-" + month + "-" + day + "-" + time + "-EDT.mp3"
file_extension = '.mp3'  


# Connect to floyd to get archive mp3
r = requests.get(url_playlist, auth=(floyd_login['user'], floyd_login['pass']))


# Get title of most recent episode
recent_link = playlist_links[0]
recent_get = requests.get(recent_link)


# Make new soup obj for public page of recent episode
soup = BeautifulSoup(recent_get.content, 'html.parser')


# Prep lists for .txt writing
episode_name_list = util.getEpisodeName(soup)
description = util.getEpisodeDescription(soup)
artist_names = util.getContentList('artist', soup)
song_names = util.getContentList('song', soup)
album_names = util.getContentList('release', soup)
release_years = util.getContentList('released', soup)
label_names = util.getContentList('label', soup)
folder_name = season + str(content[0].month) + "/" + day + "/" + year[2:] + " " + episode_name_list[0]


# Begin printing a .txt file to house the playlist 
playlist_txt_name = episode_name_list[0][:-1] + '.txt'
playlist_txt = open(playlist_txt_name, 'w')
playlist_txt.write(episode_name_list[1] + '\n\n')
playlist_txt.write(description[:-14] + '\n\n' + description[-14:] + '\n\n')
for i in range(len(song_names)):
     playlist_txt.write(str(i + 1) + '. ' + artist_names[i] + ' / ' + song_names[i] + ' / ' + album_names[i] + ' / ' + release_years[i] + ' / ' + label_names[i] + '\n')
playlist_txt.close()


# If extension does not exist in end of url, append it
if file_extension not in url_playlist.split("/")[-1]:
    filename = f'{url_playlist}{file_extension}'
# Else take the last part of the url as filename
else:
    filename = url_playlist.split("/")[-1]

with open(filename, 'wb') as f:
    # You will get the file in base64 as content
    f.write(r.content)


# Print short message to cl to show correct/most recent episode
try:
    util.prSuccess("Found most recent episode: ")
    print(folder_name)

except:
    util.prError("Could not find recent episode\n")


# Do the functions for drive archive
try:
    playlist_folder_ID = util.createRemoteFolder(folder_name, util.folderID)
    playlist_mp3_ID = util.uploadFile(playlist_folder_ID, filename, 'audio/mp3')
    playlist_txt_ID = util.uploadFile(playlist_folder_ID, playlist_txt_name, 'text/plain')
    util.prSuccess("Archival complete: ")
    print(datetime.now().strftime("%-m/%-d/%Y %H:%M:%S"))

except:
    util.prError("Error when attempting to upload to Google Drive:\n")
    util.printErrorMsg('arch')


# Do the functions for email distribute
try:
    util.distribute(playlist_mp3_ID, date)
    util.prSuccess("Distribution complete: ")
    print(datetime.now().strftime("%-m/%-d/%Y %H:%M:%S"))

except:
    util.prError("Error when attempting to distribute via email\n")
    util.printErrorMsg('dist')


# Do functions from site_update to update the site

# Print status message
util.prSuccess("Beginning updates to www.livefromthedungeon.net\n")

# Make the link for the audio element
downloadLink = sup.makeDownloadLink(playlist_mp3_ID)

# Make the title for the <h4> header
titStr = str(content[0].month) + "/" + day + "/" + year[2:] + " " + episode_name_list[0]

# Run the functions from sup to do the index/archive updates
sup.update_index(downloadLink, description, titStr, recent_link)
sup.update_archive(downloadLink, description, titStr)
sup.update_driver()