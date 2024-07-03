# Mesh Network API

This project provides an API for a mesh network using LoRa devices.

## Requirements

- Python 3.7 or higher
- pip

## Setup

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd mesh_api
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the API server:
    ```bash
    python app.py
    ```

## API Endpoints

- `POST /connect`: Connect to the mesh network.
- `POST /disconnect`: Disconnect from the mesh network.
- `POST /send_message`: Send a message. Requires a JSON body with a `message` field.
- `GET /get_messages`: Get all received messages.
- `GET /get_locations`: Get the locations of all devices in the network.

## Tests

Run the test script to ensure the API is working correctly:
```bash
python test_api.py
