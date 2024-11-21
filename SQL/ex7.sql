CREATE VIEW UserSubscriptionDetails AS
SELECT
    u.email AS UserEmail,
    u.display_name AS DisplayName,
    u.start_date_of_subscription AS SubscriptionStartDate,
    s.TierName AS SubscriptionTier,
    s.Price AS SubscriptionPrice,
    s.Duration AS SubscriptionDuration
FROM
    User u
LEFT JOIN
    SubscriptionTiers s
ON
    u.subscription_type_id = s.TierName;


CREATE VIEW RevenueByAdvertiser AS
SELECT
    a.company AS AdvertiserName,
    COUNT(ad.AdId) AS NumberOfAds,
    SUM(ad.costOfAd) AS TotalExpenditure
FROM
    Advertiser a
JOIN
    Advertisement ad
ON
    a.company = ad.company
GROUP BY
    a.company;


CREATE VIEW EnhancedUserSubscriptionDetails AS
SELECT
    u.email AS UserEmail,
    u.display_name AS DisplayName,
    u.start_date_of_subscription AS SubscriptionStartDate,
    DATE_ADD(u.start_date_of_subscription, INTERVAL s.Duration MONTH) AS SubscriptionEndDate,
    s.TierName AS SubscriptionTier,
    s.Price AS SubscriptionPrice,
    s.Duration AS SubscriptionDuration
FROM
    User u
LEFT JOIN
    SubscriptionTiers s
ON
    u.subscription_type_id = s.TierName
WHERE
    u.start_date_of_subscription IS NOT NULL
    AND DATE_ADD(u.start_date_of_subscription, INTERVAL s.Duration MONTH) >= CURRENT_DATE;

CREATE VIEW DetailedRevenueByAdvertiser AS
SELECT
    a.company AS AdvertiserName,
    COUNT(ad.AdId) AS NumberOfAds,
    SUM(ad.costOfAd) AS TotalExpenditure,
    AVG(ad.costOfAd) AS AverageAdCost,
    CASE
        WHEN SUM(ad.costOfAd) > 10000 THEN 'High Spender'
        ELSE 'Low Spender'
    END AS AdvertiserCategory
FROM
    Advertiser a
JOIN
    Advertisement ad
ON
    a.company = ad.company
GROUP BY
    a.company;