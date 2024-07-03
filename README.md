# LEVkey
# Mesh Network API

This project provides an API for connecting, sending, and receiving encrypted messages using a mesh network with LoRa and Meshtastic. The API is built using Flask and supports encryption with AES.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Running the API

1. Ensure the LoRa device is connected to `COM25` (or change the port in the `app.py` file if necessary).

2. Start the Flask server:

    ```bash
    python app.py
    ```

## Testing the API

1. Run the test script:

    ```bash
    python test_api.py
    ```

This will perform the following actions:
- Connect to the mesh network.
- Send an encrypted message.
- Retrieve messages.
- Send a location.
- Retrieve locations.
- Disconnect from the mesh network.

## Working with Branches

### Overview

Branches in Git are used to develop features, fix bugs, or experiment in isolation from the main codebase. The `main` or `master` branch is typically the production branch.

### Common Commands

- **Create a new branch**: 
    ```bash
    git checkout -b <branch-name>
    ```
- **Switch to an existing branch**:
    ```bash
    git checkout <branch-name>
    ```
- **List all branches**:
    ```bash
    git branch
    ```
- **Merge a branch into the current branch**:
    ```bash
    git merge <branch-name>
    ```
- **Delete a branch**:
    ```bash
    git branch -d <branch-name>
    ```

### Workflow Example

1. Create a new branch for a feature or bugfix:

    ```bash
    git checkout -b feature/my-new-feature
    ```

2. Make your changes and commit them:

    ```bash
    git add .
    git commit -m "Add my new feature"
    ```

3. Push the branch to the remote repository:

    ```bash
    git push origin feature/my-new-feature
    ```

4. Open a pull request to merge your feature branch into the main branch.

5. Once the pull request is reviewed and approved, merge it into the main branch:

    ```bash
    git checkout main
    git pull origin main
    git merge feature/my-new-feature
    ```

6. Delete the feature branch after merging:

    ```bash
    git branch -d feature/my-new-feature
    git push origin --delete feature/my-new-feature
    ```

## Notes

- Make sure to replace `<repository-url>` and `<repository-directory>` with your repository's URL and directory.
- Adjust the COM port in `app.py` if necessary.
- Ensure the encryption key is securely managed and not hard-coded in a production environment.

Feel free to reach out if you have any questions or need further assistance.
