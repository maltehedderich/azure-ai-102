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
            sentiment_analysis = cog_client.analyze_sentiment(documents=[text])[0]
            print(f"\nSentiment: {sentiment_analysis.sentiment}")

            # Get key phrases
            phrases = cog_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
                for phrase in phrases:
                    print(f"\t{phrase}")

            # Get entities
            entities = cog_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities")
                for entity in entities:
                    print(f"\t{entity.text} ({entity.category})")

            # Get linked entities
            linked_entities = cog_client.recognize_linked_entities(documents=[text])[
                0
            ].entities
            if len(entities) > 0:
                print("\nLinks")
                for linked_entity in linked_entities:
                    print(f"\t{linked_entity.name} ({linked_entity.url})")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
