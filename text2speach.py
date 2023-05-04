from gtts import gTTS
import os

# Define a function to convert text to speech
def speak(text):
    # Create a gTTS object and specify the language
    tts = gTTS(text=text, lang='en')

    # Save the audio file
    tts.save("output.mp3")

    # Play the audio file
    os.system("mpg321 output.mp3")

# Get user input
user_input = input("What would you like me to say? ")

# Convert user input to speech
speak(user_input)

