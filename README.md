![Code Coverage](https://raw.githubusercontent.com/RyanMcClean/wizlight-music-sync/badges/coverage.svg?raw=true)
![Last Commit](https://img.shields.io/github/last-commit/RyanMcClean/wizlight-music-sync)
![Github Actions Status](https://img.shields.io/github/actions/workflow/status/RyanMcClean/wizlight-music-sync/django.yml)
![PyLint Score](https://raw.githubusercontent.com/RyanMcClean/wizlight-music-sync/badges/pylint.svg?raw=true)

# Wizlight Bulb Audio Sync Project

Ryan Urquhart's QUB final year project.

This project is an attempt to synchronize the brightness and color of Wiz
light  
bulbs with the rhythm of music, either played from the local device, or the  
ambient music, using the microphone of the device.

The project has been developed in Python, containing some javascript, html, css.

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
    -   `sounddevice` as a dependency of `pyaudio`
    -   `numpy`, `scipy` for signal processing
    -   `pytest`, `pytest-django` to convert django tests to pytest for running
        in vscode
    -   `pytest-cov` for test coverage reporting
    -   `playwright` for website navigation testing
    -   `pytest-xdist` to allow parallel testing, to cut down testing run time.

-   **Hardware**: Wiz light bulbs and a computer (Windows, or Linux) with a
    microphone.

# Installation:

The way to install the system is to follow these steps:

-   **Download the repository**:

    -   Clone this repository locally on your machine

-   **Create a virtual enviroment**:

    -   **_Linux_**:
        -   `python3 -m venv {directory_name_to_place_virtual_environment}`
    -   **_Windows_**:
        -   `py -m venv {directory_name_to_place_virtual_environment}`

-   **Start the virtual enviroment**

    -   **_Linux_**:
        -   `source ./{directory_name_to_place_virtual_environment}/bin/activate`
    -   **_Windows_**:
        -   `./{directory_name_to_place_virtual_environment}/Scripts/Active.ps1`

-   **Install requirements**

    -   **_Linux_**:
        -   `cat ./requirements.txt | grep -Eo '(^[^#]+)' | xargs -n 1 pip3 install`
        -   This extra script prevents an error when installing pyaudiowpatch,
            which is only available on windows
    -   **_Windows_**:
        -   `pip install -r ./requirements.txt`

-   **Make Django Migrations**:

    -   `python ./manage.py makemigrations bulb_control_frontend`

-   **Apply Django Migrations**:

    -   `python ./manage.py migrate`

-   **Start Server**:

    -   `python ./manage.py runserver 0.0.0.0:8000`
    -   This runs the server and makes it available to all connections, if you
        want to only be able to access it from the local machine change
        `0.0.0.0` to `127.0.0.1`

-   **Load WebApp**:
    -   Open a browser and navigate to `localhost:8000` or `127.0.0.1:8000`
