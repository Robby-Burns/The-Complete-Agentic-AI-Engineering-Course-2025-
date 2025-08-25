# Use a lightweight official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install uv && uv pip install -r requirements.txt

# Copy the rest of your project files
COPY . .

# The default command to run your app
CMD ["uv", "run", "python", "app.py"]
