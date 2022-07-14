from core.algo import manhattan
import os


path = os.path.join(os.getcwd(), "src/py/logs/")
print("PATH: ")
print(path)

file = open(os.path.join(path, "a.log"))
lines = file.readlines()

print("\nFILE LINES: \n")
print(lines)


file.close()
