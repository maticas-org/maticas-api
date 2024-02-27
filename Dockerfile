# Pull base image
FROM python:3.10.3-slim-bullseye

# Set environment variables

# # Disables an automatic check for pip updates each time
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# # Python will not try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# # Ensures our console output is not buffered by Docker
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /api_source

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py load fixtures/variable
RUN python manage.py load fixtures/actuator_type

# Copy project
COPY . .
