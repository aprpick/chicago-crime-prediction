# Chicago Crime Prediction - Data Processing Pipeline

**Project:** XGBoost Crime Prediction Model for Chicago (2023-2025)  
**Goal:** Predict crime severity by 3-hour time blocks per community area

---

## Script Overview

### 01_run_pipeline.py
**Purpose:** Attempts to run entire pipeline, currently untested

---

### 02_preview_data.py
**Purpose:** Create 100-row preview for quick testing  
**Input:** `23.1_solar_altitude_added.csv`  
**Output:** `02.1_preview.csv`  

Creates a small sample dataset (100 rows) for testing scripts without loading the full dataset.

---

### 03_deprecated.py
**Status:** Deprecated

---

### 04_data_row_truncator_2023_2025.py
**Purpose:** Filter raw data to 2023-2025 only  
**Input:** `00_chicago_crime_2001_2025_(raw).csv`  
**Output:** `04.1_chicago_crime_2023_2025_(raw).csv`  

Extracts only crimes from 2023-2025 from the full 2001-2025 dataset. Parses date format: `12/27/2025 12:00:00 AM`

---

### 05_data_column_truncator.py
**Purpose:** Trim to 7 essential columns  
**Input:** `04.1_chicago_crime_2023_2025_(raw).csv`  
**Output:** `05.1_columns_removed.csv`  

**Columns kept:**
- ID
- Date
- Primary Type
- Description
- Community Area
- Domestic
- Year

---

### 06_data_analyzer.py
**Purpose:** Analyze column data types and values  
**Input:** `05.1_columns_removed.csv`  
**Output:** `06.1_column_analysis.md`  

Creates markdown report showing:
- Unique values per column
- Null value counts
- Value distributions
- Special handling for Primary Type + Description combinations

---

### 07_domestic_remove.py
**Purpose:** Remove domestic crimes  
**Input:** `05.1_columns_removed.csv`  
**Output:** `07.1_domestics_removed.csv`  

Filters out all crimes where `Domestic = True`, then drops the Domestic column. Domestic crimes have different patterns and aren't suitable for location-based prediction.

---

### 08_remove_enforcement_crimes.py
**Purpose:** Remove enforcement-driven and non-predictable crimes  
**Input:** `07.1_domestics_removed.csv`  
**Output:** `08.1_enforcement_crimes_removed.csv`  

**Removes 16 crime types:**
- Enforcement-driven: NARCOTICS, WEAPONS VIOLATION, PROSTITUTION, GAMBLING, etc.
- Non-predictable: STALKING, DECEPTIVE PRACTICE, OFFENSE INVOLVING CHILDREN
- Too vague: OTHER OFFENSE

These crimes are either only found when police are present or don't have predictable spatial/temporal patterns.

---

### 09_severity_analyzer.py
**Purpose:** Analyze crime hierarchy for severity scoring  
**Input:** `08.1_enforcement_crimes_removed.csv`  
**Output:** `09.1_severity_hierarchy.md`  

Creates markdown report showing all Primary Types with their Description subcategories. Used as reference when manually assigning severity scores (1-10).

---

### 10_remove_rare_combinations.py
**Purpose:** Remove rare crime combinations  
**Input:** `08.1_enforcement_crimes_removed.csv`  
**Output:** `10.1_rare_combos_removed.csv`  

Removes any Primary Type + Description combination with fewer than 100 occurrences. Rare combinations add noise without enough data to train on.

**Threshold:** 100 crimes minimum

---

### 11_add_severity_scores.py
**Purpose:** Add severity scores to crimes  
**Input:** `10.1_rare_combos_removed.csv`  
**Output:** `11.1_severity_added.csv`  

Maps all 88 remaining crime combinations to severity scores (1-10):
- **10:** HOMICIDE, Armed robbery with gun
- **8-9:** Aggravated assault/battery, sexual assault
- **4-7:** Burglary, vehicle theft, arson
- **1-3:** Theft, trespass, minor offenses

**New column:** `Severity_Score`

---

### 12_deprecated.py
**Status:** Deprecated

---

