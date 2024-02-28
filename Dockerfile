# docker build -t oxygen_cs-app . to build the image
# to run the image locally: docker run -it --rm oxygen_cs-app
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock from your host to the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv
RUN pip install pipenv

# Install dependencies from Pipfile
RUN pipenv install --deploy --ignore-pipfile --system \
    # Remove Pipenv cache
    && rm -rf $PIPENV_CACHE_DIR \
    # Clean up pip cache and temporary files
    && rm -rf /root/.cache/pip/*

# Copy the rest of your application code to the container
COPY . /app

# Run the application
CMD ["python", "src/main.py"]
