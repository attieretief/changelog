FROM python:3.9-slim

# Copy the requirements file
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ ./src/

# Set the entry point for the action
ENTRYPOINT ["python", "/src/main.py"]