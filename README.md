This app demonstrates how to integrate with Google Calendar using the Google API Client Library for python  and OAuth2 for authentication.

# Requirements
Python Django A Google API Console project with the Google Calendar API enabled A client ID and client secret for your project A redirect URI for your app

# **Getting Started**
Clone or download the repository. Run pip install to install the required dependencies. Start the app with python manage.py runserver localhost:8000 Visit http://localhost:8000/rest/v1/calendar/init in your web browser to start the OAuth2 flow. Follow the prompts to grant access to your Google Calendar. The app will redirect to http://localhost:8000/rest/v1/calendar/redirect with an authorization code. The app will then use the authorization code to get the access token and retrieve a list of events from your Google Calendar. The list of events will be displayed in the browser.

# Views
/rest/v1/calendar/init: This view starts the OAuth2 flow by redirecting the user to the authorization URL.
/rest/v1/calendar/redirect: This view handles the redirect from Google with the authorization code. The view uses the authorization code to get the access token and retrieve a list of events from the user's Google Calendar.

# Conclusion
This app demonstrates how to use the googleapis library to implement Google Calendar integration using OAuth2 for authentication. By using this app as a starting point, you can build your own app that integrates with Google Calendar in a secure and reliable way.
