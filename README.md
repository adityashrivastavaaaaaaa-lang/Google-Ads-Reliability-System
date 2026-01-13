# Google Ads Reliability System (GARS)
### Automated Root Cause & Revenue Leakage Monitoring

**Problem:**
Advertisers lose revenue due to broken tracking, paused campaigns, and unnoticed conversion drops.

**Solution:**
Built a Python + SQL monitoring console that:

* Detects abnormal conversion drops
* Diagnoses root cause (tracking / traffic / website)
* Flags revenue-leaking campaigns
* Quantifies business impact
* Suggests corrective actions in real-time

**Tech Stack:**
Python, Pandas, SQL, Streamlit

**Outcome:**
Automated detection of revenue leakage & conversion tracking failures.

---
### Setup & Usage

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Monitoring Console**
   ```bash
   streamlit run app.py
   ```

3. **Run SQL Revenue Analysis Simulation**
   ```bash
   python3 sql_case.py
   ```
