import asyncio
import websockets
import json
from rankingV1 import rankV1 
from rankingV2 import rankV2

# Function to handle the connection with the client
async def handle_connection(websocket, path):
   
    if path == "/rankV1":
        
        # Receive the message from the client
        message = await websocket.recv()
        print(f"Message received from client: {message}")

        data = json.loads(message)
        
        papers = data.get("papers")
        query = data.get("query")

        # Call the Python function passing the message (parameter)
        result = rankV1(papers, query)
        
        
        # Convert the result to JSON format
        json_result = json.dumps(result)
        
        # Send the result to the client
        await websocket.send(json_result)

    elif path == "/rankV2":
       
        message = await websocket.recv()
        print(f"Message received from client: {message}")

        data = json.loads(message)
        
        papers = data.get("papers")
        query = data.get("query")

        result = rankV2(papers, query)
        
        
        json_result = json.dumps(result)
        
        await websocket.send(json_result)
       

# Function to start the WebSocket server
async def main():
    # Start the WebSocket server on port 8765
    server = await websockets.serve(handle_connection, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

# Start the server
asyncio.run(main())