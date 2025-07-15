# Organizes solutions into a structured directory based on problem completeness
# It copies .SOL and .sas files for problems that have at least 5 solutions into a new directory structure. 

import os
import re
import shutil

solutions_folder = './solutions'
target_sol_folder = './solutions_organized'

# Identify full problems based on having at least 6 .SOL files
completed_dict = {}
for file in os.listdir(solutions_folder):
    if file.endswith(".SOL"):
        problem = file.split(".")[0]
        if "_" in problem:
            problem = file.split("_")[0]
        completed_dict[problem] = completed_dict.get(problem, 0) + 1

full_problems = {problem for problem, cnt in completed_dict.items() if cnt == 6}
print("Full problems:", len(full_problems))

# Regex to match files like p123456_0.SOL or p123456_1.sas (case-insensitive)
pattern = re.compile(r'^(?P<problem>p\d+)_(\d+|og).*\.?(?P<ext>SOL|sas)$', re.IGNORECASE)

# Loop through all files in the solutions folder and copy only those for full problems
for filename in os.listdir(solutions_folder):
    file_path = os.path.join(solutions_folder, filename)
    if os.path.isfile(file_path):
        match = pattern.match(filename)
        if match:
            problem = match.group("problem")
            if problem in full_problems:
                ext = match.group("ext").lower()  # normalize extension to lower-case
                # Set target subdirectory based on file extension
                if ext == "sol":
                    subfolder = "sols"
                elif ext == "sas":
                    subfolder = "sas"
                else:
                    continue

                # Construct directory paths
                problem_folder = os.path.join(target_sol_folder, problem)
                target_folder = os.path.join(problem_folder, subfolder)
                os.makedirs(target_folder, exist_ok=True)

                # Build target file path and copy file
                target_file = os.path.join(target_folder, filename)
                # print(f"Copying {filename} to {target_file}")
                shutil.copy(file_path, target_file)
