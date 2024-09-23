# Public Transport NER Model API

This repository contains the code and Docker configuration to deploy the Public Transport NER Model API. The model has been fine-tuned for entity-extraction related to route numbers, route names and stop places in Oslo and Akershus.

# Features
- Fine-tuned NER model for route and stop place recognition.
- RESTful API built using FastAPI.
- Dockerized for easy deployment and portability.

# Requirements

Before you can build and run the Docker image, ensure you have the following installed:
- Docker
- Python 3.x (for local development)
- FastAPI and Transformers (included in the Docker image)

# How to Use
# 1. Build Docker Image
To build the Docker image, run the following command:

```docker build -t <image_name> . ```

Example:

```docker build -t ner-model-api . ```
# 2. Run Docker Container

Run the container and expose it on port 8000:

```docker run --name <container_name> -p 8000:8000 <image_name> ```

Example:

```docker run --name ner-api -p 8000:8000 ner-model-api ```

The API will be available at: http://localhost:8000.
# 3. API Endpoints

The following endpoints are available:

    POST /recognize?text=<text>

        Parameters:
            text: The input text to be processed by the NER model.
            group_entities: Optional boolean to group entities together (default: false).
            wait: Optional boolean to wait for the full result before returning (default: true).

Example Request:

```bash
curl -X POST "http://localhost:8000/recognize?text=Når ankommer 31 Grorud på Jernbanetorget?" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{"text": "Når ankommer 31 Grorud på Jernbanetorget?"}'
```

Response:

JSON containing the recognized entities and their labels.

Example Response:

```json
  {
    "entities": [
      {"word": "31", "entity_group": "B-ROUTENUMBER", "confidence": 0.98},
      {"word": "Grorud", "entity_group": "B-ROUTENAME", "confidence": 0.95},
      {"word": "Jernbanetorget", "entity_group": "B-STOPPLACE", "confidence": 0.96}
    ]
  }
```
# 4. Stopping and Removing Containers

To stop the running container:

```docker stop <container_name> ```

To remove the container:

``` docker rm <container_name> ```

# Development Setup (Without Docker)

If you prefer to run the API locally without Docker:

Install dependencies:

```pip install -r requirements.txt ```

Run the FastAPI server:

```uvicorn main:app --reload --host 0.0.0.0 --port 8000 ```

The API will be available at: http://localhost:8000.
