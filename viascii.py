import sys
import subprocess

# Define the command to run the script
args = ["python", "src/main.py"]

# Add any additional arguments to `args` if needed, for example:
args.extend(sys.argv[1:])

try:
    subprocess.run(args=args)
except KeyboardInterrupt:
    pass