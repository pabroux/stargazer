FROM python:3.12-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Set the working directory inside the container
WORKDIR /app

# Copy the requirement file to the working directory
COPY requirements/prod.txt requirements.txt

# Install the app dependencies
RUN pip install -r requirements.txt

# Copy the app code to the working directory
COPY main.py .
COPY /stargazer ./stargazer
COPY /apps ./apps

# Expose the port on which the app will run
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
