# capstone-backend-flask

## Running Locally

1.  Create virtual environment and install dependencies

    ```
    python -m venv venv
    venv/Scripts/activate
    pip install -r requirements.txt
    ```

    Download gensim models beforehand

    ```
    python3 -c "import gensim.downloader; model=gensim.downloader.load('glove-wiki-gigaword-100'); model.save('glove-wiki-gigaword-100.model')"
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
    docker build -t capstone-backend-flask:$TAG .
    ```

    - **$TAG** should be of form **[MAJOR]:[MINOR]**
    - **.** describes the location of the Dockerfile

3. Running the image container
    ```
    docker run -e PORT=5000 -p 5000:5000 capstone-backend-flask:$TAG
    ```

Notes: Don't use slim version, as scikit needs gcc where as it is removed in slim version

## Pushing to Artifact Registry

0. Authenticate artifact registry

    ```
    gcloud auth configure-docker asia-southeast2-docker.pkg.dev

    gcloud artifacts repositories describe flask-docker --project=capstone-match-event --location=asia-southeast2
    ```

1. Tag the image

    ```
    docker tag capstone-backend-flask:$TAG asia-southeast2-docker.pkg.dev/capstone-match-event/flask-docker/capstone-backend-flask:$TAG
    ```

2. Push to Artifact Registry

    ```
    docker push asia-southeast2-docker.pkg.dev/capstone-match-event/flask-docker/capstone-backend-flask:$TAG
    ```
