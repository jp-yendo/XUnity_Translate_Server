"""XUnity.AutoTranslator CustomTranslate translation server."""

import argparse
import sys
from typing import Type
from flask import Flask, request, jsonify
from .providers.base_provider import BaseProvider
from .providers.openai_provider import OpenAIProvider
from .providers.openai_compatible_provider import OpenAICompatibleProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.anthropic_compatible_provider import AnthropicCompatibleProvider
from .providers.ollama_provider import OllamaProvider
from .providers.gemini_provider import GeminiProvider


class TranslationServer:
    """Translation server"""

    def __init__(self, provider: BaseProvider):
        self.provider = provider
        self.app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        """Setup routes"""
        self.app.route("/translate", methods=["POST"])(self.handle_translate)
        self.app.route("/health", methods=["GET"])(self.handle_health)

    def handle_health(self):
        """Health check endpoint"""
        return jsonify({"status": "ok"})

    def handle_translate(self):
        """Translation endpoint (CustomTranslate specification)"""
        try:
            # Parse request
            data = request.get_json()

            # CustomTranslate request format (batch processing)
            # { "contentType": "application/json", "untranslatedTexts": [...], "sourceLanguage": "ja", "destinationLanguage": "en" }
            untranslated_texts = data.get("untranslatedTexts", [])
            src_lang = data.get("sourceLanguage")
            dst_lang = data.get("destinationLanguage")

            if not untranslated_texts:
                return jsonify({"error": "untranslatedTexts is required"}), 400

            # Translate each text individually (1-to-1)
            translations = []
            for text in untranslated_texts:
                translation = self.provider.translate(text, src_lang, dst_lang)
                translations.append(translation)

            # CustomTranslate response format
            # { "translatedTexts": [...] }
            return jsonify({"translatedTexts": translations})

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"Translation error: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc()
            return jsonify({"error": "Internal server error"}), 500

    def start(self, host: str, port: int):
        """Start server"""
        print(f"Translation server starting: http://{host}:{port}")
        print(f"Provider: {self.provider.config.provider}")
        print(f"Model: {self.provider.config.model}")
        if self.provider.config.summary:
            print(f"App summary: {self.provider.config.summary}")
        print("Press Ctrl+C to exit")
        self.app.run(host=host, port=port)


def get_provider_class(provider_name: str) -> Type[BaseProvider]:
    """Get provider class from provider name"""
    provider_map = {
        "openai": OpenAIProvider,
        "openai-compatible": OpenAICompatibleProvider,
        "anthropic": AnthropicProvider,
        "anthropic-compatible": AnthropicCompatibleProvider,
        "ollama": OllamaProvider,
        "gemini": GeminiProvider,
    }

    provider_class = provider_map.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unsupported provider: {provider_name}")

    return provider_class


def list_models_and_exit(provider: BaseProvider):
    """List available models and exit"""
    try:
        print(f"Available models for provider '{provider.config.provider}':")
        models = provider.list_models()
        for model in models:
            print(f"  - {model}")
    except Exception as e:
        print(f"Failed to retrieve model list: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="XUnity.AutoTranslator CustomTranslate translation server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server with OpenAI
  python main.py --provider openai --model gpt-4 --api-key YOUR_KEY --host 127.0.0.1 --port 4660

  # Start server with Anthropic (with app summary)
  python main.py --provider anthropic --model claude-3-5-sonnet-20241022 --api-key YOUR_KEY --summary "RPG game" --host 127.0.0.1 --port 4660

  # Start server with Ollama
  python main.py --provider ollama --model llama2 --api-base http://localhost:11434 --host 127.0.0.1 --port 4660

  # List available models
  python main.py --provider ollama --list-models
        """,
    )

    # Common parameters
    parser.add_argument(
        "--provider",
        required=True,
        choices=["openai", "openai-compatible", "anthropic", "anthropic-compatible", "ollama", "gemini"],
        help="Translation provider",
    )
    parser.add_argument("--model", help="Model name (not required with --list-models)")
    parser.add_argument("--summary", help="Application summary (improves translation accuracy)")
    parser.add_argument("--fallback-from", help="Fallback source language code (e.g., ja)")
    parser.add_argument("--fallback-to", help="Fallback target language code (e.g., en)")
    parser.add_argument("--list-models", action="store_true", help="List available models and exit")
    parser.add_argument("--host", help="Server bind address (required for server startup)")
    parser.add_argument("--port", type=int, help="Server port (required for server startup)")

    # Parse common arguments first (to identify provider)
    args, _ = parser.parse_known_args()

    # Add provider-specific arguments
    provider_class = get_provider_class(args.provider)
    provider_class.add_provider_args(parser)

    # Re-parse all arguments
    args = parser.parse_args()

    # Required checks for non--list-models mode
    if not args.list_models:
        if not args.model:
            parser.error("--model is required")
        if not args.host:
            parser.error("--host is required")
        if not args.port:
            parser.error("--port is required")

    return args


def main():
    """Main entry point"""
    args = parse_arguments()

    try:
        # Create provider instance
        provider_class = get_provider_class(args.provider)
        provider = provider_class.create_from_args(args)

        # If --list-models is specified
        if args.list_models:
            list_models_and_exit(provider)
            return

        # Start server
        server = TranslationServer(provider)
        server.start(args.host, args.port)

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
