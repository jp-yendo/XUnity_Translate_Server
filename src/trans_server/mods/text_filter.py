"""Text filtering utilities for translation optimization."""

import re


def is_dynamic_value(text: str) -> bool:
    """動的な値(定期的に変化する値)かどうかを判定

    Args:
        text: チェック対象のテキスト

    Returns:
        True: 動的な値(翻訳をキャッシュすべきでない), False: それ以外
    """
    # FPS表示パターン
    # 例: "FPS: 60", "FPS:60", "60 FPS", "60FPS"など
    if re.search(r"FPS\s*[:：]?\s*\d+|^\d+\s*FPS$", text, re.IGNORECASE):
        return True

    return False


def should_skip_translation(text: str) -> bool:
    """翻訳をスキップすべきテキストかどうかを判定
    (数字・空白・記号のみのテキストを検出)

    Args:
        text: チェック対象のテキスト

    Returns:
        True: 翻訳をスキップすべき(数字・空白・記号のみ), False: 翻訳が必要
    """
    # 空文字列またはスペースのみ
    if not text or not text.strip():
        return True

    # 数字・空白・記号のみかチェック
    # \W は非単語文字(記号など)、\d は数字、\s は空白、_ はアンダースコア
    if re.fullmatch(r"[\W\d\s_]+", text, re.UNICODE):
        return True

    return False
