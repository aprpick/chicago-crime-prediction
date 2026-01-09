# Event & Holiday Crime Impact Analysis

**Analysis Date:** 2026-01-08 17:46:06
**Dataset:** ../01 Foundation & Data/24.1_training_ready.csv
**Total Blocks Analyzed:** 672,672

---

## Executive Summary

### Major Events (Lollapalooza, St. Patrick's Day, Marathon, Pride)

- **Data Coverage:** 7,392 blocks (1.10% of dataset)
- **Severity Multiplier:** 1.25x baseline
- **Average Severity:** 3.38 (vs 2.71 normally)
- **Impact Assessment:** 🟢 **MINOR IMPACT**

### Violent Holidays (NYE, July 4th, Thanksgiving)

- **Data Coverage:** 12,936 blocks (1.92% of dataset)
- **Severity Multiplier:** 1.01x baseline
- **Average Severity:** 2.75 (vs 2.72 normally)
- **Impact Assessment:** ⚪ **MINIMAL IMPACT**

### Theft Holidays (Black Friday, Christmas Shopping Season)

- **Data Coverage:** 12,936 blocks (1.92% of dataset)
- **Severity Multiplier:** 0.88x baseline
- **Average Severity:** 2.40 (vs 2.73 normally)
- **Impact Assessment:** ⚪ **MINIMAL IMPACT**

---

## Major Events (Lollapalooza, St. Patrick's Day, Marathon, Pride) - Detailed Analysis

### Coverage

| Metric | Value |
|--------|-------|
| Blocks with major_event = 1 | 7,392 |
| Percentage of dataset | 1.10% |

### Severity Statistics

| Statistic | During Event | Non-Event | Difference |
|-----------|--------------|-----------|------------|
| Mean | 3.38 | 2.71 | +0.67 |
| Median | 0.00 | 0.00 | +0.00 |
| Std Dev | 6.38 | 4.62 | +1.76 |
| **Multiplier** | **1.25x** | 1.00x | **+24.7%** |

### Distribution Analysis

| Metric | During Event | Non-Event |
|--------|--------------|-----------|
| Zero-crime blocks | 53.1% | 57.7% |
| High-severity blocks (>10) | 8.5% | 6.6% |
| 25th percentile | 0.00 | 0.00 |
| 50th percentile (median) | 0.00 | 0.00 |
| 75th percentile | 5.00 | 4.00 |

### Interpretation

