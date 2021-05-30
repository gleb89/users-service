# users-service

## Users service app /fastapi(python)
***
## Build and run the container

1. Install Docker.

2. Create a `.env` file 

    ```
    # Environment settings for local development.
      CONTRIB_FASTAPI_APP=app
      CONTRIB_LOG_PATH: path/to/
      CONTRIB_LOG_LEVEL=CONTRIB_LOG_LEVEL
      CONTRIB_MONGODB_DSN=CONTRIB_MONGODB_DSN
    ```


3. On the command line, within this directory, do this to build the image and
   start the container:


        docker-compose up --build
        docker-compose up -d
        docker-compose -f docker-compose.yml logs -f


4. Open http://0.0.0.0/users/api/v1 in your browser.
