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
    # 基本パターン: "FPS: 359", "FPS:359", "FPS 359", "359 FPS", "359FPS"
    # 小数点対応: "FPS: 59.9", "59.9 FPS", "59.9FPS"
    # フレームレート表現: "framerate: 60", "60 fps", "Frame Rate: 60"
    # パターン1: FPS/framerate + 数字
    # パターン2: 数字 + FPS/framerate
    if re.search(
        r"(?:FPS|F\.P\.S\.?|framerate|frame\s*rate)\s*[:：]?\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?\s*(?:FPS|F\.P\.S\.?|framerate|frame\s*rate)",
        text,
        re.IGNORECASE,
    ):
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
