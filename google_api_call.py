from apiclient import discovery
from google.oauth2 import service_account


def credentials_from_file(scopes, client_secret_file):
    credentials = service_account.Credentials.from_service_account_file(
        client_secret_file, scopes=scopes)

    return credentials


def Create_Service(client_secret_file, api_name, api_version, scopes):
    credentials = credentials_from_file(scopes, client_secret_file)
    service = discovery.build(api_name, api_version, credentials=credentials)
    return service
