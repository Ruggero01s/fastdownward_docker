#counts completed FULL PROBLEMS (Have all .SOL files)
import os

solutions_path = "solutions"
completed_dict = {}
total_count_plans = 0
for file in os.listdir(solutions_path):
    if file.endswith(".SOL"):
        name = file.split("_")[0]
        if not (name in completed_dict):
            completed_dict[name] = 0
        completed_dict[name] += 1
        total_count_plans += 1

completed_count = 0
not_completed_count = 0
for key, val in completed_dict.items():
    if val >= 5:
        completed_count += 1
    else:
        # print(f"Problem: {key}, is NOT completed ({val}/5)")
        not_completed_count += 1

print("FULL PROBLEMS: ", completed_count)
print("NOT FULL PROBLEMS: ", not_completed_count)
print("TOTAL PLANS PROCESSED: ", total_count_plans)