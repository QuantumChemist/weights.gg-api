import os
import time
import asyncio
import aiohttp
import json  # Import the json module
from typing import Optional, Callable, Any, Dict
from dataclasses import dataclass, field

@dataclass
class WeightsApi:
    """
    A class to interact with the Weights API.

    attr api_key: Optional[str]: API key for authentication.
    attr endpoint: Optional[str]: API endpoint URL.
    attr session: Optional[aiohttp.ClientSession]: HTTP session for making requests.
    """
    api_key: Optional[str] = None
    endpoint: Optional[str] = field(default_factory=lambda: os.getenv('WEIGHTS_UNOFFICIAL_ENDPOINT', 'http://localhost:3000'))
    session: Optional[aiohttp.ClientSession] = field(init=False, default=None)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def api_call(self, path: str, method: str = 'GET', body: Optional[Dict] = None) -> aiohttp.ClientResponse:
        """
        Makes an async HTTP request to the API endpoint
        """
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': str(self.api_key)
        }
        
        url = self.endpoint + path
        
        try:
            if method == 'GET' and body:
                params = {}
                for key, value in body.items():
                    if value is not None:
                        params[key] = str(value)  # Convert values to string
                async with self.session.get(url, params=params, headers=headers) as response:
                    response.raise_for_status()
                    return response
            else:
                async with self.session.request(method, url, json=body, headers=headers) as response:
                    response.raise_for_status()
                    return response
        except aiohttp.ClientError as e:
            raise Exception(f"Weights API Error: {e}")

    async def _check_health(self):
        """
        Checks the health of the API and raises an exception if it's not reachable.
        """
        try:
            await self.get_health_data()
        except Exception as e:
            raise Exception(f"Weights API Error: The API is not reachable. Please check your connection or the API status: {e}")

    async def get_health_data(self) -> Dict:
        """
        Retrieves health status of the API
        """
        try:
            response = await self.api_call('/health')
            return await response.json()
        except Exception as e:
            raise Exception(f"Weights API Error: {e}")

    async def call_with_health_check(self, api_call: Callable[[], Any]) -> Any:
        """
        Wraps API calls with health check
        """
        try:
            await self._check_health()
            return await api_call()
        except Exception as e:
            raise Exception(f"Weights API Error: The API is not reachable. Please check your connection or the API status: {e}")
        
    async def _api_call_wrapper(self, path: str, method: str = 'GET', body: Optional[Dict] = None, response_type: str = 'json'):
        """
        A wrapper for API calls that handles the request and response.
        """
        async def call():
            response = await self.api_call(path, method=method, body=body)
            if response_type == 'json':
                return await response.json()
            elif response_type == 'text':
                return await response.text()
            else:
                raise ValueError(f"Unsupported response type: {response_type}")
        return await self.call_with_health_check(call)


    async def get_status(self, image_id: str) -> Dict:
        """
        Gets the status of a specific image
        """
        return await self._api_call_wrapper(f'/status/{image_id}')

    async def get_quota(self) -> str:
        """
        Retrieves quota information
        """
        return await self._api_call_wrapper('/quota', response_type='text')

    async def search_loras(self, query: str) -> Dict:
        """
        Searches for Lora models
        """
        return await self._api_call_wrapper('/search-loras', body={'query': query})

    async def generate_image(self, prompt: str, lora_name: Optional[str] = None) -> Dict:
        """
        Generates an image based on parameters
        """
        params = {'prompt': prompt, 'loraName': lora_name}
        return await self._api_call_wrapper('/generateImage', body=params)


    async def generate_progressive_image(self, prompt: str, lora_name: Optional[str] = None, 
                                      callback: Callable[[str, Dict], None] = lambda status, data: None) -> Dict:
        """
        Generates a progressive image with status updates
        """
        await self._check_health()

        result = await self.generate_image(prompt, lora_name)
        image_id = result['imageId']
        status_response = await self.get_status(image_id)
        status = status_response.get('status')
        callback(status, {'imageId': image_id})
        if status == 'COMPLETED':
            return status_response
        old_modified_date = None
        while True:
            await asyncio.sleep(0.1)
            status_response = await self.get_status(image_id)
            status = status_response.get('status')
            last_modified_date = status_response.get('lastModifiedDate')
            error = status_response.get('error')
            
            if old_modified_date != last_modified_date:
                old_modified_date = last_modified_date
                callback(status, {'imageId': image_id})
            
            if status == 'COMPLETED':
                break
            
            if status == 'FAILED':
                raise Exception(f"Image generation failed: {error}")
        return status_response
