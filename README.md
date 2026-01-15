Google Ads Reliability System (GARS)

Automated Root Cause & Revenue Leakage Monitoring for Advertising Systems

🔴 Problem

Advertisers frequently lose revenue due to silent failures in their advertising setup, such as:

* Broken or missing conversion tracking tags
* Campaigns paused unintentionally
* Website or traffic changes breaking event tracking
* Sudden conversion drops going unnoticed

These issues often remain undetected for days, leading to significant revenue leakage and delayed diagnosis.

💡 Solution

The Google Ads Reliability System (GARS) is a Python and SQL-based monitoring console designed to proactively detect, diagnose, and quantify revenue-impacting issues in advertising systems.

The system:

* Detects abnormal drops in conversions using trend-based analysis
* Diagnoses likely root causes across tracking, traffic, and website layers
* Flags campaigns leaking revenue in real time
* Quantifies business impact to help prioritize fixes
* Suggests corrective actions before revenue loss escalates

This mirrors real-world workflows used by gTech Ads & Customer Solutions Engineers**.

🚀 Key Capabilities

* 📉 Conversion Drop Detection
  Automatically detects sudden conversion drops (e.g., >50–80%) across campaigns.

* 🧠 Root Cause Diagnosis
  Identifies whether the issue is related to:

  * Tracking implementation
  * Traffic anomalies
  * Website or event-mapping changes

* 💰 Revenue Leakage Identification 
  Flags high-click, low-conversion campaigns with potential revenue impact.

* 📊 Business Impact Quantification
  Estimates revenue loss to help prioritize remediation.

* 🖥 Monitoring Console
  Streamlit-based dashboard for uploading data and visualizing alerts.

---

🧪 Example Scenario

1. An advertiser uploads daily traffic and conversion data.
2. The system detects a 90% conversion drop** on a specific day.
3. GARS flags the anomaly within minutes.
4. Root cause is classified as a tracking failure.
5. Revenue-leaking campaigns are highlighted for immediate action.

This reflects common Google Ads customer incidents.

---

🛠 Tech Stack

* Python – Monitoring & diagnostic logic
* Pandas – Data processing & trend analysis
* SQL – Campaign-level revenue analysis
* Streamlit – Interactive monitoring console

---

⚙️ Setup & Usage

Install Dependencies

```bash
pip install -r requirements.txt
```

 Run Monitoring Console

```bash
streamlit run app.py
```

 Run SQL Revenue Analysis Simulation

```bash
python3 sql_case.py
```

---

📈 Outcome

* Automated detection of **conversion tracking failures**
* Early identification of revenue-leaking campaigns
* Reduced diagnosis time from hours to minutes
* Demonstrates **customer-focused, business-aware engineering**

---

🎯 Why This Project Matters

This project was built to understand how **Customer & Partner Solutions Engineers**:

* Debug complex ad tracking issues
* Protect advertiser revenue proactively
* Translate data into actionable customer insights

It reflects the mindset required for gTech Ads roles at Google.

---

👤 Author

Kumar Aditya
Customer Solutions Engineer Aspirant
Python • SQL • Ads Debugging • Data Analysis
