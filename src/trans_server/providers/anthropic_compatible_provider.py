"""Anthropic-compatible provider implementation."""

import argparse
from dataclasses import dataclass
from anthropic import Anthropic
from ..data_models import ProviderConfig
from ..mods.prompt_builder import PromptBuilder
from .anthropic_provider import AnthropicProvider, AnthropicConfig


@dataclass
class AnthropicCompatibleConfig:
    """Anthropic-compatible service configuration"""

    api_key: str | None = None  # Some services don't require API key
    api_base: str = ""  # Required for compatible services


class AnthropicCompatibleProvider(AnthropicProvider):
    """Anthropic-compatible provider"""

    def __init__(self, config: ProviderConfig, anthropic_config: AnthropicCompatibleConfig):
        # Initialize with dummy AnthropicConfig to satisfy parent __init__
        dummy_config = AnthropicConfig(
            api_key=anthropic_config.api_key if anthropic_config.api_key else "sk-ant-no-key-required",
        )
        # Don't call super().__init__ yet, we need to override client creation
        super(AnthropicProvider, self).__init__(config)  # Call BaseProvider.__init__
        self.anthropic_config = anthropic_config

        # Initialize client with base_url (required for compatible services)
        # api_key is optional for some services
        # If not provided, use a dummy key to ensure compatibility
        self.client = Anthropic(
            api_key=anthropic_config.api_key if anthropic_config.api_key else "sk-ant-no-key-required",
            base_url=anthropic_config.api_base,
        )
        self.prompt_builder = PromptBuilder()

    @staticmethod
    def add_provider_args(parser: argparse.ArgumentParser) -> None:
        """Add Anthropic-compatible specific arguments"""
        parser.add_argument("--api-key", help="API key (optional, some services don't require it)")
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
