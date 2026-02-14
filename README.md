# DevKB-API - REST API Wrapper

A lightweight REST API wrapper for DevKB that can be used by external applications.

## Features

- RESTful API endpoints
- JSON responses
- Authentication support
- Rate limiting
- CORS enabled

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The API will be available at `http://localhost:8080`

## Endpoints

- `GET /api/snippets` - List all snippets
- `POST /api/snippets` - Create a snippet
- `GET /api/snippets/{id}` - Get a snippet
- `DELETE /api/snippets/{id}` - Delete a snippet
- `GET /api/search?q=query` - Search snippets

## License

MIT
