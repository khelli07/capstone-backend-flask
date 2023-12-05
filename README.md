# capstone-backend-flask

## Running Locally

1.  Create virtual environment and install dependencies

    ```
    python -m venv venv
    venv/Scripts/activate
    pip install -r requirements.txt
    ```

2.  Run the app

    ```
    python app.py

    OR

    flask run --debug -p 5000
    ```

3.  Open the app
    Visit http://localhost:5000/

## Building Docker Image

1. Make sure all requirements are updated

    ```
    pip freeze > requirements.txt
    ```

2. Build the image

    ```
    docker build -t capstone-backend-flask:[tag] .
    ```

    - **[tag]** should be of form **[MAJOR]:[MINOR]**
    - **.** describes the location of the Dockerfile

3. Running the image container
    ```
    docker run -p 5000:5000 capstone-backend-flask:[tag]
    ```

## Pushing to Artifact Registry

0. Authenticate artifact registry

    ```
    gcloud auth configure-docker asia-southeast2-docker.pkg.dev

    gcloud artifacts repositories describe flask-docker --project=capstone-match-event --location=asia-southeast2
    ```

1. Tag the image

    ```
    docker tag capstone-backend-flask:[tag] asia-southeast2-docker.pkg.dev/capstone-match-event/flask-docker/capstone-backend-flask:[tag]
    ```

2. Push to Artifact Registry

    ```
    docker push asia-southeast2-docker.pkg.dev/capstone-match-event/flask-docker/capstone-backend-flask:[tag]
    ```
