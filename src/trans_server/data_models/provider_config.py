"""Provider configuration data model."""

from dataclasses import dataclass
from typing import Optional
from ..utils.language_mapper import LanguageMapper


@dataclass
class ProviderConfig:
    """プロバイダ共通設定"""

    provider: str  # プロバイダ名 (openai, anthropic, ollama, etc.)
    model: str  # 使用するモデル名
    summary: Optional[str] = None  # アプリケーション概要
    fallback_src_lang: Optional[str] = None  # フォールバック翻訳元言語
    fallback_dst_lang: Optional[str] = None  # フォールバック翻訳先言語

    def __post_init__(self):
        """初期化後の検証"""
        # fallback言語コードのバリデーション
        if self.fallback_src_lang:
            LanguageMapper.validate_language_code(self.fallback_src_lang, "Fallback from")
        if self.fallback_dst_lang:
            LanguageMapper.validate_language_code(self.fallback_dst_lang, "Fallback to")
