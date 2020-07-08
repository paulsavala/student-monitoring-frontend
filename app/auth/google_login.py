import requests
import os
from oauthlib.oauth2 import WebApplicationClient
from flask import request
import json


# Google login urls
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def google_login_request_uri():
    # Get Google login endpoint
    google_provider_cfg = get_google_provider_cfg()
    auth_endpoint = google_provider_cfg['authorization_endpoint']

    # Construct Google login request
    request_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return request_uri


def process_google_login_callback():
    # Get auth code from Google
    code = request.args.get('code')

    # Get Google token endpoint
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Get userinfo endpoint
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Check if user's Google account is verified, then grab userinfo
    if userinfo_response.json().get("email_verified"):
        user_id = userinfo_response.json()["sub"]
        email = userinfo_response.json()["email"]
        profile_pic = userinfo_response.json()["picture"]
        name = userinfo_response.json()["given_name"]
        return {'user_id': user_id, 'email': email, 'profile_pic': profile_pic, 'name': name}
    else:
        return None
