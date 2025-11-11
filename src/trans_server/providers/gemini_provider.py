"""Google AI Studio (Gemini) プロバイダ"""

import argparse
from dataclasses import dataclass

try:
    import google.generativeai as genai
except ImportError as e:
    raise ImportError(f"google-generativeai パッケージのインストールが必要です: pip install google-generativeai. Error: {e}") from e

from ..data_models import ProviderConfig
from ..mods.prompt_builder import PromptBuilder
from .base_provider import BaseProvider


@dataclass
class GeminiConfig:
    """Gemini プロバイダ設定 (--api-base は不要)"""

    api_key: str


class GeminiProvider(BaseProvider):
    """Google AI Studio (Gemini) API プロバイダ"""

    def __init__(self, config: ProviderConfig, gemini_config: GeminiConfig):
        super().__init__(config)
        self.gemini_config = gemini_config
        # Configure API key globally
        genai.configure(api_key=gemini_config.api_key)
        self.prompt_builder = PromptBuilder()

    def list_models(self) -> list[str]:
        """利用可能なモデル一覧を取得"""
        # List models that support generateContent
        models = []
        for model in genai.list_models():
            if "generateContent" in model.supported_generation_methods:
                models.append(model.name)
        return models

    def translate(self, text: str, src_lang: str, dst_lang: str) -> str:
        """テキストを翻訳"""
        src_lang = self.resolve_source_language(src_lang)
        dst_lang = self.resolve_target_language(dst_lang)

        # Build prompts
        system_prompt = self.prompt_builder.build_system_prompt(self.config.summary)
        user_prompt = self.prompt_builder.build_translation_request(text, src_lang, dst_lang)

        # Create model instance
        model_instance = genai.GenerativeModel(
            self.config.model,
            system_instruction=system_prompt,
        )

        try:
            # Generate content
            response = model_instance.generate_content(
                user_prompt,
                generation_config=genai.GenerationConfig(temperature=0.3),
            )

            # Parse response
            if response and response.text:
                content = response.text
                translation = self.prompt_builder.extract_translation(content)
                return translation

            raise ValueError("Empty response from Gemini API")

        except Exception as e:
            raise RuntimeError(f"Gemini API translation failed: {e}") from e

    @staticmethod
    def add_provider_args(parser: argparse.ArgumentParser) -> None:
        """Gemini プロバイダの引数を追加"""
        parser.add_argument("--api-key", required=True, help="Google AI Studio API key")

    @staticmethod
    def create_from_args(args: argparse.Namespace) -> "GeminiProvider":
        """引数からプロバイダインスタンスを作成"""
        config = ProviderConfig(
            provider=args.provider,
            model=args.model,
            summary=args.summary,
            fallback_src_lang=args.fallback_from,
            fallback_dst_lang=args.fallback_to,
        )
        gemini_config = GeminiConfig(api_key=args.api_key)
        return GeminiProvider(config, gemini_config)
