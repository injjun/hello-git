SELECT
    d.CalendarYear AS [Year],
    d.MonthNumberOfYear AS [Month],
    SUM(f.SalesAmount) AS SalesAmount
FROM dbo.FactInternetSales AS f
JOIN dbo.DimDate AS d ON f.OrderDateKey = d.DateKey
GROUP BY d.CalendarYear, d.MonthNumberOfYear
ORDER BY [Year], [Month];
