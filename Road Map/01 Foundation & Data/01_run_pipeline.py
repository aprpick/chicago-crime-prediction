"""
MASTER PIPELINE RUNNER
Runs all data processing scripts in order from 04 to 25
Skips deprecated scripts (01, 03, 12, 19)
"""

import subprocess
import sys
import os
from datetime import datetime

# ============================================================
# PIPELINE CONFIGURATION
# ============================================================

# List of scripts to run IN ORDER (skipping deprecated ones)
PIPELINE_SCRIPTS = [
    '04_data_row_truncator_2023_2025.py',
    '05_data_column_truncator.py',
    '06_data_analyzer.py',
    '07_domestic_remove.py',
    '08_remove_enforcement_crimes.py',
    '09_severity_analyzer.py',
    '10_remove_rare_combinations.py',
    '11_add_severity_scores.py',
    # 12 is deprecated
    '13_adding_weekly_columns.py',
    '14_adding_holidays.py',
    '15_download_add_weather.py',
    '16_weather_DI_add.py',
    '17_column_truncator.py',
    '18_3h_blocks_0_crime_blocks.py',
    # 19 is deprecated
    '20_school_in_out.py',
    '21_big_events.py',
    '22_moon_illumination.py',
    '23_add_solar_altitude.py',
    '24_pretrain_prune.py',
    '25_training_complexity_estimator.py',
]

# Optional: Scripts to skip (comment out to run all)
SKIP_SCRIPTS = [
    # '06_data_analyzer.py',  # Uncomment to skip analysis scripts
    # '09_severity_analyzer.py',
    # '25_training_complexity_estimator.py',
]

# ============================================================

def run_script(script_name, script_number, total_scripts):
    """Run a single Python script and return success status"""
    print("\n" + "=" * 80)
    print(f"[{script_number}/{total_scripts}] RUNNING: {script_name}")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Run the script and capture output in real-time
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,  # Raises exception if script fails
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print()
        print(f"✓ COMPLETED: {script_name}")
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print(f"✗ FAILED: {script_name}")
        print(f"Error code: {e.returncode}")
        print(f"Failed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return False
    except FileNotFoundError:
        print()
        print(f"✗ ERROR: Script not found: {script_name}")
        return False
    except Exception as e:
        print()
        print(f"✗ UNEXPECTED ERROR: {str(e)}")
        return False

def main():
    print("=" * 80)
    print("                    CHICAGO CRIME PREDICTION")
    print("                     FULL PIPELINE RUNNER")
    print("=" * 80)
    print(f"\nPipeline started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total scripts to run: {len(PIPELINE_SCRIPTS)}")
    
    if SKIP_SCRIPTS:
        print(f"Scripts to skip: {len(SKIP_SCRIPTS)}")
        for script in SKIP_SCRIPTS:
            print(f"  - {script}")
    
    print("\n" + "=" * 80)
    input("Press ENTER to start the pipeline (or Ctrl+C to cancel)...")
    print("=" * 80)
    
    # Track results
    start_time = datetime.now()
    results = []
    
    # Run each script
    for i, script_name in enumerate(PIPELINE_SCRIPTS, 1):
        # Skip if in skip list
        if script_name in SKIP_SCRIPTS:
            print(f"\n[{i}/{len(PIPELINE_SCRIPTS)}] SKIPPING: {script_name}")
            results.append((script_name, 'SKIPPED'))
            continue
        
        # Run script
        success = run_script(script_name, i, len(PIPELINE_SCRIPTS))
        results.append((script_name, 'SUCCESS' if success else 'FAILED'))
        
        # Stop pipeline if script failed
        if not success:
            print("\n" + "=" * 80)
            print("PIPELINE STOPPED - Script failed")
            print("=" * 80)
            break
    
    # Final summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print("                      PIPELINE SUMMARY")
    print("=" * 80)
    print(f"\nStarted:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}")
    
    # Count results
    success_count = sum(1 for _, status in results if status == 'SUCCESS')
    failed_count = sum(1 for _, status in results if status == 'FAILED')
    skipped_count = sum(1 for _, status in results if status == 'SKIPPED')
    
    print(f"\n✓ Successful: {success_count}")
    print(f"✗ Failed:     {failed_count}")
    print(f"○ Skipped:    {skipped_count}")
    
    # Detailed results
    print("\n" + "-" * 80)
    print("DETAILED RESULTS:")
    print("-" * 80)
    for script_name, status in results:
        symbol = "✓" if status == "SUCCESS" else ("✗" if status == "FAILED" else "○")
        print(f"{symbol} {script_name:50s} - {status}")
    
    print("\n" + "=" * 80)
    if failed_count == 0 and success_count > 0:
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("   Ready for training: 24.1_training_ready.csv")
        print("   Analysis report: 25.1_dataset_analysis.md")
    elif failed_count > 0:
        print("⚠️  PIPELINE INCOMPLETE - Check errors above")
    else:
        print("ℹ️  No scripts were run")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("PIPELINE CANCELLED BY USER")
        print("=" * 80)
        sys.exit(1)