# docker build -t oxygen_cs-app . to build the image
# to run the image localy: docker run -it --rm oxygen_cs-app
# Use the official Python image as the base image for the build stage
FROM python:3.12.2-alpine3.19 AS build

# Install dependencies
RUN apk add --no-cache build-base libffi-dev openssl-dev postgresql-dev
RUN pip install pipenv

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --deploy --system --ignore-pipfile && \
    # Remove unused packages
    pip uninstall -y filelock pipenv setuptools wheel

# Runtime stage
FROM python:3.12.2-alpine3.19

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . /app

# Set environment variables
ENV HOST=http://159.203.50.162 \
    T_MAX=30 \
    T_MIN=15

# Run the application
CMD ["python", "src/main.py"]

