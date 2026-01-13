import streamlit as st
import pandas as pd
from conversion_debugger import diagnose_drop
import io

st.set_page_config(page_title="Ads Reliability System", page_icon="📈", layout="wide")

st.title("🛡️ Google Ads Reliability System")
st.markdown("### 🚀 Production Monitoring Console")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Upload Ad Traffic CSV", type=["csv"])
    st.info("Upload daily traffic data to detect revenue leakage.")

if uploaded_file is not None:
    # Save temp
    with open("temp_upload.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Run Analysis
    alerts = diagnose_drop("temp_upload.csv")
    
    # --- BUSINESS IMPACT PANEL ---
    if alerts:
        total_risk = sum([a['revenue_at_risk'] for a in alerts])
        affected_days = len(alerts)
        max_severity = "LOW"
        if any("CRITICAL" in a['severity'] for a in alerts):
            max_severity = "🔴 CRITICAL"
        elif any("HIGH" in a['severity'] for a in alerts):
            max_severity = "🟠 HIGH"
        elif any("MEDIUM" in a['severity'] for a in alerts):
            max_severity = "🟡 MEDIUM"

        col1, col2, col3 = st.columns(3)
        col1.metric("Revenue at Risk", f"₹{total_risk:,.2f}")
        col2.metric("Affected Days", affected_days)
        col3.metric("Priority Level", max_severity)
        
        st.markdown("---")
    
    # --- ALERTS SECTION ---
    if not alerts:
        st.success("✅ No anomalies detected. Systems normal.")
    else:
        st.subheader("⚠️ Active Incidents")
        for alert in alerts:
            sev = alert['severity']
            
            # Card UI
            with st.expander(f"{sev} | {alert['date']} | Drop: {alert['drop_pct']}% | Risk: ₹{alert['revenue_at_risk']:.2f}", expanded=True):
                c1, c2 = st.columns([1, 1])
                
                with c1:
                    st.markdown(f"**Likely Cause:** {alert['cause']}")
                    st.markdown(f"**Recommendation:** {alert['recommendation']}")
                
                with c2:
                    st.markdown("**Next Steps (Engineer Actions):**")
                    for step in alert['action_steps']:
                        st.markdown(step)

        # --- EXPORT SECTION ---
        st.markdown("---")
        df_alerts = pd.DataFrame(alerts)
        csv = df_alerts.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📄 Download Incident Report",
            data=csv,
            file_name='incident_report.csv',
            mime='text/csv',
        )

else:
    # Landing Page State
    st.info("Awaiting Data Stream...")
    
    # Demo Data
    if st.button("Load Live Demo Data"):
        demo_csv = """date,clicks,conversions,cost,revenue
2025-12-01,1000,100,500,2000
2025-12-02,1000,100,500,2000
2025-12-03,1200,80,600,1600
2025-12-04,1100,2,550,0
2025-12-05,200,10,100,200
"""
        with open("demo_data.csv", "w") as f:
            f.write(demo_csv)
        
        # experimental_rerun is deprecated in newer versions, use rerun() or just let streamlit handle state
        # st.rerun() 
        
        # Let's run logic directly for demo
        alerts = diagnose_drop("demo_data.csv")
        
        # --- BUSINESS IMPACT PANEL ---
        total_risk = sum([a['revenue_at_risk'] for a in alerts])
        affected_days = len(alerts)
        max_severity = "LOW"
        if any("CRITICAL" in a['severity'] for a in alerts):
            max_severity = "🔴 CRITICAL"

        col1, col2, col3 = st.columns(3)
        col1.metric("Revenue at Risk", f"₹{total_risk:,.2f}")
        col2.metric("Affected Days", affected_days)
        col3.metric("Priority Level", max_severity)
        
        st.subheader("⚠️ Active Incidents")
        for alert in alerts:
            with st.expander(f"{alert['severity']} | {alert['date']} | Drop: {alert['drop_pct']}%", expanded=True):
                st.write(f"Cause: {alert['cause']}")
                st.markdown("**Next Steps:**")
                for step in alert['action_steps']:
                    st.markdown(step)
                
                # Export for demo too
                df_alerts = pd.DataFrame(alerts)
                csv = df_alerts.to_csv(index=False).encode('utf-8')
                st.download_button(label="📄 Download Report", data=csv, file_name='demo_report.csv', mime='text/csv')

# Footer
st.markdown("---")
st.markdown("**Google Solutions Engineer Prep** | System Status: Online 🟢")
