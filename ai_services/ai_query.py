from poe_api_wrapper import AsyncPoeApi
import asyncio
import json

tokens = {
    'p-b': 'j_z0wVswlfUC63DA9IK9yg%3D%3D', 
    'p-lat': '5Q99zQvBGN3OdCSZW%2BO%2FKY61dH%2Bt6D5NdSwH%2F62qLw%3D%3D',
}

async def query_ai(message, file_paths=None):
    client = await AsyncPoeApi(tokens=tokens).create()
    response = ""
    kwargs = {"bot": "Claude-3-Opus", "message": message}
    if file_paths:
        kwargs["file_path"] = file_paths
    async for chunk in client.send_message(**kwargs):
        response += chunk["response"]
    return response

def query_ai_sync(message, file_paths=None):
    return asyncio.run(query_ai(message, file_paths))