FROM node:20-alpine AS build

ARG BACKEND_URL

WORKDIR /app

COPY ./ui/package.json ./

RUN npm install

COPY ./ui/ . 

ENV VITE_BACKEND_URL=$BACKEND_URL

RUN npm run build

# Stage 1: Builder
FROM python:3.11 AS builder

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

# Stage 2: Deployer
FROM python:3.11 AS deployer

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y unixodbc-dev && apt-get install -y libgl1


# Set the working directory
WORKDIR /app

# Copy the rest of the application code
COPY . .
# COPY --from=build /app/dist ./ui/dist
# COPY --from=build /app/dist-library ./ui/dist-library

EXPOSE 8001

CMD ["python3", "main.py", "--config", "./config.yaml", "llm"]