# Use an official lightweight Python image as a base
FROM python:3.11.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements.txt initially to leverage Docker cache
COPY ./requirements.txt /app/

# Install Python dependencies without cache files to save space
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./spotify_api /app/spotify_api

# Expose the port the FastAPI app will listen on
EXPOSE 8000

# Create a non-root user for security purposes
RUN useradd -m appuser
USER appuser

# Define the command to start the application using Uvicorn
CMD ["uvicorn", "spotify_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
