from app.llm.base_provider import BaseProvider
from google import genai
from google.genai import types
from google.genai.client import AsyncClient
from app.llm.llm_interaction import LLMInteraction

class GeminiProvider(BaseProvider,LLMInteraction):
    client:AsyncClient
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash",config={},temperature:float=1, **kwargs):
        super().__init__(api_key=api_key, model=model, config=config,temperature=temperature)
        
        self.client = genai.Client(api_key=self.api_key).aio


    async def create_client(self):
        client = genai.Client(api_key=self.api_key)
        return client
    
    async def generate_content_by_prompt(self, prompt: str, context: str = ""):
        contents = []
        config = None
        contents.append(prompt)
        config = types.GenerateContentConfig(temperature=self.temperature)
        if context:
            config.system_instruction=context
            
        response = await self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config 
        )
        
        return response.text or ""


    def __create_chat_history(self, messages: list[dict]) -> list[types.ContentOrDict]:
        history: list[types.ContentOrDict] = []
        for message in messages:
            role = message.get("role", "user") 
            text = message.get("content", "")
            
            history.append(types.Content(role=role, parts=[types.Part(text=text)]))
        return history
    
    async def generate_content_by_chat(self,current_message:str, messages: list[dict], context: str="") -> str:
        history: list[types.ContentOrDict] = self.__create_chat_history(messages)

        config: types.GenerateContentConfig | None = types.GenerateContentConfig(temperature=self.temperature)
        if context:
            config.system_instruction = context

        chat_session = self.client.chats.create(
            model=self.model, 
            history=history, 
            config=config    
        )
        
        response = await chat_session.send_message(message=current_message)
        
        return response.text or ""