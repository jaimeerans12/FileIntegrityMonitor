import hashlib
import os
import json
from pathlib import Path

# --- CORE FUNCTIONS ---

def calculate_file_hash(filepath):
    """
    Calculates the SHA-256 hash of a file.
    Reads the file in chunks to handle large files (memory efficiency).
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(filepath, "rb") as f:
            # Read the file in 4KB chunks
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
    except PermissionError:
        return "ACCESS_DENIED"

def scan_directory(directory_path):
    """
    Recursively scans a directory and returns a dictionary:
    { 'filepath': 'hash_value' }
    """
    files_dict = {}
    
    # os.walk allows us to look into sub-directories automatically
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # --- IGNORE LIST ---
            # 1. Ignore .DS_Store (macOS metadata)
            # 2. Ignore baseline.json (our own database)
            # 3. Ignore the script itself (optional, but good practice)
            if file in [".DS_Store", "baseline.json", "sentinel.py"]:
                continue
            
            # Create the full path using pathlib
            full_path = Path(root) / file
            
            # Calculate the hash
            file_hash = calculate_file_hash(full_path)
            
            # Store it in our dictionary
            if file_hash: # Only store if we successfully got a hash
                files_dict[str(full_path)] = file_hash
            
    return files_dict

def save_baseline(data, filename="baseline.json"):
    """
    Saves the dictionary of file hashes to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n[+] Baseline saved to {filename}")

def load_baseline(filename="baseline.json"):
    """
    Loads the baseline JSON file into a dictionary.
    """
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def compare_baselines(baseline, current_scan):
    """
    Compares the stored baseline with the current scan.
    Returns a list of alerts.
    """
    alerts = []
    
    # Check for Modifications and New Files
    for filepath, current_hash in current_scan.items():
        if filepath not in baseline:
            alerts.append(f"[NEW] File created: {filepath}")
        elif baseline[filepath] != current_hash:
            alerts.append(f"[MODIFIED] content changed: {filepath}")
            
    # Check for Deletions (Files in baseline that are NOT in current scan)
    for filepath in baseline:
        if filepath not in current_scan:
            alerts.append(f"[DELETED] File removed: {filepath}")
            
    return alerts

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    print("\n--- Sentinel-FIM: File Integrity Monitor ---")
    print("1. Initialize Baseline (Trust current state)")
    print("2. Run Integrity Check")
    
    choice = input("\nSelect mode (1/2): ")
    
    if choice == "1":
        # Scan and Save
        print("Calculating hashes...")
        data = scan_directory('.') # Scanning current folder
        save_baseline(data)
        
    elif choice == "2":
        # Load, Scan, and Compare
        baseline_data = load_baseline()
        
        if not baseline_data:
            print("[-] No baseline found. Run mode 1 first.")
        else:
            print("Scanning current files...")
            current_data = scan_directory('.')
            
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
