import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.conf import settings
from datetime import datetime
import pytz
import logging
from django.utils import timezone


SCOPES = ['https://www.googleapis.com/auth/calendar']

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def get_calendar_service():
    creds = None
    token_path = os.path.join(settings.BASE_DIR, 'token.json')
    creds_path = settings.GOOGLE_CLIENT_SECRETS_FILE

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            flow.redirect_uri = 'http://localhost:8000/oauth2callback/'
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_calendar_event(appointment):
    service = get_calendar_service()

    # Ensure timezone-aware datetimes
    start_datetime = datetime.combine(appointment.appointment_date, appointment.start_time)
    end_datetime = datetime.combine(appointment.appointment_date, appointment.end_time)
    start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
    end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())

    start_time_str = start_datetime.isoformat()
    end_time_str = end_datetime.isoformat()
    print(start_time_str, end_time_str)
    event = {
        'summary': f'Appointment with Dr. {appointment.doctor.user.username}',
        'start': {
            'dateTime': start_time_str,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time_str,
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [
            {'email': appointment.doctor.user.email},
            {'email': appointment.patient.user.email},
        ],
    }

    logging.debug(f"Event to be created: {event}")

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        logging.info(f"Event created: {event}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise e

    return event
