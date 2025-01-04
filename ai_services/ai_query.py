from poe_api_wrapper import AsyncPoeApi
import asyncio
import json
from duckduckgo_search import DDGS
import threading

tokens = {
    'p-b': 'j_z0wVswlfUC63DA9IK9yg%3D%3D', 
    'p-lat': '5Q99zQvBGN3OdCSZW%2BO%2FKY61dH%2Bt6D5NdSwH%2F62qLw%3D%3D',
}

async def query_ai(message, file_paths=None, online_search=False):
    client = await AsyncPoeApi(tokens=tokens).create()
    
    if online_search:
        search_query = await get_search_query(client, message)
        print(f"Search query: {search_query}")
        search_results = perform_ddg_search(search_query)
        print("Search Results:")
        for result in search_results:
            print(json.dumps(result, indent=2))
    
    response = ""
    #kwargs = {"bot": "Claude-3-Opus", "message": message}
    kwargs = {"bot": "Claude-3-Sonnet", "message": message} #lets just use sonnet for the full response while debugging
    if file_paths:
        kwargs["file_path"] = file_paths
    async for chunk in client.send_message(**kwargs):
        response += chunk["response"]
    return response

async def get_search_query(client, user_query):
    sonnet_prompt = f"""
Given the following user prompt, generate 3 search queries for DuckDuckGo to find more info on the subject, but keep in mind we want to combine those 3 queries into DuckDuckGo's semantically simlar search which is described like this:

```
~"cats and dogs"	Experimental syntax: more results that are semantically similar to "cats and dogs", like "cats & dogs" and "dogs and cats" in addition to "cats and dogs".
```

We want the 3 search queries combined into one long query with this format:

~"can cats and dogs live together" OR ~"fun facts about cats and dogs" OR ~"should I get a cat and a dog"

Convert acronyms to the full phrase if you are sure you know what they mean. Try and use alternate words where possible to maximise the variation of results.

Return only the search query, without any explanation or additional text.

    User query: {user_query}
    """
    
    search_query = ""
    async for chunk in client.send_message(bot="Claude-3-Sonnet", message=sonnet_prompt):
        search_query += chunk["response"]
    
    return search_query.strip()

def perform_ddg_search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(
            query,
            region='wt-wt',
            safesearch='moderate',
            timelimit='m24',  # Last 24 months (2 years)
            max_results=5
        ))
    return results

def query_ai_sync(message, file_paths=None, online_search=False):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(query_ai(message, file_paths, online_search))
    finally:
        loop.close()