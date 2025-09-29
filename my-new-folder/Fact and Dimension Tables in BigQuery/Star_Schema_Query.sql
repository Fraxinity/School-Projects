WITH ranked_names AS (
  SELECT 
    -- Dimensions
    s.state_code,
    s.state_category,
    t.decade_start,
    t.period_label,
    f.name_standardized,
    
    -- Measure: Total births for the name in the decade
    SUM(f.births_count) AS total_births,
    
    -- Ranking: Top names per state by TOTAL decade births
    ROW_NUMBER() OVER (
      PARTITION BY s.state_code 
      ORDER BY SUM(f.births_count) DESC
    ) AS name_rank
  FROM 
    `sampleproj-472411.class_dw.fact_names` f  -- Start from fact table
  JOIN 
    `sampleproj-472411.class_dw.dim_state` s ON f.state_code = s.state_code 
  JOIN 
    `sampleproj-472411.class_dw.dim_time` t ON f.year = t.year 
  JOIN 
    `sampleproj-472411.class_dw.dim_gender` g ON f.gender = g.gender  
  WHERE 
    t.period_label = '21st Century'  -- Filter to 2000s (2000-2009)
    AND f.state_code IS NOT NULL  -- Ensure valid states
    AND g.gender = 'M'  -- Selecting only Male
  GROUP BY 
    s.state_code, s.state_category, t.decade_start, t.period_label, g.gender_label, f.name_standardized  --aggregate to the following needed rank
)
SELECT 
  state_code,
  state_category,
  period_label,
  name_standardized,
  total_births,
  name_rank
FROM ranked_names
WHERE name_rank <= 5  -- Top 5 per state (now unique names)
ORDER BY 
  state_code, name_rank;  -- Sort by state, then rank
