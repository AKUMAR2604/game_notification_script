import os
from pathlib import Path

def check_env_file():
    # Get the current working directory
    current_dir = os.getcwd()
    env_path = Path(current_dir) / '.env'
    
    print(f"Current directory: {current_dir}")
    print("\nChecking for .env file...")
    
    # Check if file exists
    if not env_path.exists():
        print("❌ ERROR: .env file not found!")
        print(f"Expected location: {env_path}")
        return
    
    print("✓ .env file found!")
    
    # Read and check file contents
    print("\nChecking .env file contents...")
    try:
        with open(env_path, 'r') as f:
            lines = f.readlines()
            
        # Check if file is empty
        if not lines:
            print("❌ ERROR: .env file is empty!")
            return
            
        # Check each line
        expected_vars = ['EMAIL', 'PASSWORD']
        found_vars = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if '=' not in line:
                print(f"❌ Invalid line format: {line}")
                continue
                
            var_name = line.split('=')[0].strip()
            var_value = line.split('=')[1].strip()
            
            found_vars.append(var_name)
            
            # Check for common formatting issues
            if '"' in var_value or "'" in var_value:
                print(f"❌ Warning: Remove quotes from value in line: {line}")
            if ' = ' in line:
                print(f"❌ Warning: Remove spaces around = in line: {line}")
                
        # Check for missing variables
        for var in expected_vars:
            if var in found_vars:
                print(f"✓ Found {var}")
            else:
                print(f"❌ Missing {var}")
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")

if __name__ == "__main__":
    check_env_file()