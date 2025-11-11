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
- Output ONLY the <translate> tag with translation
- NO explanations or extra text
- Preserve ALL whitespace exactly (leading/trailing spaces, newlines, indentation)
- Preserve ALL tags and markup structure (translate only the content within tags)
- For single words or short phrases, aim for balanced character width using concise wording (multibyte chars = width 2, single-byte chars = width 1)
- Maintain original line breaks and formatting
- Keep terms already established in the target language region (e.g., in Japan: ATK, HP, MP, ID)"""

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
- Preserve all tags and markup (translate content only)
- For short text, aim for balanced character width using concise wording (multibyte = 2, single-byte = 1)
- Keep established terms unchanged (e.g., in Japan: ATK, HP, MP)"""

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