### 13_adding_weekly_columns.py
**Purpose:** Add temporal features  
**Input:** `11.1_severity_added.csv`  
**Output:** `13.1_weekends_added.csv`  

**Adds 5 columns:**
- `hour` - Hour of day (0-23)
- `day_of_week` - Day (0=Monday, 6=Sunday)
- `month` - Month (1-12)
- `weekend_night_peak` - Fri/Sat 9pm-midnight, Sat/Sun midnight-3am (aligned to 3-hour blocks)
- `weekend_regular` - Fri 6-9pm, Sat 3am-9pm, Sun 3am-midnight

---

### 14_adding_holidays.py
**Purpose:** Add holiday features  
**Input:** `13.1_weekends_added.csv`  
**Output:** `14.1_holidays_added.csv`  

**Adds 2 columns:**
- `is_violent_holiday` - NYE, July 4th, Thanksgiving (high violence days)
- `is_theft_holiday` - Christmas shopping period, Black Friday (high theft days)

---

### 15_download_add_weather.py
**Purpose:** Download weather data and merge with crimes  
**Input:** `14.1_holidays_added.csv`  
**Output:** `15.1_weather_data_added.csv`  

Downloads hourly weather from Meteostat (Chicago O'Hare station) for 2023-2025, then merges with crime data by rounding datetime to nearest hour.

**Adds 7 columns:**
- `temp` - Temperature (°C)
- `rhum` - Relative humidity (%)
- `prcp` - Precipitation (mm/hour)
- `wspd` - Wind speed (km/h)
- `wdir` - Wind direction (°)
- `pres` - Atmospheric pressure (hPa)
- `coco` - Weather condition code

---

### 16_weather_DI_add.py
**Purpose:** Calculate weather discomfort indices  
**Input:** `15.1_weather_data_added.csv`  
**Output:** `16.1_weather_DI_added.csv`  

**Adds 2 columns:**
- `heat_DI` - Thom Heat Index (°C) - predicts irritability/violence in summer
- `cold_DI` - Wind Chill (°C) - predicts "empty streets" effect in winter

---

### 17_column_truncator.py
**Purpose:** Remove unnecessary weather columns  
**Input:** `16.1_weather_DI_added.csv`  
**Output:** `17.1_columns_truncated.csv`  

**Removes columns:** prcp, wdir, pres, coco, temp, rhum, wspd, Primary Type, Description

Keeps only the derived discomfort indices and core features needed for training.

---

### 18_3h_blocks_0_crime_blocks.py
**Purpose:** Aggregate to 3-hour blocks and add zero-crime blocks  
**Input:** `16.1_weather_DI_added.csv`  
**Output:** `18.1_3hour_blocks_with_zeros.csv`  

**Major transformation:**
1. Groups hourly data into 3-hour blocks (0-7, representing 00-03, 03-06, etc.)
2. Aggregates by Community Area + Date + Time Block
3. Adds zero-crime blocks for all Community Area × Date × Time Block combinations with no crimes

**Aggregation rules:**
- `crime_count` - COUNT of crimes
- `Severity_Score` - SUM of severities
- `weekend_night_peak`, `weekend_regular`, `is_violent_holiday`, `is_theft_holiday` - MAX (1 if any hour flagged)
- `heat_DI`, `cold_DI` - MEAN (average for block)
- `Year`, `day_of_week`, `month` - FIRST value

**Result:** Complete dataset with ~2 million rows (77 areas × 1,096 days × 8 blocks), most with 0 crimes.

---

### 19_deprecated.py
**Status:** Deprecated

---

### 20_school_in_out.py
**Purpose:** Add school calendar feature  
**Input:** `18.1_3hour_blocks_with_zeros.csv`  
**Output:** `20.1_school_calendar_added.csv`  

**Adds 1 column:**
- `school_in_session` - Binary flag for school hours (8am-3pm on school days)

**Blocks flagged:**
- Block 2 (06-09) - Overlaps hours 8-9
- Block 3 (09-12) - Full overlap
- Block 4 (12-15) - Overlaps hours 12-14

Accounts for CPS calendar: summer breaks, winter breaks, spring breaks, holidays, weekends, professional development days, parent-teacher conferences.

---

## Next Scripts (21-25)

### 21_big_events.py
**Purpose:** Add major Chicago events feature  
**Input:** `20.1_school_calendar_added.csv`  
**Output:** `21.1_major_events_added.csv`  

**Adds 1 column:**
- `major_event` - Binary flag for major city events

**Events tracked:**
- **St. Patrick's Day Parade** - Saturday before/on March 17, 3pm-3am (blocks 5,6,7,0)
- **Pride Parade** - Last Sunday in June, 12pm-11pm (blocks 4,5,6,7)
- **Chicago Marathon** - 2nd Sunday in October, 7am-4pm (blocks 2,3,4,5)
- **Lollapalooza** - First Thu-Sun in August (4 days), 11am-10pm (blocks 3,4,5,6,7)

Automatically calculates event dates for each year (2023-2025) and flags blocks that overlap with event hours.

---

### 22_moon_illumination.py
**Purpose:** Add moon phase feature  
**Input:** `21.1_major_events_added.csv`  
**Output:** `22.1_moon_phase_added.csv`  

**Adds 1 column:**
- `moon_illumination` - Continuous value 0-100% representing moon brightness

**Calculation:**
- Uses astronomical formula based on synodic month (29.53 days)
- Reference: Known new moon January 6, 2000 at 18:14 UTC
- Calculated at start of each 3-hour block
- 0% = New moon (darkest), 100% = Full moon (brightest)

Moon phase changes slowly, so all hours within a 3-hour block have essentially the same illumination.

---

### 23_add_solar_altitude.py
**Purpose:** Add sun position feature  
**Input:** `22.1_moon_phase_added.csv`  
**Output:** `23.1_solar_altitude_added.csv`  

**Adds 1 column:**
- `solar_altitude` - Sun angle in degrees (-90° to 90°)

**Calculation:**
- Uses Astral library with Chicago coordinates (41.88°N, 87.63°W)
- Calculated at midpoint of each 3-hour block (block start + 1.5 hours)
- Positive = daytime (sun above horizon)
- Negative = nighttime (sun below horizon)
- -18° = astronomical twilight (full darkness)

**Requires:** `astral` and `pytz` packages

---

### 24_pretrain_prune.py
**Purpose:** Final cleanup before training  
**Input:** `23.1_solar_altitude_added.csv`  
**Output:** `24.1_training_ready.csv`  

**Removes 3 columns:**
- `block_datetime` - Already encoded in time features
- `time_block` - Redundant with weekend/school/event features
- `crime_count` - Reference only, not a feature

**Final dataset (15 columns):**
- **Features (14):** Community Area, Year, day_of_week, month, weekend_night_peak, weekend_regular, is_violent_holiday, is_theft_holiday, heat_DI, cold_DI, school_in_session, major_event, moon_illumination, solar_altitude
- **Target (1):** Severity_Score

Ready for XGBoost training: `X = df.drop('Severity_Score')`, `y = df['Severity_Score']`

---

### 25_training_complexity_estimator.py
**Purpose:** Analyze dataset and estimate training time  
**Input:** `24.1_training_ready.csv`  
**Output:** `25.1_dataset_analysis.md`  

**Creates markdown report with:**
- Dataset overview (rows, columns, memory usage)
- Feature types (numeric vs. text)
- Training time estimate (based on CPU complexity heuristic)
- Detailed column statistics (type, nulls, min/max/mean/std)

**Checks for:**
- Text columns that need encoding (XGBoost requires numeric)
- Null values
- Data quality issues

**Estimation:** Uses complexity factor (rows × columns) to estimate training time on standard laptop.

---

## Complete Data Flow

```
Raw Data (2001-2025, 8M rows)
  ↓ [04] Filter to 2023-2025
  ↓ [05] Keep 7 columns
  ↓ [07] Remove domestic crimes
  ↓ [08] Remove enforcement crimes (16 types)
  ↓ [10] Remove rare combinations (<100 occurrences)
  ↓ [11] Add severity scores (1-10 scale, 88 combinations)
  ↓ [13] Add temporal features (hour, day_of_week, month, weekends)
  ↓ [14] Add holiday features (violent & theft holidays)
  ↓ [15] Download & merge weather data (Meteostat API)
  ↓ [16] Calculate weather discomfort indices (heat_DI, cold_DI)
  ↓ [17] Remove raw weather columns
  ↓ [18] **MAJOR TRANSFORMATION** - Aggregate to 3-hour blocks + add zeros (~2M rows)
  ↓ [20] Add school calendar (CPS schedule 2023-2025)
  ↓ [21] Add major events (4 Chicago events)
  ↓ [22] Add moon illumination (0-100%)
  ↓ [23] Add solar altitude (-90° to 90°)
  ↓ [24] Remove unnecessary columns
  ↓ [25] Analyze dataset & estimate training time
  ↓ **FINAL:** 24.1_training_ready.csv (15 columns, ~2M rows)
```

---

## Final Dataset Schema

**Dimensions:** ~2 million rows × 15 columns

**Structure:** Community Area (77) × Date (1,096 days) × Time Block (8) = complete grid with zero-crime blocks

**Features (14):**
1. `Community Area` - 1-77 (Chicago community areas)
2. `Year` - 2023, 2024, 2025
3. `day_of_week` - 0-6 (Monday-Sunday)
4. `month` - 1-12
5. `weekend_night_peak` - Binary (Fri/Sat 9pm-midnight, Sat/Sun midnight-3am)
6. `weekend_regular` - Binary (Fri 6-9pm, Sat 3am-9pm, Sun 3am-midnight)
7. `is_violent_holiday` - Binary (NYE, July 4, Thanksgiving)
8. `is_theft_holiday` - Binary (Christmas shopping, Black Friday)
9. `heat_DI` - Continuous (Thom Heat Index in °C)
10. `cold_DI` - Continuous (Wind Chill in °C)
11. `school_in_session` - Binary (8am-3pm on school days, blocks 2-4)
12. `major_event` - Binary (St. Pat's, Pride, Marathon, Lollapalooza)
13. `moon_illumination` - Continuous 0-100%
14. `solar_altitude` - Continuous -90° to 90°

**Target (1):**
15. `Severity_Score` - Integer 0-10 (sum of crime severities in 3-hour block)

---

## Key Design Decisions

### Why 3-hour blocks?
- Balances temporal granularity with data sparsity
- Aligns weekend/event features to block boundaries
- Reduces dataset size while preserving patterns
- Most blocks have 0 crimes (sparse data problem addressed with zero-blocks)

### Why include zero-crime blocks?
- Model needs to learn "what does no crime look like"
- Essential for predicting future crime vs. no crime
- Creates complete grid: every Community Area × Time Block × Date

### Why sum Severity_Score instead of count?
- Severity represents impact, not just frequency
- 3 minor crimes (severity 1 each) = total 3
- 1 major crime (severity 10) = total 10
- Model learns both frequency AND severity patterns

### Feature engineering priorities
1. **Time patterns** - Weekend nights are high-crime periods
2. **School calendar** - Youth crime correlates with school hours
3. **Weather** - Heat stress increases irritability/violence
4. **Moon phase** - Folk wisdom suggests full moon correlation
5. **Solar position** - Day/night affects street activity
6. **Major events** - Large gatherings concentrate both people and crime

---

## Training Recommendations

**Model:** XGBoost (handles large datasets, missing values, non-linear patterns)

**Split strategy:**
- Train: 2023-2024 data
- Test: 2025 data (temporal split)
- OR: 80/20 random split if temporal patterns less important

**Features to try removing (if overfitting):**
- Low-frequency flags: `major_event` (only 1-2% of data)
- Redundant weather: Keep either `temp` OR `heat_DI/cold_DI`

**Hyperparameters to tune:**
- `max_depth`: 6-10 (deeper for complex location patterns)
- `n_estimators`: 100-500 trees
- `learning_rate`: 0.01-0.1
- `subsample`: 0.8 (prevent overfitting with large dataset)

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-08  
**Total Scripts:** 25 (20 active + 5 deprecated)