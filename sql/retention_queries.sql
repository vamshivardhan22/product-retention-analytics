-- Product analytics SQL examples

-- Funnel counts
SELECT event_name, COUNT(DISTINCT user_id) AS users
FROM events
WHERE event_name IN ('signup', 'session_start', 'view_feature', 'activation', 'checkout_start', 'purchase')
GROUP BY event_name;

-- Monthly acquisition cohorts
SELECT strftime('%Y-%m', MIN(event_time)) AS signup_month, COUNT(DISTINCT user_id) AS users
FROM events
WHERE event_name = 'signup'
GROUP BY signup_month
ORDER BY signup_month;

-- Inactive users after first month
SELECT user_id, MAX(event_time) AS last_seen
FROM events
GROUP BY user_id
HAVING julianday('2025-10-01') - julianday(MAX(event_time)) > 30;
