import pandas as pd
import sys

def diagnose_drop(file_path):
    alerts = []
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()
        
        # Ensure required columns exist
        required = {'date', 'clicks', 'conversions'}
        if not required.issubset(df.columns):
             pass

        df['date'] = pd.to_datetime(df['date'])

        daily = df.groupby('date').agg({
            'clicks': 'sum',
            'conversions': 'sum',
            'cost': 'sum' if 'cost' in df.columns else lambda x: 0,
            'revenue': 'sum' if 'revenue' in df.columns else lambda x: 0
        }).reset_index()

        daily['conv_rate'] = daily['conversions'] / daily['clicks']
        daily['change_pct'] = daily['conversions'].pct_change() * 100
        
        avg_clicks = daily['clicks'].mean()

        # Check for drops
        drop_days = daily[daily['change_pct'] < -20]

        for _, row in drop_days.iterrows():
            dropped_pct = round(row['change_pct'], 2)
            
            # --- INCIDENT OBJECT ---
            alert = {
                'date': row['date'].strftime('%Y-%m-%d'),
                'drop_pct': dropped_pct,
                'severity': 'LOW',
                'cause': 'Unknown',
                'recommendation': 'Investigate manually.',
                'revenue_at_risk': 0.0,
                'action_steps': []
            }
            
            # Use Cost as proxy for risk if Revenue is 0, or Lost Revenue if we have it
            # Simple formula: Cost - Revenue (if Cost > Revenue)
            cost = row['cost']
            revenue = row['revenue'] if 'revenue' in row else 0
            alert['revenue_at_risk'] = max(0, cost - revenue)

            # --- SEVERITY ENGINE ---
            if row['conversions'] == 0 and cost > 500:
                alert['severity'] = '🔴 CRITICAL'
            elif dropped_pct < -50:
                alert['severity'] = '🟠 HIGH'
            elif dropped_pct < -20:
                alert['severity'] = '🟡 MEDIUM'
            
            # --- ROOT CAUSE & ACTION ENGINE ---
            if row['clicks'] > 1000 and row['conversions'] < 5:
                # Tracking Issue
                alert['cause'] = 'Tracking Broken'
                alert['recommendation'] = 'Check tag firing on /checkout page.'
                alert['action_steps'] = [
                    "✔ Check Google Tag firing on checkout page",
                    "✔ Verify GTM Container version is live",
                    "✔ Inspect browser console for 404/500 errors on conversion pixels"
                ]
            elif row['clicks'] < avg_clicks * 0.5:
                 # Traffic Issue
                 alert['cause'] = 'Traffic Paused'
                 alert['recommendation'] = 'Verify campaign status in Google Ads UI.'
                 alert['action_steps'] = [
                     "✔ Verify campaign status in Google Ads UI",
                     "✔ Check for Ad Disapprovals or Policy violations",
                     "✔ Review Budget caps and bid adjustments"
                 ]
            else:
                 # Website Issue
                 alert['cause'] = 'Website Issue'
                 alert['recommendation'] = 'Review checkout logs and payment gateway.'
                 alert['action_steps'] = [
                     "✔ Inspect payment gateway logs for failures",
                     "✔ Test checkout flow manually on Mobile and Desktop",
                     "✔ Check server logs for backend latency spikes"
                 ]
            
            alerts.append(alert)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return alerts

def print_alerts(alerts):
    if not alerts:
        print("No significant drops detected.")
        return

    for alert in alerts:
        print(f"\n ALERT on {alert['date']}")
        print(f"Severity: {alert['severity']}")
        print(f"Revenue at Risk: ${alert['revenue_at_risk']:.2f}")
        print(f"Likely cause: {alert['cause']}")
        print("Next Steps:")
        for step in alert['action_steps']:
            print(f"  {step}")

if __name__ == "__main__":
    file_to_run = "traffic_drop_data.csv"
    if len(sys.argv) > 1:
        file_to_run = sys.argv[1]
    
    results = diagnose_drop(file_to_run)
    print_alerts(results)
