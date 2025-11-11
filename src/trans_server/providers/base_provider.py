"""Base provider interface."""

from abc import ABC, abstractmethod
from typing import Optional
import argparse
from ..data_models import ProviderConfig


class BaseProvider(ABC):
    """Translation provider base class"""

    def __init__(self, config: ProviderConfig):
        self.config = config

    @abstractmethod
    def list_models(self) -> list[str]:
        """Get available models"""
        ...

    @abstractmethod
    def translate(self, text: str, src_lang: str, dst_lang: str) -> str:
        """Execute translation (1-to-1)"""
        ...

    @staticmethod
    @abstractmethod
    def add_provider_args(parser: argparse.ArgumentParser) -> None:
        """Add provider-specific arguments"""
        ...

    @staticmethod
    @abstractmethod
    def create_from_args(args: argparse.Namespace) -> "BaseProvider":
        """Create provider instance from arguments"""
        ...

    def _resolve_language(self, lang: Optional[str], fallback: Optional[str], lang_type: str) -> str:
        """Resolve language code (with fallback)"""
        if lang:
            return lang

        if fallback:
            return fallback

        raise ValueError(f"{lang_type} language not specified and no fallback configured")

    def resolve_source_language(self, src_lang: Optional[str]) -> str:
        """Resolve source language"""
        return self._resolve_language(src_lang, self.config.fallback_src_lang, "Source")

    def resolve_target_language(self, dst_lang: Optional[str]) -> str:
        """Resolve target language"""
        return self._resolve_language(dst_lang, self.config.fallback_dst_lang, "Target")
