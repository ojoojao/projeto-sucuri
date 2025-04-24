import os, subprocess
from .sintaxe import a_palavras_reservadas, r_palavras_reservadas, funcoes, operadores

def transform_in_py(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as suc:
        t = suc.readlines()
    suc.close()

    lines = []
    for i, l in enumerate(t):
        lines.append(l)

        for k in a_palavras_reservadas.keys():
            if k in lines[i]:
                lines[i] = str(lines[i]).replace(k, a_palavras_reservadas[k])
        
        for k in r_palavras_reservadas.keys():
            if k in lines[i]:
                lines[i] = str(lines[i]).replace(k, r_palavras_reservadas[k])
        
        for k in funcoes.keys():
            if k in lines[i]:
                lines[i] = str(lines[i]).replace(k, funcoes[k])

    text = ""
    for l in lines:
        text += l
    
    i = file_path[::-1].find("/")
    file = file_path[::-1][:i][::-1]
    i = file_path.find(file)
    path = file_path[:i]
    path = path + "run_files/"
    
    file = file.replace(".su", ".py")

    file_path = path + file

    if not os.path.exists(path):
        os.makedirs(path)  
        os.system(f'attrib +h "{path[:-1]}"') 

    with open(file_path, 'w', encoding='utf-8') as py:
        py.write(text)

    py.close()
    
    return file_path

def py_cmd_to_su(cmd_text: str):   
    t = cmd_text.splitlines()

    lines = []
    for i, l in enumerate(t):
        lines.append(l)

        for k in a_palavras_reservadas.keys():
            if a_palavras_reservadas[k] in lines[i]:
                lines[i] = str(lines[i]).replace(a_palavras_reservadas[k], k)
        
        for k in r_palavras_reservadas.keys():
            if r_palavras_reservadas[k] in lines[i]:
                lines[i] = str(lines[i]).replace(r_palavras_reservadas[k], k)
        
        for k in funcoes.keys():
            if funcoes[k] in lines[i]:
                lines[i] = str(lines[i]).replace(funcoes[k], k)

    text = ""
    for l in lines:
        text += l + "\n"

    return text

def run_script(file_path: str):
    command = f"python {file_path}" # Replace your_script.py with the actual script name.
    process = subprocess.run(command, capture_output=True, text=True, shell=True, encoding="utf-8")

    output = process.stdout
    error = process.stderr

    if process.returncode == 0:
        su_output = py_cmd_to_su(output)
        
        return su_output
    else:
        return f"Erro ao executar arquivo... \n{error}\n{process.returncode}\n{output}"