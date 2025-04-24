t = "C:/Users/jluca/Documents/python/sucuri"

print("Caminho original:", t)
for i, l in enumerate(t[::-1]):
    if l == '/':       
        t = t[::-1][i:][::-1]
        break

print("Caminho novo:", t)
