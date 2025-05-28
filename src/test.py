import os

print(os.path.exists(os.path.join(os.getcwd(), "src")))

print()

print(os.path.join(os.getcwd(), os.path.join("src", "temp") if os.path.exists("src") else os.path.join("temp")))
