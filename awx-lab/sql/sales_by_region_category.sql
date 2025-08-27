SELECT 
    t.SalesTerritoryRegion AS Region,         -- 지역
    p.EnglishProductName AS Product,          -- 제품 이름
    pr.EnglishPromotionType AS Promotion,     -- 프로모션 유형
    SUM(f.SalesAmount) AS TotalSales          -- 총 매출
FROM FactInternetSales AS f
JOIN DimProduct AS p
    ON f.ProductKey = p.ProductKey
JOIN DimPromotion AS pr
    ON f.PromotionKey = pr.PromotionKey
JOIN DimSalesTerritory AS t
    ON f.SalesTerritoryKey = t.SalesTerritoryKey
GROUP BY t.SalesTerritoryRegion, p.EnglishProductName, pr.EnglishPromotionType
ORDER BY TotalSales DESC;
