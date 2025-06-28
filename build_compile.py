import subprocess
import os
from templates import utils_code, main_code  # 👈 import from separated module

# --- Directory Setup ---
src_dir = "src"
os.makedirs(src_dir, exist_ok=True)

# --- Write Source Files ---
with open(os.path.join(src_dir, "utils.py"), "w") as f:
    f.write(utils_code)

with open(os.path.join(src_dir, "main.py"), "w") as f:
    f.write(main_code)

# --- PyInstaller Build ---
print("Compiling with PyInstaller...")
build_cmd = [
    "pyinstaller",
    "--onefile",
    "--distpath", "dist",
    "--workpath", "build",
    "--specpath", "build",
    os.path.join(src_dir, "main.py")
]

result = subprocess.run(build_cmd, capture_output=True, text=True)

if result.returncode != 0:
    print("Build failed:\n", result.stderr)
else:
    print("Build succeeded. Executable is in ./dist/main")

    # --- Run Compiled Executable ---
    exe_path = os.path.join("dist", "main")
    print("\nRunning compiled executable:\n")
    run_result = subprocess.run([exe_path], capture_output=True, text=True)
    print(run_result.stdout)
