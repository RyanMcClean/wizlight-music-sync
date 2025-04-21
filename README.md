![Code Coverage](https://img.shields.io/badge/Coverage-69%25-yellow.svg)

# Wizlight Bulb Audio Sync Project

Ryan Urquhart's QUB final year project.

This project is an attempt to synchronize the brightness and color of Wiz
light  
bulbs with the rhythm of music, either played from the local device, or the  
ambient music, using the microphone of the device.

The project has been developed in Python (There was an attempt in Java, but it
did not work).

## Features

-   **Audio Synchronization**: Dynamically adjusts the brightness of Wiz light
    bulbs based on the rhythm and beats of the music.
-   **Local and Ambient Music Support**: Works with both locally played music
    and ambient sound captured via the device's microphone.
-   **Local bulb control**: Can turn Wizbulb lights on and off on the app.

## Technologies Used

-   **Programming Language**: Python

-   **Libraries**:

    -   `django` for website design and management
    -   `pyaudio` (linux) or `pyaudiowpatch` (windows) for audio input
    -   `sounddevice` as a dependacny of `pyaudio`
    -   `numpy`, `scipy` for signal processing
    -   `pytest`, `pytest-django` to convert django tests to pytest for running
        in vscode
    -   `pytest-cov` for test coverage reporting
    -   `playwright` for website navigation testing
    -   `pytest-xdist` to allow parallel testing, to cut down testing run time.

-   **Hardware**: Wiz light bulbs and a computer (Windows, or Linux) with a
    microphone.
