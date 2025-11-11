"""OpenAI-compatible provider implementation."""

import argparse
from dataclasses import dataclass
from openai import OpenAI
from ..data_models import ProviderConfig
from ..mods.prompt_builder import PromptBuilder
from .openai_provider import OpenAIProvider, OpenAIConfig


@dataclass
class OpenAICompatibleConfig:
    """OpenAI-compatible service configuration"""

    api_key: str | None = None  # Some services don't require API key
    api_base: str = ""  # Required for compatible services
    organization: str | None = None


class OpenAICompatibleProvider(OpenAIProvider):
    """OpenAI-compatible provider (Azure OpenAI, LocalAI, etc.)"""

    def __init__(self, config: ProviderConfig, openai_config: OpenAICompatibleConfig):
        # Initialize with dummy OpenAIConfig to satisfy parent __init__
        dummy_config = OpenAIConfig(
            api_key=openai_config.api_key if openai_config.api_key else "sk-no-key-required",
            organization=openai_config.organization,
        )
        # Don't call super().__init__ yet, we need to override client creation
        super(OpenAIProvider, self).__init__(config)  # Call BaseProvider.__init__
        self.openai_config = openai_config

        # Initialize client with base_url (required for compatible services)
        # api_key is optional for some services (e.g., LocalAI)
        # If not provided, use a dummy key to bypass OpenAI client validation
        self.client = OpenAI(
            api_key=openai_config.api_key if openai_config.api_key else "sk-no-key-required",
            base_url=openai_config.api_base,
            organization=openai_config.organization,
        )
        self.prompt_builder = PromptBuilder()

    @staticmethod
    def add_provider_args(parser: argparse.ArgumentParser) -> None:
        """Add OpenAI-compatible specific arguments"""
        parser.add_argument("--api-key", help="API key (optional, some services don't require it)")
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
