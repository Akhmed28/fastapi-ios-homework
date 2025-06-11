# Dockerfile

# 1. Start from an official Python base image.
# We'll use Python 3.9 in a "slim" version, which is smaller.
FROM python:3.11-slim

# 2. Set the working directory inside the container.
# All subsequent commands will run from this path.
WORKDIR /app

# 3. Copy the requirements file into the container's working directory.
COPY requirements.txt .

# 4. Install the Python dependencies listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application's code into the container.
# The first "." means "the current folder on your Mac".
# The second "." means "the current working directory inside the container (/app)".
COPY . .

# 6. Expose the port the app runs on.
# This is more for documentation; the -p flag in `docker run` actually opens the port.
EXPOSE 80

# 7. Define the command to run your application when the container starts.
# We use "--host 0.0.0.0" to make the server accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]