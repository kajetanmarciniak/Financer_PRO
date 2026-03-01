# 🏦 AI Financial Auditor v2: PDF-to-SQL Data Pipeline
**Automated Intelligence for Modern Accounting | Powered by Groq, Python & SQL**

Stop wasting time on manual expense tracking. **AI Financial Auditor** is an automated pipeline that transforms messy PDF receipts and bank statements into a structured, audit-ready **SQLite database** using Llama 3.3 intelligence.

## 🛠️ Key Features
* **AI-Powered Extraction**: Uses **Llama 3.3 70B** (via Groq) to understand financial context. It distinguishes between a refund and a charge automatically.
* **SQL Persistence (v2)**: Moves beyond flat files. Every transaction is indexed in a permanent **SQLite3 database** for long-term auditing and history.
* **Live FX Engine**: Integrated with **Open Exchange Rates API**. Automatically converts foreign currencies (AED, EUR, USD) into your base currency (PLN/USD/EUR) using live market data.
* **Real-Time Monitoring**: Powered by `Watchdog`. Drop a PDF into the `/vault` folder, and the system processes it in seconds without a single click.
* **Data Normalization**: Custom engine to clean special characters and standardize vendor names for professional reporting.

## 📊 Technical Architecture
| Feature | Implementation |
| :--- | :--- |
| **Brain** | Groq AI (Llama 3.3 70B Versatile) |
| **Database** | **SQLite3 (Relational Storage)** |
| **Monitoring** | Python Watchdog (Event-driven) |
| **FX Rates** | Open Exchange Rates API (Requests) |
| **Reporting** | SQL Queries & UTF-8-BOM CSV Exports |



## 💡 Why this pipeline is different:
* 🚀 **Context-Aware**: It doesn't just see "15.00", it knows it was "Netflix Subscription" and labels it as *Entertainment*.
* 🧠 **Zero Manual Input**: Fully automated "Vault" system — no buttons to click.
* 🧹 **Audit-Ready**: Tracks `file_source` and `processed_at` timestamp for every entry, ensuring data integrity.

## 🚀 Roadmap
* ✅ **v1 (Foundation)**: PDF monitoring & Groq AI extraction. (**February Version**)
* ✅ **v2 (Database)**: Full SQL integration, Live FX rates, and data normalization. (**Current Version**)
* 📅 **v3 (Cloud)**: AWS S3 & Lambda integration for 24/7 cloud automation (**Planned for March/April 2026**).

## 📁 Setup & Usage
1. **Clone & Install Dependencies**:
   ```bash
   pip install groq pdfplumber python-dotenv watchdog requests
   
   Environment: Create a .env file in the root folder and add your key:
   GROQ_API_KEY=your_api_key_here

   Process Data: Select your base currency and drop PDF files into the /vault folder.
    View Results: Check /outputs for CSV reports or use DB Browser for SQLite to open financial_audit.db.

Building the future of personal data engineering. Part of the 2026-2027 Development Journey.
