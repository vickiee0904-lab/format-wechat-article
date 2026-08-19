#!/usr/bin/env python3
"""Wrap a WeChat article fragment in a standalone mobile preview page."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Pasteable article fragment")
    parser.add_argument("output", type=Path, help="Standalone preview HTML")
    parser.add_argument("--title", default="公众号文章预览", help="Browser page title")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fragment = args.input.read_text(encoding="utf-8")
    page_title = html.escape(args.title, quote=True)
    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #eef1f6; color: #1f2430; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .toolbar {{ position: sticky; top: 0; z-index: 10; display: flex; justify-content: center; gap: 10px; padding: 12px; background: rgba(238,241,246,.94); border-bottom: 1px solid #dfe3ea; backdrop-filter: blur(12px); }}
    .toolbar button {{ border: 0; border-radius: 999px; padding: 9px 16px; color: #fff; background: #4967f2; font-size: 14px; cursor: pointer; }}
    .status {{ align-self: center; color: #687083; font-size: 13px; }}
    .device {{ width: min(100%, 423px); margin: 24px auto 48px; padding: 24px; background: #fff; box-shadow: 0 18px 60px rgba(40,52,90,.12); }}
    @media (max-width: 480px) {{ .device {{ width: 100%; margin: 0; padding: 0; box-shadow: none; }} }}
  </style>
</head>
<body>
  <div class="toolbar">
    <button id="copy" type="button">复制公众号富文本</button>
    <span class="status" id="status">复制范围仅包含文章</span>
  </div>
  <main class="device"><article id="wechat-article">{fragment}</article></main>
  <script>
    const button = document.getElementById('copy');
    const status = document.getElementById('status');
    const article = document.getElementById('wechat-article');
    button.addEventListener('click', async () => {{
      const htmlValue = article.innerHTML;
      const textValue = article.innerText;
      try {{
        if (navigator.clipboard && window.ClipboardItem) {{
          const item = new ClipboardItem({{
            'text/html': new Blob([htmlValue], {{ type: 'text/html' }}),
            'text/plain': new Blob([textValue], {{ type: 'text/plain' }})
          }});
          await navigator.clipboard.write([item]);
        }} else {{
          const range = document.createRange();
          range.selectNodeContents(article);
          const selection = window.getSelection();
          selection.removeAllRanges();
          selection.addRange(range);
          document.execCommand('copy');
          selection.removeAllRanges();
        }}
        status.textContent = '已复制，可粘贴到公众号编辑器';
      }} catch (error) {{
        status.textContent = '复制失败，请手动选择文章内容';
      }}
    }});
  </script>
</body>
</html>
"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    print(f"Created preview: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

