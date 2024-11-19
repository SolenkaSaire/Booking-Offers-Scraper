from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

# Define los scopes necesarios
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Autentica al usuario y guarda el token."""
    creds = None
    # Si existe un archivo token.json, carga las credenciales guardadas
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si no existen credenciales válidas, solicita autorización al usuario
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales en token.json
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("Autenticación exitosa. Token guardado.")

if __name__ == '__main__':
    main()
