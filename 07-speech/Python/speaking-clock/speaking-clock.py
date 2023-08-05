import os
from datetime import datetime

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv


def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv("COG_SERVICE_KEY")
        cog_region = os.getenv("COG_SERVICE_REGION")

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        print("Ready to use speech service in:", speech_config.region)

        # Get spoken input
        command = transcribe_command()
        if command.lower() == "what time is it?":
            tell_time()

    except Exception as ex:
        print(ex)


def transcribe_command():
    command = ""

    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print("Speek now...")

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command


def tell_time():
    now = datetime.now()
    response_text = "The time is {}:{:02d}".format(now.hour, now.minute)

    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = "en-GB-LibbyNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    # Synthesize spoken output
    response_ssml = """
     <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
         <voice name='en-GB-LibbyNeural'>
             {}
             <break strength='weak'/>
             Time to end this lab!
         </voice>
     </speak>
     """.format(response_text)
    speak = speech_synthesizer.speak_ssml_async(response_ssml).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()
