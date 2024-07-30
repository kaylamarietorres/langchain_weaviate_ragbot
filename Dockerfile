# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Copy the entrypoint script
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/code/entrypoint.sh"]

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
