# Use an official Python runtime as a parent image
FROM python

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN apt-get -y update && apt-get -y install dnsutils 
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app

COPY app/* /app/


# Expose port 5000 to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
#CMD ["fastapi", "run", "llama_cpu_server.py"]