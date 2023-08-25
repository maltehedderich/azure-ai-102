import os

import numpy as np
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from matplotlib import pyplot as plt
from msrest.authentication import ApiKeyCredentials
from PIL import Image, ImageDraw


def main():
    from dotenv import load_dotenv

    try:
        # Get Configuration Settings
        load_dotenv()
        prediction_endpoint = os.getenv("PredictionEndpoint")
        prediction_key = os.getenv("PredictionKey")
        project_id = os.getenv("ProjectID")
        model_name = os.getenv("ModelName")

        # Authenticate a client for the training API
        credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        prediction_client = CustomVisionPredictionClient(
            endpoint=prediction_endpoint, credentials=credentials
        )

        # Load image and get height, width and channels
        image_file = "produce.jpg"
        print("Detecting objects in", image_file)
        image = Image.open(image_file)
        h, w, _ = np.array(image).shape

        # Detect objects in the test image
        with open(image_file, mode="rb") as image_data:
            results = prediction_client.detect_image(project_id, model_name, image_data)

        # Create a figure for the results
        fig = plt.figure(figsize=(8, 8))
        plt.axis("off")

        # Display the image with boxes around each detected object
        draw = ImageDraw.Draw(image)
        line_width = int(w / 100)
        color = "magenta"
        for prediction in results.predictions:
            # Only show objects with a > 50% probability
            if (prediction.probability * 100) > 50:
                # Box coordinates and dimensions are proportional - convert to absolutes
                left = prediction.bounding_box.left * w
                top = prediction.bounding_box.top * h
                height = prediction.bounding_box.height * h
                width = prediction.bounding_box.width * w
                # Draw the box
                points = (
                    (left, top),
                    (left + width, top),
                    (left + width, top + height),
                    (left, top + height),
                    (left, top),
                )
                draw.line(points, fill=color, width=line_width)
                # Add the tag name and probability
                plt.annotate(
                    prediction.tag_name + f": {prediction.probability * 100:.2f}%",
                    (left, top),
                    backgroundcolor=color,
                )
        plt.imshow(image)
        outputfile = "output.jpg"
        fig.savefig(outputfile)
        print("Results saved in ", outputfile)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
