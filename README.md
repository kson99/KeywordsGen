# KeywordsGen

KeywordsGen is a lightweight FastAPI service that extracts relevant keywords and short key phrases from a block of text using KeyBERT and a local sentence-transformers model.

## What it does

This project exposes a single API endpoint that accepts text input and returns the most relevant keywords ranked by relevance. It is useful for:

- blog and content analysis
- search term generation
- topic detection
- metadata or tag extraction
- keyword suggestions for articles or documents

## Project structure

- `app.py` – FastAPI application and keyword extraction logic
- `requirements.txt` – Python dependencies
- `Dockerfile` – container build configuration
- `text.rest` – example API request for local testing

## API endpoint

### POST /extract-keywords

Request body:

```json
{
  "text": "Your article or text goes here",
  "limit": 5
}
```

Response:

```json
{
  "keywords": ["machine learning", "fastapi", "api", "model", "keywords"]
}
```

### Request fields

- `text` (required): the input text to analyze
- `limit` (optional): number of keywords to return; default is `5`

## How it works

The service uses KeyBERT with the `all-MiniLM-L6-v2` embedding model. It:

1. receives text input
2. embeds the text with a local sentence-transformers model
3. extracts candidate keywords and phrases
4. removes common stop words
5. returns the top matches

This runs locally in the application environment and does not require external API keys.

## Local development

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the API server:

```bash
python app.py
```

The app runs on:

```text
http://127.0.0.1:8000
```

## Running with Docker

Build the image:

```bash
docker build -t keywordsgen .
```

Run the container:

```bash
docker run -p 8000:8000 keywordsgen
```

## Example request

A sample request is included in `text.rest`. You can use it with REST client tools such as VS Code's REST Client extension.

## Dependencies

The project depends on:

- FastAPI for the API layer
- Uvicorn for serving the app
- Pydantic for request validation
- KeyBERT for keyword extraction
- sentence-transformers for the underlying embedding model

## Notes

- Empty text returns an empty list of keywords.
- The extraction model is preloaded during the Docker build to reduce startup time and avoid runtime download issues.
- The default output contains keyword strings only, without confidence scores.
