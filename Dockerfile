FROM python:3.10-slim AS python-base

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set up working directory
WORKDIR /app
RUN cd /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API directory
COPY Scripts/ /app/Scripts/

# Expose the API port
EXPOSE 5001

CMD ["python", "Scripts/csgo_database_api.py"]

