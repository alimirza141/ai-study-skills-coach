# API Notes

An API allows one software system to request data or actions from another system.

## Experiment

The Python `requests` library sends HTTP GET requests.

For each request, the program records:

- endpoint
- status code
- whether JSON is returned
- top-level response structure
- request errors

The Public APIs endpoint may be unavailable. The script handles this without crashing.