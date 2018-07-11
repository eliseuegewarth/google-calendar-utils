"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

def list_events(calendar, num_events=15):

    # Call the Calendar API
    num_events = int(num_events)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming {} events'.format(num_events))
    events_result = service.events().list(calendarId=calendar['id'], timeMin=now,
                                          maxResults=num_events, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def create_event(calendar):

    event = {
      'summary': 'Testinho',
      'description': 'Teste Google Calendar API.',
      'start': {
        'date': '2018-07-10',
        'timeZone': calendar['timeZone'],
      },
      'end': {
        'date': '2018-07-10',
        'timeZone': calendar['timeZone'],
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId=calendar['id'], body=event).execute()
    print(
        "Event created: {}".format(
            event.get('htmlLink')
            )
        )

def list_calendars():
    page_token = None
    have_next = True
    calendars = []
    while have_next:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendars.append(calendar_list_entry)
            page_token = calendar_list.get('nextPageToken')
        if not page_token:
            have_next = False
    return calendars

def get_calendar(name=None):
    calendars = list_calendars()
    calendar = {
        'summary': "primary",
        'id': 'primary'
    }
    if name:
        for current_calendar in calendars:
            if name == current_calendar['summary']:
                calendar = current_calendar
                break
    else:
        # Do nothing
        pass
    return calendar

def main():
    print("1 List events")
    print("2 List calendars")
    print("3 Create events")
    option = input("Choose:")
    if "2" in option:
        list_calendars()
    elif "3" in option:
        create_event(get_calendar("eliseuegewarth@gmail.com"))
    else:
        list_events(get_calendar("eliseuegewarth@gmail.com"))
if __name__ == '__main__':
    main()