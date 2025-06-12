# Start from our Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# --- THIS IS THE NEW LINE ---
# First, upgrade pip to the latest version to get the best dependency resolver
RUN pip install --upgrade pip

# Now, copy the requirements file and install the packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 80

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]