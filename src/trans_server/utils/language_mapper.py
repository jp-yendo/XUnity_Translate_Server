"""Language code to natural language mapper."""


class LanguageMapper:
    """Google翻訳の言語コードから自然言語名へのマッピング"""

    LANGUAGE_MAP = {
        "ja": "Japanese",
        "en": "English",
        "zh-CN": "Simplified Chinese",
        "zh-TW": "Traditional Chinese",
        "ko": "Korean",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ar": "Arabic",
        "th": "Thai",
        "vi": "Vietnamese",
        "id": "Indonesian",
        "ms": "Malay",
        "hi": "Hindi",
        "tr": "Turkish",
        "pl": "Polish",
        "nl": "Dutch",
        "sv": "Swedish",
        "no": "Norwegian",
        "da": "Danish",
        "fi": "Finnish",
        "cs": "Czech",
        "hu": "Hungarian",
        "ro": "Romanian",
        "uk": "Ukrainian",
        "bg": "Bulgarian",
        "el": "Greek",
        "he": "Hebrew",
    }

    @classmethod
    def get_language_name(cls, lang_code: str) -> str:
        """言語コードから言語名を取得"""
        return cls.LANGUAGE_MAP.get(lang_code, lang_code)

    @classmethod
    def is_supported(cls, lang_code: str) -> bool:
        """サポートされている言語コードかチェック"""
        return lang_code in cls.LANGUAGE_MAP
