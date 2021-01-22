## build stage 
FROM python:3-alpine as build-stage

# make the 'app' folder the current working directory
WORKDIR /app

# copy requirements
COPY requirements.txt .

# install project dependencies
RUN pip install -r requirements.txt

# copy other files needed 
COPY . .
# production stage
EXPOSE 1234
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "1234"]
