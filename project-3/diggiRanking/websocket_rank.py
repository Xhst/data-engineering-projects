import asyncio
import websockets
import json
from rankingV1 import rank 

# Function to handle the connection with the client
async def handle_connection(websocket, path):
   
   if path == "/rank":
        # Receive the message from the client
        message = await websocket.recv()
        print(f"Message received from client: {message}")
        
        # Call the Python function passing the message (parameter)
        result = rank(message)
        
        # TO-DO
        papers = ""
        query = ""
        
        # Convert the result to JSON format
        json_result = json.dumps(papers,query)
        
        # Send the result to the client
        await websocket.send(json_result)

# Function to start the WebSocket server
async def main():
    # Start the WebSocket server on port 8765
    server = await websockets.serve(handle_connection, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

# Start the server
asyncio.run(main())