# Stage 1: UI Build
FROM node:20-alpine AS ui-build

ARG BACKEND_URL

WORKDIR /app/ui

# Copy package files first for better caching
COPY ./ui/package.json ./ui/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the UI source code
COPY ./ui/ .

# Set environment variable and build
ENV VITE_BACKEND_URL=$BACKEND_URL
RUN npm run build

# Stage 2: Python Builder
FROM python:3.11 AS python-builder

# Improve performance and prevent generation of .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Create and activate a virtual environment, then install the dependencies
RUN pip install virtualenv && \
    virtualenv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install -r requirements.txt

# Stage 3: Final Deployer
FROM python:3.11 AS deployer

# Copy the virtual environment from the builder stage
COPY --from=python-builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y unixodbc-dev libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the rest of the application code
COPY . .

# Copy the built UI files from the UI build stage
COPY --from=ui-build /app/ui/dist ./ui/dist
COPY --from=ui-build /app/ui/dist-library ./ui/dist-library


EXPOSE 8001

CMD ["python3", "main.py", "--config", "./config.yaml", "llm"]