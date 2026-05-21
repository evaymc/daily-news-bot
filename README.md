# 📰 AI Daily News Bot

A simple automation tool that:

👉 Collects the latest news 👉 Summarizes it using AI 👉 Sends it directly to Telegram every day

It runs fully automatically — no need to open your computer daily.

---

## ✨ What it does

- 📡 Fetches news from 4 RSS sources
- 🧠 Uses Google Gemini (Free API) to summarize news
- 🗣️ Outputs summaries in Cantonese (Hong Kong) / Traditional Chinese
- 📊 Organizes news into:
  - Finance Top 5
  - Tech Top 3
  - Global News Top 2
- 🚫 Removes duplicate articles automatically
- 📩 Sends results to Telegram channel or group
- ⏰ Runs automatically every day using GitHub Actions

---

## 💡 Why use this?

Instead of:

❌ Checking multiple news sites
❌ Spending time filtering important news
❌ Switching between apps

You only need:

✅ Open Telegram
✅ Read one clean AI-generated summary

---

## ⚙️ Tech Stack

- Python
- RSS feeds (news sources)
- Gemini API (free AI summarization)
- GitHub Actions (automation scheduler)
- Telegram Bot (message delivery)

---

## 📡 News Sources

| Source | URL |
|--------|-----|
| Yahoo Finance | https://finance.yahoo.com/rss/topstories |
| The Verge | https://www.theverge.com/rss/index.xml |
| TechCrunch | https://techcrunch.com/feed/ |
| TLDR Newsletter | https://tldr.tech/rss |
| TradingView | Supplemented via Gemini Google Search |

---

## 🚀 Quick Start

### 1. Clone the project

```bash
git clone https://github.com/your-username/daily-news-bot.git
cd daily-news-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_free_gemini_api_key
TG_BOT_TOKEN=your_telegram_bot_token
TG_CHAT_ID=your_chat_id
```

### 4. Run locally

```bash
python main.py
```

---

## 🔑 How to get API keys

### 🤖 Gemini API (Free)

1. Go to https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click **Create API key**
4. Free tier is enough for daily news summarization

> Free tier limits: 5 RPM / 20 RPD / 250,000 tokens per day
> No credit card required.

### 📩 Telegram Bot

1. Search `@BotFather` on Telegram
2. Run `/newbot`
3. Follow the instructions to get your bot token
4. Create a channel or group and add your bot
5. Get your Chat ID via `@userinfobot`

---

## ⏰ Automation (GitHub Actions)

Runs automatically every day at **09:00 HKT** (UTC 01:00).

### Setup Secrets (one-time)

Go to: **GitHub repo → Settings → Secrets and variables → Actions → New repository secret**

Add the following:

| Secret | Description |
|--------|-------------|
| `GEMINI_API_KEY` | Your Gemini API key |
| `TG_BOT_TOKEN` | Your Telegram bot token |
| `TG_CHAT_ID` | Your Telegram channel or group ID |

### Manual trigger

**Actions → Daily News Digest → Run workflow**

> ⚠️ **Note:** GitHub pauses scheduled workflows after 60 days of repo inactivity. If paused, go to Actions and click **Enable workflow**.

---

## 💰 Cost

This project runs completely free:

| Item | Cost |
|------|------|
| Gemini API (free tier) | $0 |
| GitHub Actions | $0 |
| Telegram Bot | $0 |
| **Total** | **$0 / month** |

---

## 🧠 System Flow

```
RSS News → Deduplication → Gemini AI → Summarization → Telegram
```

---

## 📁 Project Structure

```
daily-news-bot/
├── main.py                    # Main script
├── requirements.txt           # Dependencies
├── .gitignore
└── .github/
    └── workflows/
        └── daily_news.yml     # GitHub Actions scheduler
```

---

## 🌱 Who is this for?

- Beginners learning automation projects
- People learning GitHub Actions
- Anyone building Telegram bots
- Portfolio / CV projects for software roles
