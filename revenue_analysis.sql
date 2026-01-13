SELECT 
    campaign_name as campaign,
    SUM(cost) AS total_spend,
    SUM(revenue) AS total_revenue,
    CASE 
        WHEN SUM(revenue) = 0 AND SUM(cost) > 100 THEN 'CRITICAL LEAKAGE'
        ELSE 'OK'
    END AS status
FROM ads_performance
GROUP BY campaign_name
ORDER BY total_spend DESC;
