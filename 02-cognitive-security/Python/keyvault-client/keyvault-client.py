import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv


def main():
    global cog_endpoint
    global cog_key

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        key_vault_name = os.getenv('KEY_VAULT')
        app_tenant = os.getenv('TENANT_ID')
        app_id = os.getenv('APP_ID')
        app_password = os.getenv('APP_PASSWORD')

        # Get cognitive services key from keyvault using the service principal credentials
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
        credential = ClientSecretCredential(app_tenant, app_id, app_password)
        keyvault_client = SecretClient(key_vault_uri, credential)
        secret_key = keyvault_client.get_secret("Cognitive-Services-Key")
        cog_key = secret_key.value

        # Get user input (until they enter "quit")
        user_text =''
        while user_text.lower() != 'quit':
            user_text = input('\nEnter some text ("quit" to stop)\n')
            if user_text.lower() != 'quit':
                language = get_language(user_text)
                print('Language:', language)

    except Exception as ex:
        print(ex)

def get_language(text):

    # Create client using endpoint and key
    credential = AzureKeyCredential(cog_key)
    client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

    # Call the service to get the detected language
    detected_language = client.detect_language(documents = [text])[0]
    return detected_language.primary_language.name


if __name__ == "__main__":
    main()