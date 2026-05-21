# 📰 AI 每日新聞日報 Bot

每日自動抓取財經、科技、全球時事 RSS，交由 Gemini 3.5 Flash 整理成廣東話摘要，並推送到 Telegram 頻道。

---

## ✨ 功能

- 從 4 個 RSS 來源抓取最新文章（每源最多 20 條）
- 自動去除重複文章
- 呼叫 Gemini 3.5 Flash + Google Search 生成每日摘要
  - 財經 Top 5
  - 科技 Top 3
  - 全球時事 Top 2
- 全文以**香港廣東話書面語 + 繁體中文**撰寫
- 自動分段發送至 Telegram（每段上限 4000 字）
- 每日 HKT 09:00 由 GitHub Actions 自動執行

---

## 📡 RSS 來源

| 來源 | URL |
|------|-----|
| Yahoo Finance | https://finance.yahoo.com/rss/topstories |
| The Verge | https://www.theverge.com/rss/index.xml |
| TechCrunch | https://techcrunch.com/feed/ |
| TLDR | https://tldr.tech/rss |
| TradingView | 由 Gemini Google Search 補充 |

---

## 🗂️ 檔案結構

```
news-bot/
├── main.py                          # 主程式
├── requirements.txt                 # Python 依賴
├── .env                             # 本地環境變數（不 commit）
├── .gitignore
└── .github/
    └── workflows/
        └── daily_news.yml           # GitHub Actions 排程
```

---

## 🚀 本地執行

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

複製 `.env` 並填入你的 API Key：

```env
GEMINI_API_KEY=your_key_here
TG_BOT_TOKEN=your_token_here
TG_CHAT_ID=your_chat_id_here
```

### 3. 執行

```bash
python main.py
```

---

## ⚙️ GitHub Actions 自動排程

### 設定 Secrets

前往 repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**，新增以下三個：

| Secret 名稱 | 取得方式 |
|---|---|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com) → Get API key |
| `TG_BOT_TOKEN` | Telegram 搜尋 `@BotFather` → `/newbot` |
| `TG_CHAT_ID` | 頻道用 `@username`，群組用數字 ID（可用 `@userinfobot` 查詢）|

### 手動觸發

**Actions** → **Daily News Digest** → **Run workflow**

### 排程時間

每日 UTC 01:00（= HKT 09:00）自動執行。

> ⚠️ **注意**：GitHub 對閒置 repo 有限制，若 60 日內無任何 commit，scheduled workflow 會被暫停。收到通知後到 Actions 頁面點 **Enable workflow** 重新啟用即可。

---

## 🛠️ 技術棧

- **Python 3.11**
- [google-genai](https://pypi.org/project/google-genai/) — Gemini API SDK
- [feedparser](https://pypi.org/project/feedparser/) — RSS 解析
- [requests](https://pypi.org/project/requests/) — HTTP 請求
- [python-dotenv](https://pypi.org/project/python-dotenv/) — 環境變數管理
- **GitHub Actions** — 自動排程
