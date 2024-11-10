import sys
import subprocess

# Define the command to run the script
args = ["python", "src/main.py"]

args.extend(sys.argv[1:])

try:
    subprocess.run(args=args)
except KeyboardInterrupt:
    pass
