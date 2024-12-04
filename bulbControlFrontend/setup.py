from setuptools import setup, find_packages

TEST_REQUIREMENTS = {"pytest", "pytest-django"}

setup(name="Realtime_PyAudio_FFT", packages=find_packages(), test_require=TEST_REQUIREMENTS)
