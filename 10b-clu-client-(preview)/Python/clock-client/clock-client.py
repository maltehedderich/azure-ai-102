import os
from datetime import date, datetime, timedelta

from azure.ai.language.conversations import ConversationAnalysisClient

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ls_prediction_endpoint = os.getenv("LS_CONVERSATIONS_ENDPOINT")
        ls_prediction_key = os.getenv("LS_CONVERSATIONS_KEY")

        # Get user input (until they enter "quit")
        user_text = ""
        while user_text.lower() != "quit":
            user_text = input('\nEnter some text ("quit" to stop)\n')
            if user_text.lower() != "quit":
                # Create a client for the Language service model
                client = ConversationAnalysisClient(
                    ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key)
                )

                # Call the Language service model to get intent and entities
                cls_project = "Clock"
                deployment_slot = "production"

                with client:
                    query = user_text
                    result = client.analyze_conversation(
                        task={
                            "kind": "Conversation",
                            "analysisInput": {
                                "conversationItem": {
                                    "participantId": "1",
                                    "id": "1",
                                    "modality": "text",
                                    "language": "en",
                                    "text": query,
                                },
                                "isLoggingEnabled": False,
                            },
                            "parameters": {
                                "projectName": cls_project,
                                "deploymentName": deployment_slot,
                                "verbose": True,
                            },
                        }
                    )

                top_intent = result["result"]["prediction"]["topIntent"]
                entities = result["result"]["prediction"]["entities"]

                print("view top intent:")
                print(f"\ttop intent: {top_intent}")
                print(
                    "\tcategory: {}".format(
                        result["result"]["prediction"]["intents"][0]["category"]
                    )
                )
                print(
                    "\tconfidence score: {}\n".format(
                        result["result"]["prediction"]["intents"][0]["confidenceScore"]
                    )
                )

                print("view entities:")
                for entity in entities:
                    print("\tcategory: {}".format(entity["category"]))
                    print("\ttext: {}".format(entity["text"]))
                    print("\tconfidence score: {}".format(entity["confidenceScore"]))

                print("query: {}".format(result["result"]["query"]))

                # Apply the appropriate action
                if top_intent == "GetTime":
                    location = "local"
                    # Check for entities
                    for entity in entities:
                        if "Location" == entity["category"]:
                            # ML entities are strings, get the first one
                            location = entity["text"]
                    # Get the time for the specified location
                    print(get_time(location))
                elif top_intent == "GetDay":
                    date_string = date.today().strftime("%m/%d/%Y")
                    # Check for entities
                    for entity in entities:
                        if "Date" == entity["category"]:
                            # Regex entities are strings, get the first one
                            date_string = entity["text"]
                    # Get the day for the specified date
                    print(get_day(date_string))
                elif top_intent == "GetDate":
                    day = "today"
                    # Check for entities
                    for entity in entities:
                        if "Weekday" in entity["category"]:
                            # List entities are lists
                            day = entity["text"]
                    # Get the date for the specified day
                    print(get_date(day))
                else:
                    # Some other intent (for example, "None") was predicted
                    print("Try asking me for the time, the day, or the date.")
    except Exception as ex:
        print(ex)


def get_time(location):
    time_string = ""

    # Note: To keep things simple, we'll ignore daylight savings time and support only a few cities.
    # In a real app, you'd likely use a web service API (or write  more complex code!)
    # Hopefully this simplified example is enough to get the the idea that you
    # use LU to determine the intent and entities, then implement the appropriate logic

    if location.lower() == "local":
        now = datetime.now()
        time_string = f"{now.hour}:{now.minute:02d}"
    elif location.lower() == "london":
        utc = datetime.utcnow()
        time_string = f"{utc.hour}:{utc.minute:02d}"
    elif location.lower() == "sydney":
        time = datetime.utcnow() + timedelta(hours=11)
        time_string = f"{time.hour}:{time.minute:02d}"
    elif location.lower() == "new york":
        time = datetime.utcnow() + timedelta(hours=-5)
        time_string = f"{time.hour}:{time.minute:02d}"
    elif location.lower() == "nairobi":
        time = datetime.utcnow() + timedelta(hours=3)
        time_string = f"{time.hour}:{time.minute:02d}"
    elif location.lower() == "tokyo":
        time = datetime.utcnow() + timedelta(hours=9)
        time_string = f"{time.hour}:{time.minute:02d}"
    elif location.lower() == "delhi":
        time = datetime.utcnow() + timedelta(hours=5.5)
        time_string = f"{time.hour}:{time.minute:02d}"
    else:
        time_string = f"I don't know what time it is in {location}"

    return time_string


def get_date(day):
    date_string = "I can only determine dates for today or named days of the week."

    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thusday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    today = date.today()

    # To keep things simple, assume the named day is in the current week (Sunday to Saturday)
    day = day.lower()
    if day == "today":
        date_string = today.strftime("%m/%d/%Y")
    elif day in weekdays:
        today_num = today.weekday()
        weekday_num = weekdays[day]
        offset = weekday_num - today_num
        date_string = (today + timedelta(days=offset)).strftime("%m/%d/%Y")

    return date_string


def get_day(date_string):
    # Note: To keep things simple, dates must be entered in US format (MM/DD/YYYY)
    try:
        date_object = datetime.strptime(date_string, "%m/%d/%Y")
        day_string = date_object.strftime("%A")
    except Exception:
        day_string = "Enter a date in MM/DD/YYYY format."
    return day_string


if __name__ == "__main__":
    main()
