# start by pulling the python image
FROM python:3.11.0

# ENV LISTEN_PORT=5000
# EXPOSE 5000

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# upgrade pip
RUN python -m pip install --upgrade pip

# upgrade the build tools packages
RUN python -m pip install --upgrade pip setuptools wheel

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# install protobuff correct version
RUN pip install --upgrade "protobuf<=3.20.1"

#install opencv dependencies
RUN apt-get update && apt-get install libgl1 -y

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["run.py" ]