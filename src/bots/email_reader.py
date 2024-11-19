from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import re
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_verification_link(user_email):
    creds = None
    if os.path.exists('token.json'):
        print("Credenciales encontradas.")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("No se encontraron credenciales. Asegúrate de haber completado el proceso de autenticación.")
        return None

    try:
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(
            userId='me', q='in:inbox', maxResults=1
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            print("No se encontraron mensajes en la bandeja de entrada.")
            return None

        message_id = messages[0]['id']
        message = service.users().messages().get(userId='me', id=message_id).execute()
        payload = message['payload']
        parts = payload.get('parts', [])

        plain_text_content = None
        for part in parts:
            if part['mimeType'] == 'text/plain':
                plain_text_content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break

        if not plain_text_content:
            print("No se encontró contenido en texto plano en el correo.")
            return None

        match = re.search(r'https?://[^\s]+', plain_text_content)
        if match:
            verification_link = match.group(0)
            print("Enlace de verificación encontrado:", verification_link)
            return verification_link

        print("No se encontró el enlace de verificación en el correo.")
        return None

    except Exception as e:
        print(f"Error al obtener el enlace de verificación: {e}")
        return None

if __name__ == "__main__":
    user_email = "cbastidasobregon@gmail.com"
    verification_link = get_verification_link(user_email)
    if verification_link:
        print(f"Enlace de verificación encontrado: {verification_link}")
    else:
        print("No se encontró el enlace de verificación.")
