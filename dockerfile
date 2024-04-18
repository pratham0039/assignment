# Base image for Python application
FROM python:3.9

# Set working directory
WORKDIR /core

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port for the application (adjust if needed)
EXPOSE 5000

# Entrypoint command
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "main:core/server.py" ]
