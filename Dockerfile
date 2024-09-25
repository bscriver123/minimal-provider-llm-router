FROM python:3.11-slim-buster
 
WORKDIR /backend

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="${PYTHONPATH}:/backend"

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean
 
# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /backend/
RUN pip install -r requirements.txt
 
# Copy project
COPY . /backend/

# Expose the port the app runs on
EXPOSE 80

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
