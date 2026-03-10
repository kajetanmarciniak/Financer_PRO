# 🏦 AI Financial Auditor v3: Edge-to-Cloud Data Pipeline
**Automated Intelligence for Modern Accounting | Powered by Groq, AWS S3 & SQL**

Stop wasting time on manual expense tracking. **AI Financial Auditor** is a professional-grade automated pipeline that transforms messy PDF receipts and bank statements into a structured, audit-ready **relational database** with automated **cloud backups**.

---

## 🛠️ Key Features
* **🧠 Universal AI Engine**: Compatible with any OpenAI-standard API (Groq, OpenAI, Local LLMs). Powered by **Llama 3.3 70B** for deep financial reasoning.
* **☁️ Cloud Sync (S3)**: Automated real-time synchronization with **AWS S3**. Every local database update is instantly backed up to the cloud.
* **🛡️ Security Shield**: Built-in protection against **Prompt Injection** and **SQL Injection**. Filters forbidden phrases and uses parameterized queries.
* **🗄️ SQL Persistence**: Every transaction is indexed in a permanent **SQLite3 database** with full audit trails (`file_source`, `processed_at`).
* **💱 Live FX Engine**: Integrated with **Open Exchange Rates API**. Automatically converts foreign currencies (AED, EUR, USD, etc.) into your base currency using live market data.
* **💱 Smart Currency Normalization**: Advanced mapping engine that intelligently handles dozens of currency formats. It recognizes symbols ($, €, zł), full names (Dirhams, Euro, Zloty), and shorthand (Dhs, DH, Zł) and maps them to standard ISO 4217 codes for precise FX conversion.**
* **⚡ Real-Time Monitoring**: Event-driven architecture via `Watchdog`. Drop a PDF into `/vault`, and the system handles the rest.

---

## 📊 Technical Architecture
| Feature | Implementation |
| :--- | :--- |
| **Brain** | Groq AI (Llama 3.3 70B Versatile) / OpenAI API |
| **Database** | **SQLite3 (Relational Storage)** |
| **Cloud** | **AWS S3 (boto3) Synchronization** |
| **Monitoring** | Python Watchdog (Event-driven) |
| **FX Rates** | Open Exchange Rates API (Requests) |
| **Reporting** | SQL Queries & UTF-8-BOM CSV Exports |

---

## 💡 Why this pipeline is different:
* 🚀 **Context-Aware**: It doesn't just see "15.00", it knows it was "Netflix Subscription" and labels it as *Entertainment*.
* 🔐 **Security-First**: Sanitizes vendor names and filters incoming text for malicious instructions (**Forbidden Words** filter).
* 🧹 **Audit-Ready**: Ensures data integrity by tracking the exact source file for every database entry.

---

## 🚀 Roadmap
* ✅ **v1 (Foundation)**: PDF monitoring & Groq AI extraction.
* ✅ **v2 (Database)**: SQL integration, Live FX rates, and normalization.
* ✅ **v3 (Cloud)**: AWS S3 Integration & Security Hardening.
* ✅ **v3.1 (Cloud & Stability)**: **AWS S3 Integration, Smart Currency Normalization & SQL Schema Hardening (Current Version)**.
* 📅 **v4 (Analysis)**: Streamlit Dashboard for visual expense analytics.

---

## 📁 Setup & Usage

### 1. Clone & Install Dependencies
```bash
pip install openai pdfplumber boto3 python-dotenv watchdog requests

2. Environment Configuration
Create a .env file in the root folder and fill it with your credentials:

API_KEY=your_ai_key
BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile

AWS_ACCESS_KEY_ID=your_aws_id
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=eu-central-1
AWS_S3_BUCKET=your_bucket_name

3. Run the Auditor
    Start the script: Financer-PROv3.py
    Select your base currency (e.g., PLN).
    Drop PDF files into the /vault folder.
    View results in /outputs or your AWS S3 Bucket.

Building the future of personal data engineering. Part of the 2026-2027 Development Journey.
