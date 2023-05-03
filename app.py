from flask import Flask, request
from dotenv import load_dotenv
import requests
import json
import os

app = Flask(__name__)



load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def add_user_to_server(token: str, user_id: str, server_id: str, access_token: str) -> bool:
    url = f'https://discordapp.com/api/v8/guilds/{server_id}/members/{user_id}'
    headers = {
        'Authorization': f'Bot {token}'
    }

    data = {
        "access_token": access_token
    }

    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f'User {user_id} added to server with ID {server_id}')
        return True
    else:
        print(f'Error adding user {user_id} to server with ID {server_id}')
        return False



# The callback URL for OAuth2 authorization
@app.route('/auth/callback')
def callback():
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    url = 'https://discord.com/api/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': '1101425504642404352',
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:5000/auth/callback',
        'scope': 'identify guilds.join'
    }
    response = requests.post(url, headers=headers, data=data).json()
    access_token = response['access_token']

    # Get the user ID from the access token
    url = 'https://discord.com/api/users/@me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers).json()
    user_id = response['id']

    # Add the user to the server
    invite_code = '1075365992399650836'
    bot_token = BOT_TOKEN
    add_user_to_server(bot_token, user_id, invite_code, access_token)

    return f'Authorised with Discord, adding user {user_id} to server {invite_code}'

if __name__ == '__main__':
    app.run(debug=True)