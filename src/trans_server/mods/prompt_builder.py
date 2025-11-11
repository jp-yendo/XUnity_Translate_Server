"""Prompt builder for AI translation."""

import re
from typing import Optional
from ..utils.language_mapper import LanguageMapper


class PromptBuilder:
    """AI翻訳用のプロンプト構築"""

    @staticmethod
    def build_system_prompt(app_summary: Optional[str] = None) -> str:
        """システムプロンプトを構築"""
        base_prompt = """You are a professional translator for games and applications.

CRITICAL RULES:
1. Preserve ALL whitespace exactly (leading/trailing spaces, newlines, indentation)
2. Keep similar character count - use concise wording and short synonyms
3. Maintain original line breaks and formatting
4. Leave technical terms, abbreviations, and stats unchanged if commonly understood (e.g., ATK, HP, MP, ID)
5. Only translate terms unfamiliar to target language speakers
6. Prioritize brevity - use shorter expressions when possible"""

        if app_summary:
            base_prompt += f"\n\nContext: {app_summary}"

        return base_prompt

    @staticmethod
    def build_translation_request(text: str, src_lang: str, dst_lang: str) -> str:
        """翻訳リクエストプロンプトを構築（フラットな疑似XML形式）"""
        src_lang_name = LanguageMapper.get_language_name(src_lang)
        dst_lang_name = LanguageMapper.get_language_name(dst_lang)

        prompt = f"""Translate from {src_lang_name} to {dst_lang_name}:

<request_text>{text}</request_text>

Output format:
<translate>your translation here</translate>

Rules:
- Output ONLY the <translate> tag with translation
- NO explanations or extra text
- Keep exact same whitespace/newlines
- Use concise wording to maintain character count
- Leave universal terms unchanged (ATK, HP, etc.)"""

        return prompt

    @staticmethod
    def extract_translation(response: str) -> str:
        """AI応答から翻訳結果を抽出"""
        # <translate>...</translate>のパターンで抽出（改行や空白も含む）
        pattern = r"<translate>(.*?)</translate>"
        match = re.search(pattern, response, re.DOTALL)

        if not match:
            raise ValueError(f"Failed to extract translation. Response: {response[:200]}...")

        translation = match.group(1)
        return translation
