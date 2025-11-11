"""Provider configuration data model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ProviderConfig:
    """プロバイダ共通設定"""

    provider: str  # プロバイダ名 (openai, anthropic, ollama, etc.)
    model: str  # 使用するモデル名
    summary: Optional[str] = None  # アプリケーション概要
    fallback_src_lang: Optional[str] = None  # フォールバック翻訳元言語
    fallback_dst_lang: Optional[str] = None  # フォールバック翻訳先言語
