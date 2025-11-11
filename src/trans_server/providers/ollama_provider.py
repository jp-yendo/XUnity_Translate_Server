"""Ollama provider implementation."""

import argparse
from dataclasses import dataclass
import ollama
from ..data_models import ProviderConfig
from ..mods.prompt_builder import PromptBuilder
from .base_provider import BaseProvider


@dataclass
class OllamaConfig:
    """Ollama-specific configuration"""

    api_base: str = "http://localhost:11434"


class OllamaProvider(BaseProvider):
    """Ollama provider"""

    def __init__(self, config: ProviderConfig, ollama_config: OllamaConfig):
        super().__init__(config)
        self.ollama_config = ollama_config
        self.client = ollama.Client(host=ollama_config.api_base)
        self.prompt_builder = PromptBuilder()

    def list_models(self) -> list[str]:
        """Get available models"""
        response = self.client.list()
        # pylint: disable=no-member
        return [m.model for m in response.models if m.model]  # type: ignore[attr-defined]

    def translate(self, text: str, src_lang: str, dst_lang: str) -> str:
        """Execute translation (1-to-1)"""
        src_lang = self.resolve_source_language(src_lang)
        dst_lang = self.resolve_target_language(dst_lang)

        # Build prompts
        system_prompt = self.prompt_builder.build_system_prompt(self.config.summary)
        user_prompt = self.prompt_builder.build_translation_request(text, src_lang, dst_lang)

        # API call
        response = self.client.chat(
            model=self.config.model,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            options={
                "temperature": 0.3,
            },
        )

        # Extract translation
        content = response["message"]["content"]
        translation = self.prompt_builder.extract_translation(content)

        return translation

    @staticmethod
    def add_provider_args(parser: argparse.ArgumentParser) -> None:
        """Add Ollama-specific arguments"""
        parser.add_argument("--api-base", default="http://localhost:11434", help="Ollama server base URL (default: http://localhost:11434)")

    @staticmethod
    def create_from_args(args: argparse.Namespace) -> "OllamaProvider":
        """Create provider instance from arguments"""
        config = ProviderConfig(
            provider=args.provider,
            model=args.model,
            summary=args.summary,
            fallback_src_lang=args.fallback_from,
            fallback_dst_lang=args.fallback_to,
        )
        ollama_config = OllamaConfig(
            api_base=getattr(args, "api_base", "http://localhost:11434"),
        )
        return OllamaProvider(config, ollama_config)
