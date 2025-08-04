# Use a slim Python base image for a smaller footprint
FROM python:3.13.5-bookworm
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
COPY . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN pip install .

# Define the command to run your application
ENTRYPOINT ["python3", "start.py"]