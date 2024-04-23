import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]


def remove_files(folder_path):
	files = os.listdir(folder_path)

	if files:
		for filename in files:
			if os.path.isfile(os.path.join(folder_path, filename)):  # Check if it's a file
				os.remove(os.path.join(folder_path, filename))
				# print(f"Removed file: {filename}")
	else:
		print(f"The folder {folder_path} is empty.")


def main():
	"""Shows basic usage of the People API.
	Prints the name of the first 10 connections.
	"""
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				"credentials.json", SCOPES
			)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open("token.json", "w") as token:
			token.write(creds.to_json())

	try:
		service = build("people", "v1", credentials=creds)

		# Call the People API
		results = (
			service.people()
			.connections()
			.list(
				resourceName="people/me",
				pageSize=200,
				personFields="names,birthdays,emailAddresses,phoneNumbers"
			)
			.execute()
		)
		connections = results.get("connections", [])
		mypeople = {}
		for person in connections:
			name = person['names'][0]["displayName"]
			bday = person['birthdays'][0]['date']
			birthday = f"{bday['day']}-{bday['month']}-{bday['year']}"
			email = person['emailAddresses'][0]['value']
			phone = person['phoneNumbers'][0]['value']
			mypeople[person['names'][0]['metadata']['source']['id']] = [name, birthday, email, phone]

		import json

		with open("mycontacts.json", "w") as f:
			json.dump(mypeople, f, indent=4)

		print("Contacts saved successfully!")

	except HttpError as err:
		print(err)


if __name__ == "__main__":
	main()
