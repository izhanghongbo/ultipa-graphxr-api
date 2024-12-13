# Ultipa Graph API

A FastAPI-based REST API service for interacting with Ultipa Graph Database.

## Features

- Graph database schema retrieval
- Query execution with support for nodes, edges, and paths
- Sample queries management
- Multiple graph support
- CORS enabled for cross-origin requests

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- Ultipa Graph Database instance

## Installation

### Using Docker (Recommended)

1. Clone the repository
2. Find the docker-compose.yml file and edit the environment variables:
   ```yaml
   ULTIPA_HOSTS=
   ULTIPA_USERNAME=
   ULTIPA_PASSWORD=
   GRAPH_NAME=
   ```
3. Start the service using Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Manual Installation

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy and configure environment variables:
   ```bash
   cp env-example .env
   ```

4. Start the service:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| ULTIPA_HOSTS | Ultipa database host(s) | localhost:7018 |
| ULTIPA_USERNAME | Database username | root |
| ULTIPA_PASSWORD | Database password | root |
| GRAPH_NAME | Default graph name | default |
| SAMPLES_PATH | Path to samples configuration file | samples.yaml |

## API Endpoints

### Graph Operations

- `GET /api/v1/ultipa/schema` - Retrieve graph schema
- `POST /api/v1/ultipa/execute` - Execute graph queries
- `GET /api/v1/ultipa/samples` - Get sample queries
- `GET /api/v1/ultipa/graphs` - List available graphs

## Use Grove to interact with the API

After starting the service, you can use Grove to visualize and interact with your graph data:

use a shared project:

1. Open the Grove interface at [GraphXR Grove](https://graphxr.kineviz.com/share/67595c55bcdae6c322c58738/Grove?userID=5c020fe520f1ed00216552c3&groveProjectId=67595c55bcdae6c322c58738&groveFileKey=ultipa-graph&groveVersion=0&groveFullscreen=true&groveReadonly=true&groveBlockMode=hide)

2. In the server input field at the top, enter your API server URL:
   - For local development: `http://localhost:8000`
   - For remote server: Enter your server's URL

3. Select a graph from the dropdown menu

4. You can now:
   - View and select node categories
   - Explore relationships
   - Execute custom queries
   - Visualize query results in an interactive graph

The Grove interface provides an intuitive way to explore your graph data through a visual interface while using the API endpoints described above.

use your own project:

1. create a new project https://graphxr.kineviz.com/  with a grove template
![Create Project](https://raw.githubusercontent.com/izhanghongbo/ultipa-graphxr-api/main/images/project-add.jpg)

2. download the grove file [ultipa-graph.grove](https://raw.githubusercontent.com/izhanghongbo/ultipa-graphxr-api/main/ultipa-graph.grove)
3. open the grove tab and drag the code into the panel,you will see the grove's ui in the panel
![Grove](https://raw.githubusercontent.com/izhanghongbo/ultipa-graphxr-api/main/images/grove.jpg)

