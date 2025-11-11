"""OpenAI-compatible provider implementation."""

import argparse
from dataclasses import dataclass
from openai import OpenAI
from ..data_models import ProviderConfig
from ..mods.prompt_builder import PromptBuilder
from .base_provider import BaseProvider


@dataclass
class OpenAICompatibleConfig:
    """OpenAI-compatible service configuration"""

    api_key: str
    api_base: str  # Required for compatible services
    organization: str | None = None


class OpenAICompatibleProvider(BaseProvider):
    """OpenAI-compatible provider (Azure OpenAI, LocalAI, etc.)"""

    def __init__(self, config: ProviderConfig, openai_config: OpenAICompatibleConfig):
        super().__init__(config)
        self.openai_config = openai_config

        # Initialize client with base_url (required for compatible services)
        self.client = OpenAI(
            api_key=openai_config.api_key,
            base_url=openai_config.api_base,
            organization=openai_config.organization,
        )  # type: ignore[arg-type]
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
            raise ValueError("Empty response from OpenAI-compatible API")
        translation = self.prompt_builder.extract_translation(content)

        return translation

    @staticmethod
    def add_provider_args(parser: argparse.ArgumentParser) -> None:
        """Add OpenAI-compatible specific arguments"""
        parser.add_argument("--api-key", required=True, help="API key")
        parser.add_argument("--api-base", required=True, help="API base URL (required for OpenAI-compatible services)")
        parser.add_argument("--organization", help="Organization ID (optional)")

    @staticmethod
    def create_from_args(args: argparse.Namespace) -> "OpenAICompatibleProvider":
        """Create provider instance from arguments"""
        config = ProviderConfig(
            provider=args.provider,
            model=args.model,
            summary=args.summary,
            fallback_src_lang=args.fallback_from,
            fallback_dst_lang=args.fallback_to,
        )
        openai_config = OpenAICompatibleConfig(
            api_key=args.api_key,
            api_base=args.api_base,
            organization=getattr(args, "organization", None),
        )
        return OpenAICompatibleProvider(config, openai_config)
