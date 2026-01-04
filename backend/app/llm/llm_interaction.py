from abc import ABC, abstractmethod


class LLMInteraction(ABC):

    @abstractmethod
    async def send_prompt(self, prompt: str, context: str = "") -> str:
        """Send a single prompt with optional retrieved context"""
        pass

    @abstractmethod
    async def send_chat(self, current_message:str, messages: list[dict], context: str = "") -> str:
        """
        Send a chat sequence with optional retrieved context.
        messages: [{"role": "user|ai", "content": "..."}]
        context: optional text to prepend or append to messages
        """
        pass