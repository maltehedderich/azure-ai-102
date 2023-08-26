import os
import time

# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from dotenv import load_dotenv
from msrest.authentication import CognitiveServicesCredentials


def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv("COG_SERVICE_ENDPOINT")
        cog_key = os.getenv("COG_SERVICE_KEY")

        # Authenticate Computer Vision client
        credentials = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credentials)

        # Menu for text reading functions
        print(
            "1: Use Read API for image\n2: Use Read API for document\n3: Read"
            " handwriting\nAny other key to quit"
        )
        command = input("Enter a number:")
        if command == "1":
            image_file = os.path.join("images", "Lincoln.jpg")
            get_text_read(image_file)
        elif command == "2":
            image_file = os.path.join("images", "Rome.pdf")
            get_text_read(image_file)
        elif command == "3":
            image_file = os.path.join("images", "Note.jpg")
            get_text_read(image_file)

    except Exception as ex:
        print(ex)


def get_text_read(image_file):
    print(f"Reading text in {image_file}\n")

    # Use Read API to read text in image
    with open(image_file, "rb") as image_data:
        read_op = cv_client.read_in_stream(image_data, raw=True)

        # Get the async operation id to check for the results
        operation_location = read_op.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Wait for the async operation to complete
        while True:
            read_results = cv_client.get_read_result(operation_id)
            if read_results.status not in [
                OperationStatusCodes.not_started,
                OperationStatusCodes.running,
            ]:
                break
            time.sleep(1)

        # If the operation was successful, process the text line by line
        if read_results.status == OperationStatusCodes.succeeded:
            for page in read_results.analyze_result.read_results:
                for line in page.lines:
                    print(line.text)
                    # print(line.bounding_box)


if __name__ == "__main__":
    main()
