script = \
"""
mostra("Olá mundo!")

a = True

caso(a == True):
    mostra(a)
"""

if "mostra(" in script:
    script = script.replace("mostra(", "print(")

if "caso(" in script:
    script = script.replace("caso(", "if(")

print(script)
# teste de escrita

with open("__01.py", 'w', encoding='utf-8') as py_file:
    py_file.write(script)
py_file.close()