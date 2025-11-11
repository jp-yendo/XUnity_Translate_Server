"""Language code to natural language mapper."""


class LanguageMapper:
    """Google翻訳の言語コードから自然言語名へのマッピング"""

    LANGUAGE_MAP = {
        # East Asian Languages
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "zh-CN": "Simplified Chinese",
        "zh-TW": "Traditional Chinese",
        "yue": "Cantonese",
        # English Variants
        "en": "English",
        "en-US": "American English",
        "en-GB": "British English",
        "en-AU": "Australian English",
        "en-CA": "Canadian English",
        "en-NZ": "New Zealand English",
        "en-IE": "Irish English",
        "en-ZA": "South African English",
        # European Languages - Western
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "pt-BR": "Brazilian Portuguese",
        "pt-PT": "European Portuguese",
        "nl": "Dutch",
        "ca": "Catalan",
        "gl": "Galician",
        "eu": "Basque",
        # European Languages - Northern
        "sv": "Swedish",
        "no": "Norwegian",
        "nb": "Norwegian Bokmål",
        "nn": "Norwegian Nynorsk",
        "da": "Danish",
        "fi": "Finnish",
        "is": "Icelandic",
        # European Languages - Eastern
        "ru": "Russian",
        "pl": "Polish",
        "cs": "Czech",
        "sk": "Slovak",
        "hu": "Hungarian",
        "ro": "Romanian",
        "uk": "Ukrainian",
        "bg": "Bulgarian",
        "sr": "Serbian",
        "hr": "Croatian",
        "sl": "Slovenian",
        "mk": "Macedonian",
        "be": "Belarusian",
        "lt": "Lithuanian",
        "lv": "Latvian",
        "et": "Estonian",
        "sq": "Albanian",
        # European Languages - Southern
        "el": "Greek",
        "tr": "Turkish",
        "mt": "Maltese",
        # Middle Eastern Languages
        "ar": "Arabic",
        "he": "Hebrew",
        "fa": "Persian",
        "ur": "Urdu",
        "ku": "Kurdish",
        # South Asian Languages
        "hi": "Hindi",
        "bn": "Bengali",
        "pa": "Punjabi",
        "ta": "Tamil",
        "te": "Telugu",
        "mr": "Marathi",
        "gu": "Gujarati",
        "kn": "Kannada",
        "ml": "Malayalam",
        "si": "Sinhala",
        "ne": "Nepali",
        # Southeast Asian Languages
        "th": "Thai",
        "vi": "Vietnamese",
        "id": "Indonesian",
        "ms": "Malay",
        "tl": "Tagalog",
        "fil": "Filipino",
        "my": "Burmese",
        "km": "Khmer",
        "lo": "Lao",
        # Central Asian Languages
        "kk": "Kazakh",
        "uz": "Uzbek",
        "ky": "Kyrgyz",
        "tk": "Turkmen",
        "tg": "Tajik",
        "mn": "Mongolian",
        # African Languages
        "sw": "Swahili",
        "am": "Amharic",
        "ha": "Hausa",
        "ig": "Igbo",
        "yo": "Yoruba",
        "zu": "Zulu",
        "xh": "Xhosa",
        "af": "Afrikaans",
        "so": "Somali",
        # Other Languages
        "az": "Azerbaijani",
        "ka": "Georgian",
        "hy": "Armenian",
        "iw": "Hebrew",
        "yi": "Yiddish",
        "cy": "Welsh",
        "ga": "Irish",
        "gd": "Scottish Gaelic",
        "lb": "Luxembourgish",
        "fo": "Faroese",
        "eo": "Esperanto",
        "la": "Latin",
        # Additional variants
        "auto": "Auto-detect",
    }

    @classmethod
    def get_language_name(cls, lang_code: str) -> str:
        """言語コードから言語名を取得"""
        return cls.LANGUAGE_MAP.get(lang_code, lang_code)

    @classmethod
    def is_supported(cls, lang_code: str) -> bool:
        """サポートされている言語コードかチェック"""
        return lang_code in cls.LANGUAGE_MAP
