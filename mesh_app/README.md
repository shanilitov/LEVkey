# Mesh Network UI

This project provides a user interface for a mesh network chat and location display.

## Requirements

- Python 3.7 or higher
- pip

## Setup

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd mesh_app
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the UI server:
    ```bash
    python app.py
    ```

4. Open a browser and navigate to `http://localhost:5001`.

## Notes

- The UI communicates with the API running on `http://localhost:5000`.
- Ensure the API server is running before starting the UI.
