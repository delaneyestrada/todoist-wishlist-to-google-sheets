from keys import keys
import todoist
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '12y0aw7BuNAyB9llaGmr1CxHH4Sfk1x6RlIdGQKRtHa0'
RANGE_NAME = 'Wishlist!A1'

"""Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

# Set up Sheets API
sheet = service.spreadsheets()
    



todoist_api = todoist.TodoistAPI(keys["todoist"])
todoist_api.sync()

wishlists = []

for project in todoist_api.state['projects']:
    if str(project['parent_id']) == "1799452428":
        wishlists.append(str(project["id"]))

sheets_array = []
for list in wishlists:
    item_array = []
    for item in todoist_api.state['items']:
        if str(item['project_id']) == list:
            content = item['content']
            regex = r'\[.*?\]\(.*?\)'
            if re.search(regex, content) != None:
                regex = r'\{.*?\}'
                name = re.sub(r'[\[\]]|\{.*?\}.*', "", content)
                link = re.sub(r'.*?\(|\)', "", content)
                sheets_hyperlink = '=HYPERLINK("' + link + '", "' + name + '")'
                #print("NAME: " + name + " LINK: " + link + " SHEETS_HYPERLINK: " + sheets_hyperlink)
                if price := re.search(regex,content):
                    item_array += [[sheets_hyperlink, price.group()[1:-1]]]
                else:
                    item_array += [[sheets_hyperlink]]
            else: 
                # Add to array with no price
                item_array += [[content]]
    # Add to sheets array
    sheets_array.append([">>>>>>>>>>>"])
    sheets_array += item_array
print(sheets_array)
body = {
    'values': sheets_array
}

result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
    valueInputOption="USER_ENTERED", body=body).execute()