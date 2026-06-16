-- Product behavior analytics SQL examples for Online Shoppers Purchasing Intention.
-- This is session-level data, so analysis focuses on conversion behavior and engagement.

SELECT
  COUNT(*) AS sessions,
  SUM(CASE WHEN revenue = 1 THEN 1 ELSE 0 END) AS conversions,
  ROUND(100.0 * AVG(revenue), 2) AS conversion_rate
FROM sessions;

SELECT
  visitortype,
  COUNT(*) AS sessions,
  ROUND(100.0 * AVG(revenue), 2) AS conversion_rate,
  ROUND(AVG(pagevalues), 2) AS avg_page_value
FROM sessions
GROUP BY visitortype
ORDER BY conversion_rate DESC;

SELECT
  traffictype,
  COUNT(*) AS sessions,
  ROUND(100.0 * AVG(revenue), 2) AS conversion_rate,
  ROUND(AVG(bouncerates), 4) AS avg_bounce_rate,
  ROUND(AVG(exitrates), 4) AS avg_exit_rate
FROM sessions
GROUP BY traffictype
ORDER BY sessions DESC;
