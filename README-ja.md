# XUnity_Translate_Server

XUnity.AutoTranslatorのCustomTranslate用AI翻訳サーバー

[English README is here](README.md)

## 機能

- OpenAI、Anthropic、Ollama等のAIプロバイダをサポート
- CustomTranslate仕様に準拠したHTTP APIエンドポイント
- 改行・空白を保持した高精度な翻訳
- 文字数を意識した簡潔な翻訳

## 使用方法

インストール不要で、`uvx`コマンドで直接実行できます：

### OpenAIプロバイダ

```bash
uvx XUnity_Translate_Server --provider openai --model gpt-4 --api-key YOUR_KEY --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### Anthropicプロバイダ

```bash
uvx XUnity_Translate_Server --provider anthropic --model claude-3-5-sonnet-20241022 --api-key YOUR_KEY --summary "RPG game" --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### Google Geminiプロバイダ

```bash
uvx XUnity_Translate_Server --provider gemini --model gemini-2.0-flash-exp --api-key YOUR_KEY --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### OpenAI互換プロバイダ

OpenAI互換サービス（Azure OpenAI、LocalAI等）を使用する場合：

```bash
uvx XUnity_Translate_Server --provider openai-compatible --model gpt-4 --api-key YOUR_KEY --api-base https://your-api-endpoint.com/v1 --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### Anthropic互換プロバイダ

Anthropic互換サービスを使用する場合：

```bash
uvx XUnity_Translate_Server --provider anthropic-compatible --model your-model-name --api-key YOUR_KEY --api-base https://your-api-endpoint.com --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### Ollamaプロバイダ

```bash
uvx XUnity_Translate_Server --provider ollama --model llama2 --api-base http://localhost:11434 --fallback-from ja --fallback-to en --host 127.0.0.1 --port 4660
```

### モデル一覧取得

```bash
uvx XUnity_Translate_Server --provider ollama --list-models
```

## 起動パラメータ

### 共通パラメータ

- `--provider`: プロバイダ（必須）
  - `openai`, `openai-compatible`, `anthropic`, `anthropic-compatible`, `ollama`, `gemini`
- `--model`: 使用するモデル名（必須、`--list-models`時は不要）
- `--summary`: アプリ概要（任意、翻訳精度向上のため）
- `--fallback-from`: フォールバック翻訳元言語（任意、例: ja）
- `--fallback-to`: フォールバック翻訳先言語（任意、例: en）
- `--list-models`: モデル一覧を表示して終了
- `--host`: バインドアドレス（サーバー起動時は必須）
- `--port`: ポート番号（サーバー起動時は必須）

### OpenAI固有パラメータ

- `--api-key`: APIキー（必須）
- `--organization`: Organization ID（任意）

### OpenAI互換固有パラメータ

- `--api-key`: APIキー（必須）
- `--api-base`: ベースURL（OpenAI互換サービスでは必須）
- `--organization`: Organization ID（任意）

### Anthropic固有パラメータ

- `--api-key`: APIキー（必須）

### Anthropic互換固有パラメータ

- `--api-key`: APIキー（必須）
- `--api-base`: ベースURL（Anthropic互換サービスでは必須）

### Gemini固有パラメータ

- `--api-key`: Google AI Studio APIキー（必須）

### Ollama固有パラメータ

- `--api-base`: OllamaサーバーURL（デフォルト: http://localhost:11434）

## API仕様

### GET /translate

CustomTranslate仕様に準拠した翻訳エンドポイント

**リクエスト:**

```http
GET /translate?from=ja&to=en&text=こんにちは
```

**パラメータ:**

- `from`: 翻訳元言語コード（例: ja, en）
- `to`: 翻訳先言語コード（例: en, ja）
- `text`: 翻訳するテキスト

**レスポンス:**

```text
Hello
```

プレーンテキスト形式で翻訳結果を返します。

### GET /health

ヘルスチェックエンドポイント

**レスポンス:**

```text
ok
```

## XUnity.AutoTranslatorでの設定

`AutoTranslatorConfig.ini`に以下を追加：

```ini
[Service]
Endpoint=CustomTranslate

[CustomTranslate]
Url=http://127.0.0.1:4660/translate
```

## ライセンス

MIT License
