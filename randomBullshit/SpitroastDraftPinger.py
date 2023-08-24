from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import discord
import asyncio

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1JT5zDoT9ind7NOgk_MF4MkI-9R97JKForhYxSEYSKs0'
SAMPLE_RANGE_NAME = 'Draft!F1'
LAST_PICK_TEXT = 'Draft!P23'
OTHER_LAST_PICK = 'Draft!P24'

RUN_THIS = True

CHANNEL_TO_SEND = 978083163249201162;
PLAYERS_DICT = {"Gal" : 127673716657225728,
				"Leaf" : 187785792897155072,
				"James" : 218922505891610624,
				"Devin" : 116791562322575361,
				"Vincent" : 221763209479192577,
				"Benny" : 226603911832666112,
				"Miles" : 218920440297553920,
				"Caleb" : 80546742629564416}


async def start_spitroast_pinger(bot):
	"""Shows basic usage of the Sheets API.
	Prints values from a sample spreadsheet.
	"""
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	oldId = ""
	channel = bot.get_channel(CHANNEL_TO_SEND)
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
	# Save the credentials for the next run
	with open('token.json', 'w') as token:
		token.write(creds.to_json())


	# Call the Sheets API
	service = build('sheets', 'v4', credentials=creds)
	# loop this shit to update every hour and notify bullshit andys
	sheet = service.spreadsheets()
	while(RUN_THIS):
		try:
			result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
								range=SAMPLE_RANGE_NAME).execute()
			last_pick = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
								range=LAST_PICK_TEXT).execute()
			last_pick2 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
								range=OTHER_LAST_PICK).execute()

			values = result.get('values', [])
			userId = PLAYERS_DICT[values[0][0]]
			lastpick = last_pick.get('values', [])[0][0]
			lp = ""
			lp2 = ""
			if lastpick != None:
				lp = lastpick[0][0]
			lastpick2 = last_pick2.get('values', [])[0][0]
			if lastpick2 != None:
				lp2 = lastpick2[0][0]

			if oldId != userId:
				oldId = userId
				await send_nudes(userId, channel, lp, lp2)

		except HttpError as err:
			print(err)
		
		await asyncio.sleep(300)

async def send_nudes(userId, channel : discord.channel.TextChannel, last_pick, lp2):
	await channel.send(f"<@{userId}> its your turn to pick now bruv. Last picks were {last_pick}, {lp2}.\n[Draft](<https://docs.google.com/spreadsheets/d/1JT5zDoT9ind7NOgk_MF4MkI-9R97JKForhYxSEYSKs0/edit#gid=1822506900>) [Cube](<https://www.cubecobra.com/cube/list/8gv?view=spoiler&scale=small>)")
	
