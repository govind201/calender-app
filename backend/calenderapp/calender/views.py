from django.urls import reverse
from google.oauth2.credentials import Credentials
from django.conf import settings
from django.shortcuts import redirect
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views import View
from google_auth_oauthlib.flow import Flow
from googleapiclient.errors import HttpError



def welcome(request):
    return HttpResponse("Welcome to my Google Calendar integration app!")


GOOGLE_CLIENT_CONFIG = {
        "web": {
            "client_id": "792384898936-17eq4677ondom7fk2i7bqbai5dvh55vu.apps.googleusercontent.com",
            "client_secret": "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",
            "redirect_uris": ["http://localhost:3000"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "userinfo_uri": "https://www.googleapis.com/oauth2/v1/userinfo",
            "scope": [
                "https://www.googleapis.com/auth/calendar.readonly"
            ]
        }
    }
GOOGLE_CALENDAR_SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly"
    ]
google_auth_state = None
class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_config(
            GOOGLE_CLIENT_CONFIG,
            scopes=GOOGLE_CALENDAR_SCOPES,
            redirect_uri = "http://localhost:3000"
        )

        authorization_url, state = flow.authorization_url(
            access_type="offline",
        )
        return HttpResponseRedirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Specify the state when creating the flow in the callback so that it can
        # verify the authorization server response.
        # state = google_auth_state 
        # print('state', state, request.session.get('code'), request.session.get('state'))
        # if state is None:
        #     return HttpResponseBadRequest("Invalid state parameter")

        flow = Flow.from_client_config(
            GOOGLE_CLIENT_CONFIG,
            scopes=GOOGLE_CALENDAR_SCOPES,
            redirect_uri = "http://localhost:3000",
        )

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.build_absolute_uri()
        try:
            flow.fetch_token(authorization_response=authorization_response)
        except Exception as e:
            return HttpResponseBadRequest(f"Failed to fetch token: {e}")

        # Save the credentials in session for the user.
        credentials = flow.credentials
        request.session["google_credentials"] = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }

        # Get the list of events in the user's calendar.
        try:
            service = build("calendar", "v3", credentials=credentials)
            events_result = service.events().list(calendarId="primary", timeMin="2023-01-01T00:00:00Z", maxResults=10, singleEvents=True, orderBy="startTime").execute()
            events = events_result.get("items", [])
        except HttpError as error:
            return HttpResponseBadRequest(f"An error occurred: {error}")

        # Return the list of events in JSON format.
        return JsonResponse(events, safe=False)
