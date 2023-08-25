# Script to send the recording of 'WCBN: Live from the Dungeon' 

# libraries to be imported
from googleapiclient.http import MediaFileUpload
from email.mime.multipart import MIMEMultipart
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from urllib.parse import urljoin
from httplib2 import Http
import datetime
import smtplib
import getpass
import sys

# All the stuff below is for uploading to Google Drive folder
SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive_service = build('drive', 'v3', http=creds.authorize(Http()))


if sys.argv[0] == 'playlist_main.py':
    # Get recipient emails from cl
    toaddr = sys.argv[4:]

    # Get folder ID from cl
    folderID = sys.argv[3]
    
    # Get archive number from cl
    archno = sys.argv[2]

    # Get season from cl
    season = sys.argv[1]


# Define a few printing style functions
def prSuccess(in_string): print("\033[92m{}\033[00m".format(in_string), end="")
def prError(in_string): print("\033[91m{}\033[00m".format(in_string), end="")


# Define the utility functions for playlist_main.py

def distribute(file_ID, date):
    fromaddr = input("Sender email address: ")

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = ", ".join(toaddr)

    # storing the subject
    msg['Subject'] = "WCBN Live from the Dungeon Recording " + date

    # make link to file
    link = 'https://drive.google.com/file/d/' + file_ID + '/view?usp=drive_link'

    # string to store the body of the mail
    body = "See attached and the below link to this week's Live from the Dungeon recording. Live from the Dungeon archives are now also hosted on https://www.livefromthedungeon.net.\n\n" + link

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, password=getpass.getpass('Password for ' + fromaddr + ': '))

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


def uploadFile(folder_ID, up_filename, type):
    file_metadata = {
    'name': up_filename,
    'mimeType': type,
    'parents': [folder_ID]
    }
    media = MediaFileUpload(up_filename,
                            mimetype=type,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Make sure file has the correct permissions to update the webpage without manually
    # changing permissions
    permission = {
        'role': 'reader',
        'type': 'anyone'
    }
    drive_service.permissions().create(
        fileId=file['id'],
        body=permission
    ).execute()

    return file.get('id')


def createRemoteFolder(folderName, parentID):
    # Create a folder on Drive, returns the newely created folders ID
    body = {
        'name': folderName,
        'mimeType': "application/vnd.google-apps.folder"
    }
    if parentID:
        body['parents'] = [parentID]
        root_folder = drive_service.files().create(body = body).execute()
        return root_folder.get('id')


def getContentList(name_class, soupOBJ):
    contentList = soupOBJ.find_all(class_=name_class)
    contentList = [item.get_text() for item in contentList]
    return contentList


def getEpisodeDescription(soupOBJ):
    description = soupOBJ.find(class_='episode-description').get_text()
    return description


def getEpisodeLinks(soupOBJ, url_spinitron):
    main_element = soupOBJ.find(class_="list-view playlist-list")
    anchor_tags = main_element.find_all('a')
    playlist_links = [anchor.get('href') for anchor in anchor_tags]
    playlist_links = [urljoin(url_spinitron, href) for href in playlist_links]
    return playlist_links


def getEpisodeName(soupOBJ):
    # [ (0) episode name, (1) episode name for .txt ]
    episode_name = episode_name_for_txt = soupOBJ.find(class_='episode-name').get_text()
    episode_name = episode_name.split('(', 1)[0]
    episode_name_list = [episode_name, episode_name_for_txt]
    return episode_name_list


def getEpisodeDates(soupOBJ):
    main_element = soupOBJ.find(class_="list-view playlist-list")
    content = []

    if main_element:
        datetime_elements = main_element.find_all(class_="datetime playlist")
        if datetime_elements:
            for element in datetime_elements:
                content.append(element.get_text()) 

    i = 0
    while  i < len(content):   
        # Get the entire list of playlists dates as datetime objects
        content[i] = content[i][1:]
        content[i] = content[i][:-1]
        content[i] = content[i].replace("th"," ").replace("st"," ").replace("rd"," ").replace(" PM","PM").replace(" AM","AM")
        content[i] = content[i][:3] + " " + content[i][3:]
        content[i] = content[i][:content[i].find('2023') + 4] + " " +  content[i][content[i].find('2023') + 4:]
        content[i] = content[i][:content[i].find('2022') + 4] + " " +  content[i][content[i].find('2022') + 4:]
        content[i] = datetime.datetime.strptime(content[i], '%b %d %Y %I:%M%p')
        i += 1
    
    return content


def printErrorMsg(errType):
    if errType == 'dist':
        print('If you are sure your login credentials are correct, this could be due to (1) your gmail account has two-factor-authentication enabled or (2) your gmail account does not allow less secure apps, see https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MHGUS36bnI6VCV3r-Ttgk0WeGUf9go9hrbZwl6cXFKUsC7XNz-G-plCOqYRNplxXAGvHvIwc6jJZvtsm_GUJ0gVOwL5g for more information on (2)')

    elif errType == 'arch':
        print('This could be due to (1) issues with authentication for Google Service API or (2) issues with validating your credentials.json, see https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf for more information on (1)')


def getFloydLogin():
    auth_pair = {}
    auth_pair['user'] = input('WCBN archive username: ')
    auth_pair['pass'] = getpass.getpass('WCBN archive password: ')
    return auth_pair


# def xyz(in_abc):
#   ...