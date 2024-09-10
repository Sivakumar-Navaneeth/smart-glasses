# Smart Glasses Project

This repository contains the code and resources for the **Smart Glasses** project, which focuses on detecting people using a camera mounted on smart glasses. It aims to identify individuals using the Google Contacts API and perform threat detection for enhanced user safety.

## Features

- **Person Detection**: Detects people in front of the user using a camera integrated into the smart glasses.
- **Identification**: Identifies known individuals by integrating with the Google Contacts API to match detected faces.
- **Threat Detection**: Analyzes detected individuals to determine if they pose any potential threat, providing alerts to the user.

## Getting Started

### Prerequisites

Ensure that you have the following installed before running the project:

- Python 3.7 or higher
- TensorFlow or PyTorch (depending on your ML model)
- OpenCV for image processing
- Google API client library for accessing Google Contacts
- Other dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/surprise-smart-things/smart-glasses.git
   cd smart-glasses
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the Google Contacts API:
   - Follow [Google Contacts API documentation](https://developers.google.com/contacts/v3) to create credentials and enable API access.
   - Place the credentials JSON file in the root of the project and update the path in the code.

4. Ensure that your smart glasses' camera is functional and configured for your environment.

### Usage

To start the smart glasses software:

```bash
python main.py
```

The software will start detecting people in real-time, identify them using Google Contacts, and notify if any potential threats are detected.

### Configuration

- **Google Contacts API**: You can configure the API key and other relevant settings in the `config.json` file.
- **Threat Detection Parameters**: Customize threat detection sensitivity and behavior by modifying the `threat_detection.py` script.

### Example Output

The system will display real-time video feed with identified individuals labeled. If a threat is detected, an alert will be displayed in the console and/or through an audio notification (depending on your settings).

## Project Structure

```
smart-glasses/
│
├── models/               # Pre-trained models for detection and identification
├── scripts/              # Helper scripts
├── main.py               # Entry point of the application
├── config.json           # Configuration file
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## Acknowledgments

- [Google Contacts API](https://developers.google.com/contacts/v3)
- TensorFlow, PyTorch, and OpenCV for enabling advanced image processing and machine learning.
