import hashlib # For generating the hashes
import os
import json
import argparse # You don't need this if you only need it to run inside the same folder, but any modifications to the script would be a security risk
from pathlib import Path # This should be multiplatform compatible

# --- CORE FUNCTIONS ---

def calculate_file_hash(filepath):
    """
    Calculates the SHA-256 hash of a file.
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None

def scan_directory(directory_path):
    """
    Recursively scans the TARGET directory.
    """
    files_dict = {}
    target_path = Path(directory_path)
    
    if not target_path.exists():
        print(f"[-] Error: The directory '{directory_path}' does not exist.")
        return {}

    # os.walk allows us to look into sub-directories automatically
    for root, dirs, files in os.walk(target_path):
        for file in files:
            # 1. Ignore .DS_Store
            if file == ".DS_Store":
                continue
            
            # Create the full path
            full_path = Path(root) / file
            
            # Calculate the hash
            file_hash = calculate_file_hash(full_path)
            
            # Store it in our dictionary with the ABSOLUTE path
            if file_hash: 
                files_dict[str(full_path.resolve())] = file_hash
            
    return files_dict

def save_baseline(data, filename="baseline.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n[+] Baseline saved to '{filename}' (in current directory)")

def load_baseline(filename="baseline.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def compare_baselines(baseline, current_scan):
    alerts = []
    
    # Check for Modifications and New Files
    for filepath, current_hash in current_scan.items():
        if filepath not in baseline:
            alerts.append(f"[NEW] File created: {filepath}")
        elif baseline[filepath] != current_hash:
            alerts.append(f"[MODIFIED] content changed: {filepath}")
            
    # Check for Deletions
    for filepath in baseline:
        if filepath not in current_scan:
            alerts.append(f"[DELETED] File removed: {filepath}")
            
    return alerts

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="File Integrity Monitor")
    parser.add_argument("target_dir", help="The directory you want to monitor")
    args = parser.parse_args()

    # The baseline stays HERE (where the script is), not in the target dir
    BASELINE_FILE = "baseline.json"
    target_dir = args.target_dir

    print("\n--- Sentinel-FIM: File Integrity Monitor ---")
    print(f"Targeting: {os.path.abspath(target_dir)}")
    print(f"Baseline storage: {os.path.abspath(BASELINE_FILE)}")
    print("-" * 40)
    print("1. Initialize Baseline")
    print("2. Run Integrity Check")
    
    choice = input("\nSelect mode (1/2): ")
    
    if choice == "1":
        print("Calculating hashes...")
        data = scan_directory(target_dir)
        if data: # Only save if we actually found something or the folder exists
            save_baseline(data, BASELINE_FILE)
        
    elif choice == "2":
        if not os.path.exists(BASELINE_FILE):
             print("[-] 'baseline.json' not found. Please run Mode 1 first.")
        else:
            baseline_data = load_baseline(BASELINE_FILE)
            
            print("Scanning current files...")
            current_data = scan_directory(target_dir)
            
            print("Comparing against baseline...")
            alerts = compare_baselines(baseline_data, current_data)
            
            print(f"\nScan complete. Found {len(alerts)} alerts:")
            print("-" * 30)
            if len(alerts) == 0:
                print("✅ System Secure. No changes detected.")
            else:
                for alert in alerts:
                    print(alert)
    else:
        print("Invalid choice.")
