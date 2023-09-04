# Use Ubuntu 22.04 as a base image
FROM ubuntu:22.04

# Set non-interactive mode (useful when installing packages)
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install required packages
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3.10-dev python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Setup a virtual environment (Optional, but isolates dependencies)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install Rasa
RUN pip install rasa

# Install Django
RUN pip install django

# Copy your existing Rasa and Django projects into the container (assuming they are in 'rasa_project' and 'django_project' directories respectively)
# COPY rasa_project /app/rasa_project
# COPY django_project /app/django_project

# Expose ports (Rasa default is 5005, Django default is 8000)
EXPOSE 5005
EXPOSE 8000

# By default, just run a shell. You can change this to run Rasa/Django or any other command.
CMD ["/bin/bash"]
