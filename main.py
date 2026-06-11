import os
import time
import feedparser
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
TG_CHAT_ID = os.environ["TG_CHAT_ID"]

RSS_FEEDS = {
    "Yahoo Finance": "https://finance.yahoo.com/rss/topstories",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    "TLDR": "https://tldr.tech/rss",
}

MAX_ITEMS_PER_FEED = 20
GEMINI_MAX_RETRIES = 3
GEMINI_RETRYABLE_STATUS = (429, 500, 502, 503, 504)
GEMINI_RETRY_SLEEP_SECONDS = 5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_rss() -> str:
    seen_titles: set[str] = set()
    lines: list[str] = []

    for source, url in RSS_FEEDS.items():
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            feed = feedparser.parse(r.content)
        except Exception as e:
            print(f"[WARNING] Failed to fetch {source}: {e}")
            continue
        count = 0
        for entry in feed.entries:
            if count >= MAX_ITEMS_PER_FEED:
                break
            title_key = entry.get("title", "").lower().strip()
            if not title_key or title_key in seen_titles:
                continue
            seen_titles.add(title_key)
            published = entry.get("published", "N/A")
            link = entry.get("link", "")
            lines.append(f"[{source}] {entry.get('title', '')} | {published} | {link}")
            count += 1

    return "\n".join(lines)


def build_prompt(rss_content: str, date_str: str) -> str:
    return f"""你係一個新聞助手。以下係今日從各媒體 RSS 抓取嘅文章列表：

{rss_content}

TradingView 冇 RSS，請用 Google Search 搜尋「TradingView news site:tradingview.com」補充最新財經新聞。

將所有文章語意聚類，依「被多個來源同時提及」嘅次數排序，選出：
- 財經類 Top 5（股市、經濟、企業、貨幣等）
- 科技類 Top 3（AI、科技產品、互聯網、半導體等）
- 全球時事 Top 2（地緣政治、外交、戰爭、國際峰會等）

規則：
- 不用 keyword 過濾，直接由你判斷分類
- 三個類別之間新聞不能重複
- 每條新聞必須來自上述媒體之一

每個類別撰寫約 150 字總結，語言要求：
- 全部使用香港廣東話書面語
- 繁體中文
- 專業術語括號保留英文，例如「大型語言模型（LLM）」
- 段與段之間空一行

輸出格式：

━━━━━━━━━━
 AI 日報 | {date_str}
━━━━━━━━━━

【今日財經重點】

[約150字廣東話總結]

◠◡◠◡◠◡◠◡◠◡◠◡
【財經 Top 5】

① 來源 | 英文標題
　繁：中文標題
　時間：發布時間 ET | 香港時間 HKT
　🔗 URL
　[3-4句廣東話內文]

② ③ ④ ⑤ 同上格式

◠◡◠◡◠◡◠◡◠◡◠◡
【今日科技重點】

[約150字廣東話總結]

◠◡◠◡◠◡◠◡◠◡◠◡
【科技 Top 3】

① ② ③ 同財經格式

◠◡◠◡◠◡◠◡◠◡◠◡
【今日全球重點】

[約150字廣東話總結]

◠◡◠◡◠◡◠◡◠◡◠◡
【全球 Top 2】

① ② 同財經格式

◠◡◠◡◠◡◠◡◠◡◠◡
📡 每日自動更新"""


def call_gemini(prompt: str) -> str:
    client = genai.Client()
    for attempt in range(1, GEMINI_MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                ),
            )
            return response.text
        except Exception as e:
            status = getattr(e, "status_code", None)
            error_text = str(e).upper()
            is_retryable = status in GEMINI_RETRYABLE_STATUS or (
                status is None and "503" in error_text and "UNAVAILABLE" in error_text
            )
            if not is_retryable or attempt == GEMINI_MAX_RETRIES:
                raise
            wait_seconds = GEMINI_RETRY_SLEEP_SECONDS * (2 ** (attempt - 1))
            print(
                f"[WARNING] Gemini call failed with retryable error: {e}. "
                f"Retrying in {wait_seconds}s ({attempt}/{GEMINI_MAX_RETRIES})..."
            )
            time.sleep(wait_seconds)


def send_telegram(text: str) -> None:
    api_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    chunk_size = 4000

    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    for chunk in chunks:
        payload = {
            "chat_id": TG_CHAT_ID,
            "text": chunk,
            "parse_mode": "HTML",
        }
        resp = requests.post(api_url, json=payload, timeout=30)
        resp.raise_for_status()


def main() -> None:
    hkt = timezone(timedelta(hours=8))
    date_str = datetime.now(hkt).strftime("%Y-%m-%d")

    print(f"[{date_str}] Fetching RSS feeds...")
    rss_content = fetch_rss()
    print(f"Fetched {rss_content.count(chr(10)) + 1} articles")

    print("Calling Gemini-2.5-flash...")
    prompt = build_prompt(rss_content, date_str)
    digest = call_gemini(prompt)

    print("Sending to Telegram...")
    send_telegram(digest)
    print("Done.")


if __name__ == "__main__":
    main()
