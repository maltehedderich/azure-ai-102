import os

from azure.ai.textanalytics import TextAnalyticsClient

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv("COG_SERVICE_ENDPOINT")
        cog_key = os.getenv("COG_SERVICE_KEY")

        # Create client using endpoint and key
        credential = AzureKeyCredential(cog_key)
        cog_client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = "reviews"
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print("\n-------------\n" + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding="utf8").read()
            print("\n" + text)

            # Get language
            detected_language = cog_client.detect_language(documents=[text])[0]
            print(f"\nLanguage: {detected_language.primary_language.name}")

            # Get sentiment

            # Get key phrases

            # Get entities

            # Get linked entities

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
