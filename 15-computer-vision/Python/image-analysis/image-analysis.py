import os
import sys

# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw


def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv("COG_SERVICE_ENDPOINT")
        cog_key = os.getenv("COG_SERVICE_KEY")

        # Get image
        image_file = "images/street.jpg"
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # Authenticate Computer Vision client
        credentials = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credentials)

        # Analyze image
        analyze_image(image_file)

        # Generate thumbnail
        get_thumbnail(image_file)

    except Exception as ex:
        print(ex)


def analyze_image(image_file):
    print("Analyzing", image_file)

    # Specify features to be retrieved
    features = [
        VisualFeatureTypes.description,
        VisualFeatureTypes.tags,
        VisualFeatureTypes.categories,
        VisualFeatureTypes.brands,
        VisualFeatureTypes.objects,
        VisualFeatureTypes.adult,
    ]

    # Get image analysis
    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data, features)

    # Get image description
    for caption in analysis.description.captions:
        print(
            f"Description: '{caption.text}' (confidence:"
            f" {caption.confidence * 100:.2f}%)"
        )

    # Get image tags
    if len(analysis.tags) > 0:
        print("Tags: ")
        for tag in analysis.tags:
            print(f" - '{tag.name}' (confidence: {tag.confidence * 100:.2f})")

    # Get image categories
    if len(analysis.categories) > 0:
        print("Categories:")
        landmarks = []
        for category in analysis.categories:
            print(f" - '{category.name}' (confidence: {category.score * 100:.2f})")
            if category.detail:
                # Get landmarks in this category
                if category.detail.landmarks:
                    for landmark in category.detail.landmarks:
                        if landmark not in landmarks:
                            landmarks.append(landmark)

        # If there where landmarks, list them
        if len(landmarks) > 0:
            print("Landmarks:")
            for landmark in landmarks:
                print(
                    f" - '{landmark.name}' (confidence:"
                    f" {landmark.confidence * 100:.2f})"
                )

    # Get brands in the image
    if len(analysis.brands) > 0:
        print("Brands:")
        for brand in analysis.brands:
            print(f" - '{brand.name}' (confidence: {brand.confidence * 100:.2f})")

    # Get objects in the image
    if len(analysis.objects) > 0:
        print("Objects in image:")

        # Prepare image for drawing
        fig = plt.figure(figsize=(8, 8))
        plt.axis("off")
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)
        color = "cyan"

        for detected_object in analysis.objects:
            # Print object name
            print(
                f" - '{detected_object.object_property}' (confidence:"
                f" {detected_object.confidence * 100:.2f})"
            )

            # Draw object bounding box
            r = detected_object.rectangle
            bounding_box = ((r.x, r.y), (r.x + r.w, r.y + r.h))
            draw.rectangle(bounding_box, outline=color, width=3)
            plt.annotate(
                detected_object.object_property, (r.x, r.y), backgroundcolor=color
            )

        # Save annotated image
        plt.imshow(image)
        output_file = f"{image_file[:-4]}_annotated.jpg"
        fig.savefig(output_file)
        print(f"\tResults saved in: {output_file}")

    # Get moderation ratings
    ratings = "Ratings:\n - Adult: {}\n - Racy: {}\n - Gore: {}".format(
        analysis.adult.is_adult_content,
        analysis.adult.is_racy_content,
        analysis.adult.is_gory_content,
    )
    print(ratings)


def get_thumbnail(image_file):
    print("Generating thumbnail")

    # Generate a thumbnail
    with open(image_file, mode="rb") as image_data:
        # Get thumbnail data
        thumbnail_stream = cv_client.generate_thumbnail_in_stream(
            100, 100, image_data, True
        )

    # Save thumbnail image
    thumbnail_file_name = f"{image_file[:-4]}_thumbnail.jpg"
    with open(thumbnail_file_name, mode="wb") as thumbnail_file:
        for chunk in thumbnail_stream:
            thumbnail_file.write(chunk)

    print("Thumbnail saved in.", thumbnail_file_name)


if __name__ == "__main__":
    main()
