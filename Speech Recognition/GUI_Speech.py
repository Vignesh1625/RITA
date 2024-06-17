import PySimpleGUI as sg
import pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3

# Create a layout for the GUI window
layout = [
    [sg.Text("This is a real-time speech recognition GUI")],
    [sg.HorizontalSeparator()],
    [sg.Multiline("", key="text", size=(60, 10), pad=(10, 10), autoscroll=True)], # Multiline element for continuous text display
    [sg.Button("Exit")]
]

# Create a GUI window with the layout
window = sg.Window("Real-Time Speech Recognition", layout)
# Create a vosk model and recognizer
model = Model(r"./vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

# Create a pyaudio object and an input stream
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Create a loop to process the audio data and update the GUI
while True:
    # Read a chunk of audio data from the stream
    data = stream.read(4096, exception_on_overflow=False) # Add the argument to prevent the exception

    # Check if the recognizer accepts the audio data as a valid waveform
    if recognizer.AcceptWaveform(data):
        # Get the result of the speech recognition as a JSON string
        result = recognizer.Result()

        # Extract the text from the JSON string
        text = result[14:-3]
        # Update the multiline element in the GUI window with the text
        window["text"].print(text, end='\n', text_color='black') # Use print to append text

    # Check if the user has clicked any button
    event, values = window.read(timeout=0)

    # If the user has clicked the "Exit" button or closed the window, break the loop
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

# Close the window
window.close()
