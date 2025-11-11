"""Translation server implementation."""

import sys
import traceback
from flask import Flask, request
from ..providers.base_provider import BaseProvider
from ..utils.language_mapper import LanguageMapper
from .text_filter import is_dynamic_value, should_skip_translation


class TranslationServer:
    """Translation server"""

    def __init__(self, provider: BaseProvider):
        self.provider = provider
        self.app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        """Setup routes"""
        self.app.route("/translate", methods=["GET"])(self.handle_translate)
        self.app.route("/health", methods=["GET"])(self.handle_health)

    def handle_health(self):
        """Health check endpoint"""
        return "ok", 200, {"Content-Type": "text/plain; charset=utf-8"}

    def handle_translate(self):
        """Translation endpoint (CustomTranslate specification)

        GET /translate?from={source_lang}&to={target_lang}&text={text}
        Returns: Plain text translation
        """
        # Parse query parameters
        src_lang = request.args.get("from")
        dst_lang = request.args.get("to")
        text = request.args.get("text")

        if not text:
            # Return error status for missing text parameter
            return "", 400, {"Content-Type": "text/plain; charset=utf-8"}

        # 動的な値(FPS表示など)をチェック(先にチェック)
        if is_dynamic_value(text):
            # 動的な値は400を返す(翻訳をキャッシュさせない)
            return "", 400, {"Content-Type": "text/plain; charset=utf-8"}

        # 翻訳不要なテキスト(数字・空白・記号のみ)をチェック
        if should_skip_translation(text):
            # そのまま返す(200で返してキャッシュ)
            return text, 200, {"Content-Type": "text/plain; charset=utf-8"}

        # Use fallback languages if not specified
        if not src_lang:
            src_lang = self.provider.config.fallback_src_lang if self.provider.config.fallback_src_lang else "ja"
        if not dst_lang:
            dst_lang = self.provider.config.fallback_dst_lang if self.provider.config.fallback_dst_lang else "en"

        # Validate language codes
        try:
            LanguageMapper.validate_language_code(src_lang, "from")
            LanguageMapper.validate_language_code(dst_lang, "to")
        except ValueError as e:
            # Return error status for invalid language codes
            print(f"Language validation error: {e}", file=sys.stderr)
            return "", 400, {"Content-Type": "text/plain; charset=utf-8"}

        try:
            # Translate
            translation = self.provider.translate(text, src_lang, dst_lang)
            # Return plain text response (CustomTranslate specification)
            return translation, 200, {"Content-Type": "text/plain; charset=utf-8"}

        except Exception as e:
            # Log error to stderr
            print(f"Translation error: {e}", file=sys.stderr)
            traceback.print_exc()
            # Return error status without error message to prevent translation from being cached
            return "", 500, {"Content-Type": "text/plain; charset=utf-8"}

    def start(self, host: str, port: int):
        """Start server"""
        print(f"Translation server starting: http://{host}:{port}")
        print(f"Provider: {self.provider.config.provider}")
        print(f"Model: {self.provider.config.model}")
        if self.provider.config.summary:
            print(f"App summary: {self.provider.config.summary}")
        print("Press Ctrl+C to exit")
        self.app.run(host=host, port=port)
