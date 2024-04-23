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


def download_photo(url, filename):
	"""Downloads a photo from a URL and saves it locally.

	Args:
	url: The URL of the photo to download.
	filename: The filename to save the downloaded photo as.

	Returns:
	True if download is successful, False otherwise.
	"""
	try:
		response = requests.get(url, stream=True)
		if response.status_code == 200:
			with open(filename, 'wb') as f:
				for chunk in response.iter_content(1024):
					f.write(chunk)
			return True
		else:
			print(f"Failed to download photo: {response.status_code}")
			return False
	except requests.exceptions.RequestException as e:
		print(f"Download error: {e}")
		return False


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
				personFields="names,photos",
			)
			.execute()
		)
		connections = results.get("connections", [])

		remove_files("mypeople")
		for person in connections:
			# print(person)
			photo = person.get("photos", [])[0]
			if not photo.get('default'):
				url = photo.get("url")[:-5]
				name = person.get("names", [])[0].get("displayName")
				print(name, url)
				download_photo(url, f"mypeople/{person['names'][0]['metadata']['source']['id']}.jpg")
	except HttpError as err:
		print(err)


if __name__ == "__main__":
	main()
