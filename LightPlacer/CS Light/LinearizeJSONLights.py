import json
import os

# Ensures the script looks in the folder where the .py file is saved
script_dir = os.path.dirname(os.path.abspath(__file__))

def process_json_logic(data):
    changed = False
    
    if isinstance(data, dict):
        # 1. Check if we are inside a "data" block
        # We use a case-insensitive check for "data"
        for key in list(data.keys()):
            if key.lower() == "data" and isinstance(data[key], dict):
                sub_data = data[key]
                
                # Check for existing flags (case-insensitive)
                flag_key = next((k for k in sub_data if k.lower() == "flags"), None)
                
                if flag_key:
                    # Case A: Flags entry exists, append if "Linear" is missing
                    if "Linear" not in str(sub_data[flag_key]):
                        val = str(sub_data[flag_key])
                        sub_data[flag_key] = f"{val}|Linear" if val.strip() else "Linear"
                        print(f"    [MODIFIED] {flag_key}: '{val}' -> '{sub_data[flag_key]}'")
                        changed = True
                else:
                    # Case B: Flags entry is missing entirely, create it
                    sub_data["flags"] = "Linear"
                    print(f"    [ADDED] New flags entry: 'Linear' inside '{key}'")
                    changed = True
            
            # 2. Continue searching recursively through other keys
            if process_json_logic(data[key]):
                changed = True
                
    elif isinstance(data, list):
        for item in data:
            if process_json_logic(item):
                changed = True
                
    return changed

def run_update():
    all_files = os.listdir(script_dir)
    json_files = [f for f in all_files if f.lower().endswith('.json')]
    
    if not json_files:
        print(f"No .json files found in {script_dir}")
        return

    for filename in json_files:
        file_path = os.path.join(script_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            print(f"Processing: {filename}")
            if process_json_logic(content):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2)
                print(f"  [SAVED] {filename}")
            else:
                print(f"  [SKIPPED] No changes needed.")
                
        except Exception as e:
            print(f"  [ERROR] Could not process {filename}: {e}")

if __name__ == "__main__":
    print("--- JSON Data/Flags Updater ---")
    run_update()
    #input("\nFinished. Press Enter to exit.")