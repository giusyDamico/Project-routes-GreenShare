# Python image
FROM python:3.9-slim

# Define directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy proeject inside container
COPY . .

#Expose port container to localhost
EXPOSE 8000

# Commands in order to start container
CMD ["python", "django_routes/manage.py", "runserver", "0.0.0.0:8000"]
