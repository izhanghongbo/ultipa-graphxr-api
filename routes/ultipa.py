from fastapi import APIRouter, HTTPException, Request
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from ultipa import Connection, UltipaConfig
from ultipa.configuration.RequestConfig import RequestConfig
import yaml

class ExecuteRequest(BaseModel):
    command: str
    graphName: str | None = None

# Load environment variables
load_dotenv()

router = APIRouter()

# Initialize configuration
ultipaConfig = UltipaConfig()
ultipaConfig.hosts = os.getenv('ULTIPA_HOSTS', 'localhost:7018').split(',')
ultipaConfig.username = os.getenv('ULTIPA_USERNAME', 'root')
ultipaConfig.password = os.getenv('ULTIPA_PASSWORD', 'root')
ultipaConfig.defaultGraph = os.getenv('GRAPH_NAME', 'default')

# Create connection
conn = Connection.NewConnection(defaultConfig=ultipaConfig)

@router.get("/schema")
async def get_schema(request: Request, graphName: str = None):
    try:
        requestConfig = RequestConfig(graphName = graphName if graphName else ultipaConfig.defaultGraph)
        schemas = conn.showSchema(requestConfig)
        nodes = []
        relationships = []
        for schema in schemas:
            if schema.type == "node":
                nodes.append(schema.name)
            elif schema.type == "edge":
                relationships.append(schema.name)

        return {
            "categories": nodes,
            "relationships": relationships
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching schema: {str(e)}"
        )

@router.post("/execute")
async def execute(request: ExecuteRequest):
    try:
        command = request.command
        request_config = RequestConfig(graphName=request.graphName if request.graphName else ultipaConfig.defaultGraph)
        
        # Execute query
        result = conn.uql(command, request_config)
        
        # Initialize graph data structure
        graph_data = {
            "nodes": [],
            "edges": []
        }
        
        # First check status code
        if result.status.code != 0:
            raise HTTPException(
                status_code=400,
                detail=f"Query execution failed: {result.status.message}"
            )
        
        # If there is data, process result.items
        if result.items:
            # Iterate over all DataItem in the dictionary
            for alias, item in result.items.items():
                if item.type == "NODE":
                    for node in item.data:
                        graph_node = {
                            "id": node.id,
                            "category": node.schema,
                            "properties": node.values
                        }
                        graph_data["nodes"].append(graph_node)
                
                elif item.type == "EDGE":
                    for edge in item.data:
                        graph_edge = {
                            "id": edge.getUUID(),
                            "name": edge.schema,
                            "source": edge.getFrom(),
                            "target": edge.getTo(),
                            "properties": edge.values
                        }
                        graph_data["edges"].append(graph_edge)
                
                elif item.type == "PATH":
                    for path in item.data:
                        # Process nodes in the path
                        for node in path.nodes:
                            graph_node = {
                                "id": node.id,
                                "category": node.schema,
                                "properties": node.values
                            }
                            graph_data["nodes"].append(graph_node)
                        
                        # Process edges in the path
                        for edge in path.edges:
                            graph_edge = {
                                "id": edge.getUUID(),
                                "name": edge.schema,
                                "sourceId": edge.getFrom(),
                                "targetId": edge.getTo(),
                                "properties": edge.values
                            }
                            graph_data["edges"].append(graph_edge)
        
        return graph_data
            
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error executing query: {str(e)}"
        )

@router.get("/samples")
async def get_samples():
    try:
        config_path = os.getenv('SAMPLES_PATH', 'samples.yaml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        if not config or 'samples' not in config:
            return {"samples": []}
            
        return {"samples": config['samples']}
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Configuration file not found"
        )
    except yaml.YAMLError:
        raise HTTPException(
            status_code=500,
            detail="Error parsing configuration file"
        )

@router.get("/graphs")
async def get_graphs():
    try:
        # Execute query to get all graph sets
        result = conn.uql("show().graph()")
        
        if result.status.code != 0:
            raise HTTPException(
                status_code=400,
                detail=f"Query execution failed: {result.status.message}"
            )
        
        # Process the returned result
        graphs = []
        if '_graph' in result.items:
            graph_item = result.items['_graph']
            if graph_item.data:
                headers = graph_item.data.headers
                rows = graph_item.data.rows
                for row in rows:
                    graph_dict = {}
                    for i, header in enumerate(headers):
                        # Use dictionary access to get property_name
                        graph_dict[header['property_name']] = row[i]
                    graphs.append(graph_dict)
        
        return graphs
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching graphs: {str(e)}"
        ) 