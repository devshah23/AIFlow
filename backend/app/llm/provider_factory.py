from app.llm.providers.gemini_provider import GeminiProvider


class ProviderFactory:

    registry = {
        "gemini": GeminiProvider,
        # "openai": OpenAIProvider,
    }

    @staticmethod
    def create(provider_name: str, api_key: str, model: str,temperature:float, config: dict={}):
        provider_cls = ProviderFactory.registry.get(provider_name.lower())
        if not provider_cls:
            raise ValueError(f"Unknown provider: {provider_name}")

        return provider_cls(api_key=api_key, model=model, config=config,temperature=temperature)
