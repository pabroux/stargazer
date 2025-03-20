FROM python:3.12-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the application dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY main.py .
COPY settings.py .
COPY /apps ./apps

# Expose the port on which the application will run
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
