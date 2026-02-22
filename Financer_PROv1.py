import os
import json
import logging
import csv
import time
import requests
import sys
import pdfplumber
from pathlib import Path
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

if not API_KEY:
    print("CRITICAL ERROR: GROQ_API_KEY not found in .env file")
    sys.exit(1)

SESSION_ID = datetime.now().strftime('%Y%m%d_%H%M%S')

def normalize_text(text):
    if not text: return ""
    mapping = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    for char, replacement in mapping.items():
        text = text.replace(char, replacement)
    return text

def extract_pdf_text(file_path):
    try:
        full_text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content: full_text += content + "\n"
        return full_text.strip()
    except Exception as e:
        logging.error(f"Extraction Error for {file_path.name}: {e}")
        return None

def process_financial_audit(file_path, client, output_dir, base_currency, rates):
    logging.info(f"Processing: {file_path.name}")
    content = extract_pdf_text(file_path)
    if not content: return

    process_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    today = datetime.now().strftime('%Y-%m-%d')
    
    system_prompt = (
        f"Role: Senior Financial Auditor. Extract ALL transactions. "
        f"Return a JSON object with a key 'transactions' containing a list of objects. "
        f"MANDATORY: Use 3-letter ISO currency codes (USD, EUR, PLN). "
        f"If date missing, use {today}. Logic: Expenses=NEGATIVE, Income=POSITIVE. "
        f"Fields: vendor_name, date, amount, currency, category, description."
    )

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": content[:12000]}],
            model=MODEL_NAME,
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        response_data = json.loads(completion.choices[0].message.content)
        
        json_filename = f"{process_ts}_{file_path.stem}.json"
        json_path = output_dir / json_filename
        with open(json_path, 'w', encoding='utf-8') as jf:
            json.dump(response_data, jf, indent=4, ensure_ascii=False)
        logging.info(f"JSON saved: {json_filename}")

        transactions = response_data.get('transactions', [])
        if not isinstance(transactions, list): transactions = [response_data]

        db_filename = f"audit_master_{SESSION_ID}.csv"
        db_path = output_dir / db_filename
        
        for entry in transactions:
            try:
                raw_amount = float(str(entry.get('amount', 0)).replace(',', ''))
            except:
                raw_amount = 0.0

            doc_currency = str(entry.get('currency', base_currency)).upper().strip()
            rate_to_base = 1.0
            if rates and doc_currency != base_currency:
                rate_to_base = rates.get(doc_currency, 1.0)
            
            converted_total = round(raw_amount / rate_to_base, 2)
            vendor = entry.get('vendor_name') or entry.get('vendor') or "Unknown"

            processed_entry = {
                'vendor_name': normalize_text(str(vendor)),
                'date': entry.get('date', today),
                'amount': raw_amount,
                'currency': doc_currency,
                'category': normalize_text(str(entry.get('category', 'Other'))),
                'description': normalize_text(str(entry.get('description', ''))),
                f'total_{base_currency.lower()}': converted_total,
                'fx_rate_applied': rate_to_base,
                'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'file_source': normalize_text(file_path.name)
            }

            file_exists = db_path.exists()
            with open(db_path, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=processed_entry.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(processed_entry)

            logging.info(f"RECORDED: {processed_entry['vendor_name']} | {converted_total} {base_currency}")
        
    except Exception as e:
        logging.error(f"Audit Failure for {file_path.name}: {e}")

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            time.sleep(3)
            process_financial_audit(Path(event.src_path), api_client, output_path, base_curr, rates)

if __name__ == "__main__":
    root = Path.cwd()
    vault_path, output_path = root / "vault", root / "outputs"
    logs_path = output_path / "logs"
    
    for d in [vault_path, output_path, logs_path]: d.mkdir(parents=True, exist_ok=True)

    log_filename = logs_path / f"log_{SESSION_ID}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("--- SYSTEM INITIALIZED ---")
    base_curr = input("SELECT BASE CURRENCY (PLN, USD, EUR): ").upper().strip()
    if not base_curr: base_curr = "PLN"
    
    try:
        rates_response = requests.get(f"https://open.er-api.com/v6/latest/{base_curr}").json()
        rates = rates_response.get("rates")
        logging.info(f"Live rates loaded for base: {base_curr}")
    except Exception as e:
        rates = None
        logging.error(f"Could not fetch FX rates: {e}")

    api_client = Groq(api_key=API_KEY)

    for pdf_file in vault_path.glob("*.pdf"):
        process_financial_audit(pdf_file, api_client, output_path, base_curr, rates)

    observer = Observer()
    observer.schedule(PDFHandler(), str(vault_path), recursive=False)
    observer.start()
    
    logging.info(f"MONITORING ACTIVE: {vault_path}")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("SHUTDOWN SEQUENCE COMPLETED")
    observer.join()
