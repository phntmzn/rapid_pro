import os
import subprocess
import shutil
from pathlib import Path

# --- Project Info ---
project_name = "SwiftLib"
output_lib = f"lib{project_name}.dylib"
sources = {
    "Greeter.swift": """
public func greeting() -> String {
    return "Hello from SwiftLib!"
}
"""
}

# --- Paths ---
project_dir = Path(project_name)
project_dir.mkdir(exist_ok=True)
source_files = []

# --- Write Swift source files ---
for name, code in sources.items():
    path = project_dir / name
    path.write_text(code.strip() + "\n")
    source_files.append(str(path))

# --- Compile to .dylib ---
compile_cmd = [
    "swiftc",
    "-emit-library",
    "-emit-module",
    "-o", str(project_dir / output_lib),
    *source_files
]

print("Compiling Swift dynamic library...")
result = subprocess.run(compile_cmd, capture_output=True, text=True)

if result.returncode != 0:
    print("Compilation failed:\n", result.stderr)
    exit(1)
else:
    print(f"✅ Successfully built {output_lib} in {project_dir}")

# --- Sign with ad hoc identity (macOS only) ---
print("Signing the dylib with ad hoc identity...")
codesign_result = subprocess.run([
    "codesign",
    "--sign", "-",
    "--force",
    str(project_dir / output_lib)
], capture_output=True, text=True)

if codesign_result.returncode != 0:
    print("❌ Codesign failed:\n", codesign_result.stderr)
else:
    print("✅ Codesigned successfully.")

# --- Archive (zip) the output ---
zip_name = f"{project_name}_build"
shutil.make_archive(zip_name, 'zip', root_dir=project_dir)
print(f"📦 Archived to {zip_name}.zip")
