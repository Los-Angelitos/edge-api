# SweetManager Edge API
For this API, you need to have a SweetManager Edge instance running.
Technologies used:
### - Flask
### - MQTT
### - SQLite

## Installation
1. Clone the repository:
   ```bash
    git clone https://github.com/Los-Angelitos/edge-api.git
    cd edge-api
   ```
2. Create a virtual environment:
   ```bash
    python -m venv venv
    cd venv/Scripts/activate
   ```

3. Install the required packages:
   ```bash
    pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
    python app.py
   ```

## Usage
You can access the API at `http://localhost:3000`.
Also, the host configured is 0.0.0.0 so you can access it from other devices in the same network.

## Authors
- [@Los-Angelitos](https://github.com/Los-Angelitos)