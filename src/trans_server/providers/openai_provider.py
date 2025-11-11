"""OpenAI provider implementation."""

import argparse
from dataclasses import dataclass
from typing import Optional
from openai import OpenAI
from ..data_models import ProviderConfig
from ..mods.prompt_builder import PromptBuilder
from .base_provider import BaseProvider


@dataclass
class OpenAIConfig:
    """OpenAI-specific configuration"""

    api_key: str
    organization: Optional[str] = None


class OpenAIProvider(BaseProvider):
    """OpenAI provider"""

    def __init__(self, config: ProviderConfig, openai_config: OpenAIConfig):
        super().__init__(config)
        self.openai_config = openai_config

        # Initialize client
        client_kwargs = {"api_key": openai_config.api_key}
        if openai_config.organization:
            client_kwargs["organization"] = openai_config.organization

        self.client = OpenAI(**client_kwargs)  # type: ignore[arg-type]
        self.prompt_builder = PromptBuilder()

    def list_models(self) -> list[str]:
        """Get available models"""
        models = self.client.models.list()
        return [model.id for model in models.data]

    def translate(self, text: str, src_lang: str, dst_lang: str) -> str:
        """Execute translation (1-to-1)"""
        src_lang = self.resolve_source_language(src_lang)
        dst_lang = self.resolve_target_language(dst_lang)

        # Build prompts
        system_prompt = self.prompt_builder.build_system_prompt(self.config.summary)
        user_prompt = self.prompt_builder.build_translation_request(text, src_lang, dst_lang)

        # API call
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
        )

        # Extract translation
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI API")
        translation = self.prompt_builder.extract_translation(content)

        return translation

    @staticmethod
    def add_provider_args(parser: argparse.ArgumentParser) -> None:
        """Add OpenAI-specific arguments"""
        parser.add_argument("--api-key", required=True, help="OpenAI API key")
        parser.add_argument("--organization", help="Organization ID (optional)")

    @staticmethod
    def create_from_args(args: argparse.Namespace) -> "OpenAIProvider":
        """Create provider instance from arguments"""
        config = ProviderConfig(
            provider=args.provider,
            model=args.model,
            summary=args.summary,
            fallback_src_lang=args.fallback_from,
            fallback_dst_lang=args.fallback_to,
        )
        openai_config = OpenAIConfig(
            api_key=args.api_key,
            organization=getattr(args, "organization", None),
        )
        return OpenAIProvider(config, openai_config)
