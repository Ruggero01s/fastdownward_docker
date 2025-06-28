import os

import click
from os.path import  join, isdir
from utils import load_from_folder
from multiprocess import Pool

problem_count = 0

def run_script(script: str):
    global problem_count
    print(f'Running {script}\n Counter: {problem_count}')
    problem_count += 1
    os.system(f'chmod +x {script}')
    os.system(script)


def clear_scripts_dir(scripts_path: str):
    if os.path.isdir(scripts_path):
        os.system(f'rm -r {scripts_path}')
    os.system(f'mkdir -p {scripts_path}')


def check_if_already_solved(sol_path, problem_name):
    problem_sol_path = os.path.join(sol_path, f"{problem_name}.SOL")
    
    if os.path.exists(problem_sol_path):
        return True
    else:
        problem_sol_path = os.path.join(sol_path, f"{problem_name}_output.sas")
        if os.path.exists(problem_sol_path):
            return True
        else:
            problem_sol_path = os.path.join("main/og_solutions", f"{problem_name}.SOL")
            if os.path.exists(problem_sol_path):
                return True
            else:
                return False

@click.command()
@click.option('--python-path', 'python_path', type=click.STRING,
              default='/opt/anaconda/anaconda3/envs/goal_rec/bin/python', help='Path to Python bin file')
@click.option('--logger-dir', 'logger_dir', type=click.STRING,
              default='/home/rsignoroni/fastdownward_docker/logs', help='Folder where to save logs')
@click.option('--file-path', 'file_path', type=click.STRING, help='Python file to execute')
@click.option('--nodes', type=click.INT, default=2, help='Number of nodes per qsub process')
@click.option('--source-dir', 'source_dir', type=click.STRING, help='Folder that contains the problems')
@click.option('--target-dir', 'target_dir', type=click.STRING, help='Folder where to save the plans')
@click.option('--addit-params', 'addit_params', type=click.STRING, help='Additional parameters to pass to the python file', default='')
@click.option('--memory-limit', 'memory_limit', type=click.INT, help='Memory limit in MB', default=-1)
@click.option('--problem-number', 'problem_number', type=click.INT, default=100, help='Number of problems to process')
@click.option('--test', is_flag=True, help='Flag for running only 2 instances')
def run(python_path, logger_dir, file_path, nodes, source_dir, target_dir, problem_number, test, addit_params, memory_limit):
    scripts_path = './main/scripts/'
    script_name = 'script_{0}.sh'

    clear_scripts_dir(scripts_path)
    os.makedirs(scripts_path, exist_ok=True)
    os.makedirs(logger_dir, exist_ok=True)

    
    plans_paths = []
    plan_names = []
    for rec_class in [c for c in os.listdir(source_dir) if os.path.isdir(f"{source_dir}/{c}")]:
        for problem_dir in os.listdir(f"{source_dir}/{rec_class}"):
            for problem_file in os.listdir(f"{source_dir}/{rec_class}/{problem_dir}"):
                if problem_file.lower().endswith('.pddl') and problem_file != 'domain.pddl': #todo test for og sols
                    if not check_if_already_solved(target_dir, problem_file.split('.')[0]):
                        plans_paths.append(f"{source_dir}/{rec_class}/{problem_dir}/{problem_file}")
                        plan_names.append({problem_file})
    print(len(plans_paths))
    # print(plans_paths)
    print(len(plan_names))
    # print(plan_names)
    # plans = os.listdir(source_dir)
    # [not_completed_plans] = load_from_folder('/home/mchiari/state_embedding/', ['logistics_not_completed_gr.txt'])
    for i, plan in enumerate(plans_paths):
        # if plan == 'domain.pddl' or f"{plan.rsplit('.',1)[0]}\n" not in not_completed_plans:
        #     continue
        # plan_name = plan.split(os.sep)[:-1].split(".")[0]
        # print(f'Processing {plan_name} ({i+1}/{len(plans_paths)})')
    
        with open(f'{scripts_path}{script_name.format(i)}', 'w') as f:
            f.write('#!/bin/bash\n')
            if memory_limit > 0:
                f.write(f'ulimit -v {memory_limit}\n')
            f.write(f'{python_path} {file_path} --input "{plan}" {addit_params} > {os.path.join(logger_dir, f"logs_script_{i}_plan{plan_names[i]}.txt")} 2> {os.path.join(logger_dir, f"logs_script_{i}_plan{plan_names[i]}.err.txt")}')
            #f.write(f'{python_path} {file_path} -p {os.path.join(source_dir,plan)} {addit_params} ')
            f.close()
        # os.system(
        #     #f'qsub -o {logger_dir}{plan}_out.log -e {logger_dir}{plan}out.err.log -q longbatch -l nodes=minsky.ing.unibs.it:ppn={nodes} {scripts_path}{script_name.format(i)}')
        #     f'chmod +x {scripts_path}{script_name.format(i)}')
        if test and i >= 1:
            break
        elif i+1 >= problem_number:
            break
    scripts = [os.path.join(scripts_path, s) for s in os.listdir(scripts_path) if s.startswith('script')]
    with Pool(nodes) as p:
        p.map(run_script, scripts)
    
    

if __name__ == '__main__':
    run()