# 🏦 Financer_PRO: AI-Powered Financial Intelligence
**Powered by Groq & Python Automation**

Stop wasting time on manual expense tracking. **Financer_PRO** is an automated pipeline that transforms messy PDF receipts and bank statements into a structured, audit-ready database using LLM intelligence.

## 🛠️ Key Features
* **AI OCR Extraction**: Uses Llama 3.3 (via Groq) to understand context, not just text.
* **Real-Time Monitoring**: Automatically detects new files in your "vault" and processes them instantly.
* **Smart Categorization**: Intelligent vendor detection and automatic spending classification.
* **Currency Intelligence**: Live FX rate integration for multi-currency financial management.

## 📊 Technical Architecture
| Feature | Implementation |
| :--- | :--- |
| **Brain** | Groq AI (Llama 3.3 70B Versatile) |
| **Pipeline** | Python Watchdog & Multithreading |
| **Data Engine** | Pandas & SQLite (v2 Coming Soon) |
| **Cloud Ready** | Designed for AWS Lambda deployment |

## 💡 Why Financer_PRO is different:
* 🚀 **Context Aware**: It doesn't just see "15.00", it knows it was "Coffee at Starbucks" and labels it as *Food & Drink*.
* 🧠 **Zero Manual Input**: Just drop a PDF into a folder. The script handles the rest.
* 🧹 **Auto-Cleaning**: Normalizes Polish characters, fixes date formats, and handles currency symbols.
* 📁 **Scalable Structure**: Built with a "Clean Code" approach, ready for transition to SQL and Cloud.

## 🚀 Roadmap
- [x] **v1 (Foundation)**: PDF monitoring & Groq AI extraction.
- [ ] **v2 (February 2026)**: Migration to SQL (SQLite) & Data Integrity Layer.
- [ ] **v3**: AWS S3 & Lambda integration for 24/7 automation.

## 📁 How to Use
1.  Place your API Key in a `.env` file (never share it!).
2.  Drop your PDF invoices into the `/vault` folder.
3.  Run the engine: `Financer_PRO.py`
4.  Check `/outputs` for your structured data.

---
*Building the future of personal data engineering. Part of the 2026-2027 Development Journey.*
