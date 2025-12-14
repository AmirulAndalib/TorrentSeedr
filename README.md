# 🤖 Seedrcc Bot

Telegram bot to manage your Seedr.cc account directly within Telegram.

## 🌟 Features

- Supports **most Seedr.cc features** directly within Telegram.
- **Multiple account support** for separate accounts.
- **Sensitive data encrypted** at rest for enhanced security.

## 🚀 Quick Start (Manual setup)

### 1. Setup

Clone the repository:

```bash
git clone https://github.com/hemantapkh/SeedrccBot.git
cd SeedrccBot
```

### 2. Install **uv**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh # Mac/Linux
```

### OR

Check the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation) for more options.

### 3. Configuration

Copy the sample config and fill in your credentials:

```bash
cp .env.example .env
# Edit .env and fill in your credentials
```

### 4. Install Dependencies & Run

#### SQLite (Default)

```bash
uv run app
```

### OR

#### PostgreSQL

```bash
uv sync --group postgres
uv run app
```

---

## 🐳 Docker Deployment

### 1. Build the Image

#### SQLite

```bash
docker build -t seedrccbot .
```

### OR

#### PostgreSQL

```bash
docker build --build-arg DATABASE_TYPE=postgres -t seedrccbot .
```

### 2. Run the Container

Mount a volume to persist the database:

```bash
docker run --env-file .env -v $(pwd)/data:/app/data seedrccbot
```

---

## 🤝 Contributing

Any contributions you make are **greatly appreciated**. Thank you to every [contributors](https://github.com/hemantapkh/seedrccbot/graphs/contributors) who have contributed in this project!

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

Made with ❤️ by [Hemanta Pokharel](https://github.com/hemantapkh) using [Telethon](https://github.com/LonamiWebs/Telethon) and [seedrcc](https://github.com/hemantapkh/seedrcc)
