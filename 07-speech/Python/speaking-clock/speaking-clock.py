import os
from datetime import datetime

from dotenv import load_dotenv

# Import namespaces


def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv("COG_SERVICE_KEY")
        cog_region = os.getenv("COG_SERVICE_REGION")

        # Configure speech service

        # Get spoken input
        command = transcribe_command()
        if command.lower() == "what time is it?":
            tell_time()

    except Exception as ex:
        print(ex)


def transcribe_command():
    command = ""

    # Configure speech recognition

    # Process speech input

    # Return the command
    return command


def tell_time():
    now = datetime.now()
    response_text = "The time is {}:{:02d}".format(now.hour, now.minute)

    # Configure speech synthesis

    # Synthesize spoken output

    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()
