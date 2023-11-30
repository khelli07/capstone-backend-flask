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
