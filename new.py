import subprocess

def run_script(file_path):
    command = f"python {file_path}" # Replace your_script.py with the actual script name.
    process = subprocess.run(command, capture_output=True, text=True, shell=True, encoding="utf-8")

    output = process.stdout
    error = process.stderr

    if process.returncode == 0:
        print("Command executed successfully:")
        print(output)
        return output
    else:
        print(f"Command failed with error code {process.returncode}:")
        print(error)
        return f"Erro ao executar arquivo... {process.returncode}"