# XUnity_Translate_Server

AI Translation Server for XUnity.AutoTranslator's CustomTranslate

[日本語版 README はこちら](README-ja.md)

## Features

- Support for AI providers: OpenAI, Anthropic, Ollama, and more
- HTTP API endpoints compliant with CustomTranslate specification
- High-precision translation preserving line breaks and whitespace
- Concise translations with character count awareness

## Usage

No installation required. Run directly with `uvx`:

### OpenAI Provider

```bash
uvx XUnity_Translate_Server --provider openai --model gpt-4 --api-key YOUR_KEY --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### Anthropic Provider

```bash
uvx XUnity_Translate_Server --provider anthropic --model claude-3-5-sonnet-20241022 --api-key YOUR_KEY --summary "RPG game" --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### Google Gemini Provider

```bash
uvx XUnity_Translate_Server --provider gemini --model gemini-2.0-flash-exp --api-key YOUR_KEY --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### OpenAI-Compatible Provider

For OpenAI-compatible services (Azure OpenAI, LocalAI, etc.):

```bash
uvx XUnity_Translate_Server --provider openai-compatible --model gpt-4 --api-key YOUR_KEY --api-base https://your-api-endpoint.com/v1 --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### Anthropic-Compatible Provider

For Anthropic-compatible services:

```bash
uvx XUnity_Translate_Server --provider anthropic-compatible --model your-model-name --api-key YOUR_KEY --api-base https://your-api-endpoint.com --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### Ollama Provider

```bash
uvx XUnity_Translate_Server --provider ollama --model llama2 --api-base http://localhost:11434 --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### List Available Models

```bash
uvx XUnity_Translate_Server --provider ollama --list-models
```

## Command Line Parameters

### Common Parameters

- `--provider`: Provider name (required)
  - `openai`, `openai-compatible`, `anthropic`, `anthropic-compatible`, `ollama`, `gemini`
- `--model`: Model name to use (required, not needed with `--list-models`)
- `--summary`: Application summary (optional, improves translation accuracy)
- `--fallback-from`: Fallback source language code (optional, e.g., ja)
- `--fallback-to`: Fallback target language code (optional, e.g., en)
- `--list-models`: List available models and exit
- `--host`: Server bind address (required for server startup)
- `--port`: Server port number (required for server startup)

### OpenAI-Specific Parameters

- `--api-key`: API key (required)
- `--organization`: Organization ID (optional)

### OpenAI-Compatible-Specific Parameters

- `--api-key`: API key (required)
- `--api-base`: Base URL (required for OpenAI-compatible services)
- `--organization`: Organization ID (optional)

### Anthropic-Specific Parameters

- `--api-key`: API key (required)

### Anthropic-Compatible-Specific Parameters

- `--api-key`: API key (required)
- `--api-base`: Base URL (required for Anthropic-compatible services)

### Gemini-Specific Parameters

- `--api-key`: Google AI Studio API key (required)

### Ollama-Specific Parameters

- `--api-base`: Ollama server URL (default: http://localhost:11434)

## API Specification

### GET /translate

Translation endpoint compliant with CustomTranslate specification

**Request:**

```http
GET /translate?from=ja&to=en&text=こんにちは
```

**Parameters:**

- `from`: Source language code (e.g., ja, en)
- `to`: Target language code (e.g., en, ja)
- `text`: Text to translate

**Response:**

```text
Hello
```

Returns plain text translation.

### GET /health

Health check endpoint

**Response:**

```text
ok
```

## XUnity.AutoTranslator Configuration

Add the following to `AutoTranslatorConfig.ini`:

```ini
[Service]
Endpoint=CustomTranslate

[CustomTranslate]
Url=http://127.0.0.1:4660/translate
```

## License

MIT License
