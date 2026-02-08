from abc import ABC, abstractmethod


class LLMInteraction(ABC):

    @abstractmethod
    async def generate_content_by_prompt(self, prompt: str, context: str = "") -> str:
        """Send a single prompt with optional context"""
        pass

    @abstractmethod
    async def generate_content_by_chat(self, current_message:str, messages: list[dict], context: str = "") -> str:
        """
        Send a chat sequence with optional context.
        messages: [{"role": "user|ai", "content": "..."}]
        context: optional text to provide information
        """
        pass