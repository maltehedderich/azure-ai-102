import os

from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def main():
    try:
        # Get configuration settings
        load_dotenv()
        form_endpoint = os.getenv("FORM_ENDPOINT")
        form_key = os.getenv("FORM_KEY")
        training_data_url = os.getenv("STORAGE_URL")

        # Authenticate Form Training
        form_training_client = FormTrainingClient(
            form_endpoint, AzureKeyCredential(form_key)
        )

        # Train model
        poller = form_training_client.begin_training(
            training_data_url, use_training_labels=True
        )
        model = poller.result()

        print(f"Model ID: {model.model_id}")
        print(f"Status: {model.status}")
        print(f"Training started on: {model.training_started_on}")
        print(f"Training completed on: {model.training_completed_on}")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
