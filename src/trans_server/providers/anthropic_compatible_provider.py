"""Anthropic-compatible provider implementation."""

import argparse
from dataclasses import dataclass
from anthropic import Anthropic
from anthropic.types import TextBlock
from ..data_models import ProviderConfig
from ..mods.prompt_builder import PromptBuilder
from .base_provider import BaseProvider


@dataclass
class AnthropicCompatibleConfig:
    """Anthropic-compatible service configuration"""

    api_key: str
    api_base: str  # Required for compatible services


class AnthropicCompatibleProvider(BaseProvider):
    """Anthropic-compatible provider"""

    def __init__(self, config: ProviderConfig, anthropic_config: AnthropicCompatibleConfig):
        super().__init__(config)
        self.anthropic_config = anthropic_config

        # Initialize client with base_url (required for compatible services)
        self.client = Anthropic(api_key=anthropic_config.api_key, base_url=anthropic_config.api_base)  # type: ignore[arg-type]
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
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.3,
        )

        # Extract translation
        first_content = response.content[0]
        if isinstance(first_content, TextBlock):
            content = first_content.text
        else:
            raise ValueError(f"Invalid response format from Anthropic-compatible API: {type(first_content)}")
        translation = self.prompt_builder.extract_translation(content)

        return translation

    @staticmethod
    def add_provider_args(parser: argparse.ArgumentParser) -> None:
        """Add Anthropic-compatible specific arguments"""
        parser.add_argument("--api-key", required=True, help="API key")
        parser.add_argument("--api-base", required=True, help="API base URL (required for Anthropic-compatible services)")

    @staticmethod
    def create_from_args(args: argparse.Namespace) -> "AnthropicCompatibleProvider":
        """Create provider instance from arguments"""
        config = ProviderConfig(
            provider=args.provider,
            model=args.model,
            summary=args.summary,
            fallback_src_lang=args.fallback_from,
            fallback_dst_lang=args.fallback_to,
        )
        anthropic_config = AnthropicCompatibleConfig(
            api_key=args.api_key,
            api_base=args.api_base,
        )
        return AnthropicCompatibleProvider(config, anthropic_config)
