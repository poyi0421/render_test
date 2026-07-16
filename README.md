# FastAPI Render Hello API

A simple FastAPI application ready to be deployed to [Render](https://render.com/).

## API Endpoints

- **GET `/`**: Returns a JSON object `{"message": "Hello"}`.

## Local Development

If you have Python installed, you can run this application locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Access the API at `http://127.0.0.1:8000/`.

## Deployment to Render

You can deploy this project to Render in two ways:

### Option 1: Render Blueprint (Recommended)
This repository contains a `render.yaml` file. Render will automatically detect this file to set up your web service with the correct build and start commands.
1. Push this project to your GitHub/GitLab repository.
2. In the Render Dashboard, go to **Blueprints** and connect your repository.
3. Render will deploy the service automatically based on `render.yaml`.

### Option 2: Manual Web Service Setup
1. Push this project to your GitHub/GitLab repository.
2. In the Render Dashboard, click **New +** and select **Web Service**.
3. Connect your repository.
4. Configure the following settings during creation:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**.
