# Search for files ending with '_og.output.sas' in the solutions directory
import os
solutions_dir = './solutions'
og_files = [f for f in os.listdir(solutions_dir) if f.endswith('_og.output.sas')]
if og_files:
    print(f"Found OG output SAS files: {og_files}")