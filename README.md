# Serverless Financial Market Pipeline 📈

A serverless Python ETL (Extract, Transform, Load) pipeline deployed via Oracle Cloud Infrastructure (OCI). This architecture automatically ingests live market data, normalizes the metrics, and securely loads the data into a relational enterprise database to feed a live web dashboard.

**View the Live Dashboard:** [cloud-financial-dashboard.vercel.app] 

## 🏗️ Architecture & Tech Stack

* **Compute:** Oracle Cloud Infrastructure (OCI) Serverless Functions (Docker/Linux)
* **Language:** Python 3.11 (`requests`, `oracledb`)
* **Database:** Oracle Autonomous Database (Relational SQL)
* **API Middleware:** Oracle REST Data Services (ORDS)
* **Frontend UI:** HTML5/JavaScript hosted on Vercel
* **Data Source:** Yahoo Finance API

## ⚙️ How It Works (The Data Flow)

1. **Extract:** A serverless Python function is triggered to fetch real-time, unstructured JSON market data (S&P 500, AAPL, MSFT) via REST API.
2. **Transform:** The script parses the JSON payload, isolating specific quantitative metrics including Current Price, Day High, Day Low, and Trading Volume.
3. **Load:** The function authenticates with an Oracle Autonomous Database using a secure cryptographic wallet. The data is inserted into the `FINANCIAL_METRICS` table utilizing strictly parameterized SQL queries to maintain data integrity and prevent SQL injection vulnerabilities.
4. **Serve:** Oracle REST Data Services (ORDS) exposes the database table as a secure, read-only API endpoint. A lightweight Vercel frontend fetches this endpoint to visualize the metrics dynamically.

## 🔒 Security Notes

To maintain strict security standards and protect database integrity, the Oracle Cloud cryptographic wallet files (`cwallet.sso`, `tnsnames.ora`, etc.) and database credentials have been explicitly excluded from this public repository via `.gitignore`. 

## 📄 File Structure

* `func.py` - The core ETL handler executed by the Oracle serverless container.
* `requirements.txt` - Python dependencies required for the Docker build.
