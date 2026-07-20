# 1. Start with an official lightweight Python base image (matching your Python 3.14 environment)
FROM python:3.14-slim

# 2. Set environment variables to optimize Python inside a container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the directory inside the container where our code will live
WORKDIR /app

# 4. Copy the dependencies list first and install them
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your Django project code into the container
COPY . /app/

# 6. Expose the port Django runs on
EXPOSE 8000

# New line: This tells Docker to spin up a shell, run migrations, and then start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]