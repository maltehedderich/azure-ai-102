import base64
import http.client
import json
import os
import urllib
from urllib import error, parse, request

from dotenv import load_dotenv


def main():
    global cog_endpoint
    global cog_key

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv("COG_SERVICE_ENDPOINT")
        cog_key = os.getenv("COG_SERVICE_KEY")

        # Get user input (until they enter "quit")
        user_text = ""
        while user_text.lower() != "quit":
            user_text = input('Enter some text ("quit" to stop)\n')
            if user_text.lower() != "quit":
                get_language(user_text)

    except Exception as ex:
        print(ex)


def get_language(text):
    try:
        # Construct the JSON request body (a collection of documents, each with an ID and text)
        json_body = {"documents": [{"id": 1, "text": text}]}

        # Let's take a look at the JSON we'll send to the service
        print(json.dumps(json_body, indent=2))

        # Make an HTTP request to the REST interface
        uri = cog_endpoint.rstrip("/").replace("https://", "")
        conn = http.client.HTTPSConnection(uri)

        # Add the authentication key to the request header
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": cog_key,
        }

        # Use the Text Analytics language API
        conn.request(
            "POST",
            "/text/analytics/v3.1/languages?",
            str(json_body).encode("utf-8"),
            headers,
        )

        # Send the request
        response = conn.getresponse()
        data = response.read().decode("UTF-8")

        # If the call was successful, get the response
        if response.status == 200:
            # Display the JSON response in full (just so we can see it)
            results = json.loads(data)
            print(json.dumps(results, indent=2))

            # Extract the detected language name for each document
            for document in results["documents"]:
                print("\nLanguage:", document["detectedLanguage"]["name"])

        else:
            # Something went wrong, write the whole response
            print(data)

        conn.close()

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
