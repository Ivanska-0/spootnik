with open("gpt-text.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    if line.startswith("="):
        lines.remove(line)

with open("gpt-text-parsed.txt", "w") as f:
    f.writelines(lines)
