# Script to update the livefromthedungeon.net sit with most recent recording and playlist

# Pages/Files to be updated:
#   index.html
#   archive.html

import playlist_util as util


# Get Google Drive link for the audio src on site
def makeDownloadLink(fileID):
    dlLink = "https://drive.google.com/uc?export=download&id=" + fileID
    return dlLink


# Opening <p> tag: index 70 (archive.html ln 71)
def update_archive(dlLink, description, titStr):
    with open('archive.html', 'r') as file:
        data = file.readlines()

    # Get the two halves of the archive html that we need
    dataFirstHalf = data[:70]
    dataSecondHalf = data[70:]
    dataNew = []
    
    # Write to dataNew
    dataNew.append('                <div class="archive' + util.archno + '">\n')
    dataNew.append('                    <h3><a href=' + dlLink + '>' + titStr[:-1] + ':</a></h3>\n')
    dataNew.append(    '                    ' + description[:-14] + ' <br> <br>\n')
    dataNew.append('                    <audio controls>\n')
    dataNew.append('                        <source src=' + dlLink + ' type="audio/mpeg">\n')
    dataNew.append("                        Your browser does not support the audio element.\n")
    dataNew.append("                    </audio> <br> <br>\n")
    dataNew.append("                </div>\n\n")

    # Concatenate the three lists
    data = dataFirstHalf + dataNew + dataSecondHalf

    # Write to the archive file
    with open('archive.html', 'w') as file:
        file.writelines(data)


# Div class: index 74 (index.html ln 75)
# Episode title: index 75 (index.html ln 76)
# Episode description: index 76 (index.html ln 77)
# Episode mp3 GDrive link: index 78 (index.html ln 79)
# Spinitron playlist link: index 86 (index.html ln 87)
def update_index(dlLink, description, titStr, spinLink):
    with open('index.html', 'r') as file:
        data = file.readlines()
    
    # Edit the div class string
    divStr = data[74][:27] + str(util.archno) + '">\n'
    data[74] = divStr

    # Edit the episode title string
    data[75] = "            <h3><a href=" + dlLink + ">" + titStr[:-1] +":</a></h3>\n"

    # Edit the episode description
    description = description[:-14] + " <br><br>\n"
    data[76] = data[76][:12] + description

    # Edit the mp3 GDrive link
    data[78] = data[78][:28] + '"' + dlLink + '" type="audio/mpeg">\n'

    # Edit the Spinitron link
    data[86] = data[86][:20] + '"' + spinLink + '" width="100%" height="500rem"></iframe>\n'

    with open('index.html', 'w') as file:
        file.writelines(data)


# Change the archno in the driver, so the next run of the update will include the correct number
def update_driver():
    with open('driver.sh', 'r') as file:
        data = file.readlines()

    data[6] = 'python3 playlist_main.py ' + util.season + ' ' + str(int(util.archno) + 1) + ' ' + util.folderID + ' '
    for item in util.toaddr:
        data[6] = data[6] + str(item) + ' '
    
    data[6] = data[6] + '\n'
    with open('driver.sh', 'w') as file:
        file.writelines(data)