🟢 **Major Events (Lollapalooza, St. Patrick's Day, Marathon, Pride) cause a MINOR increase** (1.2x baseline). The feature has weak predictive value.
- **Slightly fewer zero-crime blocks** during events (4.6% reduction)
- **Slightly more high-severity blocks** during events (1.9% increase)

---

## Violent Holidays (NYE, July 4th, Thanksgiving) - Detailed Analysis

### Coverage

| Metric | Value |
|--------|-------|
| Blocks with is_violent_holiday = 1 | 12,936 |
| Percentage of dataset | 1.92% |

### Severity Statistics

| Statistic | During Event | Non-Event | Difference |
|-----------|--------------|-----------|------------|
| Mean | 2.75 | 2.72 | +0.03 |
| Median | 0.00 | 0.00 | +0.00 |
| Std Dev | 4.83 | 4.64 | +0.19 |
| **Multiplier** | **1.01x** | 1.00x | **+1.3%** |

### Distribution Analysis

| Metric | During Event | Non-Event |
|--------|--------------|-----------|
| Zero-crime blocks | 58.3% | 57.6% |
| High-severity blocks (>10) | 6.7% | 6.6% |
| 25th percentile | 0.00 | 0.00 |
| 50th percentile (median) | 0.00 | 0.00 |
| 75th percentile | 4.00 | 4.00 |

### Interpretation

⚪ **Violent Holidays (NYE, July 4th, Thanksgiving) show MINIMAL impact** (1.0x baseline). Consider removing this feature.
- **Similar zero-crime rates** during and outside events
- **Slightly more high-severity blocks** during events (0.1% increase)

---

## Theft Holidays (Black Friday, Christmas Shopping Season) - Detailed Analysis

### Coverage

| Metric | Value |
|--------|-------|
| Blocks with is_theft_holiday = 1 | 12,936 |
| Percentage of dataset | 1.92% |

### Severity Statistics

| Statistic | During Event | Non-Event | Difference |
|-----------|--------------|-----------|------------|
| Mean | 2.40 | 2.73 | +-0.33 |
| Median | 0.00 | 0.00 | +0.00 |
| Std Dev | 4.36 | 4.65 | +-0.28 |
| **Multiplier** | **0.88x** | 1.00x | **+-12.1%** |

### Distribution Analysis

| Metric | During Event | Non-Event |
|--------|--------------|-----------|
| Zero-crime blocks | 61.1% | 57.6% |
| High-severity blocks (>10) | 5.4% | 6.6% |
| 25th percentile | 0.00 | 0.00 |
| 50th percentile (median) | 0.00 | 0.00 |
| 75th percentile | 4.00 | 4.00 |

### Interpretation

⚪ **Theft Holidays (Black Friday, Christmas Shopping Season) show MINIMAL impact** (0.9x baseline). Consider removing this feature.
- **Similar zero-crime rates** during and outside events

---

## Most Affected Community Areas

### Major Events

| Community Area | Event Blocks | Mean Severity | Baseline | Increase | Multiplier |
|----------------|--------------|---------------|----------|----------|------------|
| 1 | 96 | 3.46 | 3.53 | +-0.07 | 0.98x |
| 2 | 96 | 3.06 | 3.06 | +-0.00 | 1.00x |
| 3 | 96 | 5.31 | 3.95 | +1.36 | 1.34x |
| 4 | 96 | 2.03 | 1.80 | +0.23 | 1.13x |
| 5 | 96 | 1.88 | 1.16 | +0.72 | 1.61x |
| 6 | 96 | 14.18 | 5.60 | +8.58 | 2.53x |
| 7 | 96 | 4.70 | 3.53 | +1.17 | 1.33x |
| 8 | 96 | 13.07 | 9.30 | +3.77 | 1.40x |
| 9 | 96 | 0.19 | 0.18 | +0.01 | 1.05x |
| 10 | 96 | 0.97 | 0.87 | +0.10 | 1.11x |

### Violent Holidays

| Community Area | Event Blocks | Mean Severity | Baseline | Increase | Multiplier |
|----------------|--------------|---------------|----------|----------|------------|
| 1 | 168 | 3.25 | 3.54 | +-0.29 | 0.92x |
| 2 | 168 | 2.97 | 3.06 | +-0.09 | 0.97x |
| 3 | 168 | 3.83 | 3.97 | +-0.14 | 0.97x |
| 4 | 168 | 1.60 | 1.80 | +-0.20 | 0.89x |
| 5 | 168 | 0.82 | 1.18 | +-0.36 | 0.70x |
| 6 | 168 | 5.80 | 5.69 | +0.11 | 1.02x |
| 7 | 168 | 3.55 | 3.54 | +0.01 | 1.00x |
| 8 | 168 | 10.32 | 9.33 | +0.99 | 1.11x |
| 9 | 168 | 0.33 | 0.18 | +0.15 | 1.86x |
| 10 | 168 | 0.88 | 0.87 | +0.01 | 1.01x |

### Theft Holidays

| Community Area | Event Blocks | Mean Severity | Baseline | Increase | Multiplier |
|----------------|--------------|---------------|----------|----------|------------|
| 1 | 168 | 3.54 | 3.53 | +0.01 | 1.00x |
| 2 | 168 | 2.67 | 3.07 | +-0.40 | 0.87x |
| 3 | 168 | 2.61 | 3.99 | +-1.38 | 0.65x |
| 4 | 168 | 1.85 | 1.80 | +0.05 | 1.03x |
| 5 | 168 | 1.71 | 1.16 | +0.55 | 1.47x |
| 6 | 168 | 4.73 | 5.71 | +-0.98 | 0.83x |
| 7 | 168 | 3.37 | 3.54 | +-0.17 | 0.95x |
| 8 | 168 | 9.40 | 9.35 | +0.05 | 1.01x |
| 9 | 168 | 0.07 | 0.18 | +-0.11 | 0.38x |
| 10 | 168 | 0.91 | 0.87 | +0.04 | 1.04x |

---

## Feature Importance Validation

From your XGBoost model training:

| Feature | Importance | Severity Multiplier | Assessment |
|---------|------------|---------------------|------------|
| major_event | 7.7% | 1.25x | ⚠️ Low impact but HIGH importance - OVERFITTED? |
| is_violent_holiday | 2.8% | 1.01x | ✅ Low impact, low importance - VALIDATED |
| is_theft_holiday | 1.6% | 0.88x | ✅ Low impact, low importance - VALIDATED |

---

## Recommendations

- ❌ **CONSIDER REMOVING major_event** - Only 1.2x increase, weak signal
- ❌ **CONSIDER REMOVING is_violent_holiday** - Only 1.0x increase, weak signal
- ❌ **CONSIDER REMOVING is_theft_holiday** - Only 0.9x increase, weak signal

### Additional Suggestions

1. **Add more events** - Only tracking 4 major events (1.1% of data). Consider adding:
   - Taste of Chicago
   - Air & Water Show
   - Cubs/Sox/Bears home games
   - Concerts at United Center/Wrigley

2. **Finer time granularity** - 3-hour blocks may be too coarse for event spikes

3. **Event-specific features** - Create separate features for different event types:
   - `music_festival` (Lollapalooza, Pitchfork)
   - `parade` (St. Patrick's Day, Pride)
   - `sporting_event` (Marathon, major games)

---

**Visualization:** See `event_severity_comparison.png` for charts