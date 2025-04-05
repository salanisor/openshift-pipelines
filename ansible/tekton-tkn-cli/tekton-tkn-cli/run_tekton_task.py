import subprocess
import argparse
import os

def run_tekton_task(task_name, params=None):
    try:
        # Base command to start a Tekton task
        command = ["tkn", "task", "start", task_name]
        
        # Add parameters if provided
        if params:
            for key, value in params.items():
                command.extend(["--param", f"{key}={value}"])
        
        # Run the `tkn` CLI command
        result = subprocess.run(
            command,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ  # Pass the current environment, including KUBECONFIG
        )
        print("Task started successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to start the task:")
        print(e.stderr)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run a Tekton task using tkn CLI.")
    parser.add_argument("--task_name", type=str, required=True, help="Name of the Tekton task to run")
    parser.add_argument("--params", nargs="*", default=[], help="Parameters in key=value format")
    parser.add_argument("--kubeconfig", type=str, required=True, help="Path to the kubeconfig file")
    args = parser.parse_args()

    # Set the KUBECONFIG environment variable
    os.environ["KUBECONFIG"] = args.kubeconfig

    # Convert params into a dictionary
    params_dict = {}
    for param in args.params:
        if "=" in param:
            key, value = param.split("=")
            params_dict[key] = value

    # Run the Tekton task
    run_tekton_task(args.task_name, params_dict)

'''
# Using command-line arguments
python run_tekton_task.py --task_name example-task --params input=hello output=world --kubeconfig /path/to/your/kubeconfig

# Using environment variables
export TEKTON_TASK_NAME="example-task"
export TEKTON_PARAMS="input=hello,output=world"
python run_tekton_task.py
'''
