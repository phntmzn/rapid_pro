import os
import subprocess
from pathlib import Path
import shutil

# --- Configuration ---
framework_name = "MyFramework"
sources = {
    "PublicAPI.swift": """
public class Greeter {
    public init() {}
    public func hello() -> String {
        return "Hello from Greeter!"
    }
}
""",
    "InternalHelper.swift": """
class Helper {
    static func shout(_ msg: String) -> String {
        return msg.uppercased()
    }
}
"""
}

# --- Paths ---
root = Path(framework_name)
src_dir = root / "Sources" / framework_name
root.mkdir(parents=True, exist_ok=True)
src_dir.mkdir(parents=True, exist_ok=True)

# --- Step 1: Write Source Files ---
for filename, content in sources.items():
    with open(src_dir / filename, "w") as f:
        f.write(content.strip() + "\n")

# --- Step 2: Create Package.swift ---
package_file = root / "Package.swift"
package_file.write_text(f"""// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "{framework_name}",
    products: [
        .library(name: "{framework_name}", type: .dynamic, targets: ["{framework_name}"])
    ],
    targets: [
        .target(name: "{framework_name}", path: "Sources/{framework_name}")
    ]
)
""")

# --- Step 3: Build the framework ---
print("Building Swift framework...")
build_cmd = ["swift", "build", "-c", "release"]
result = subprocess.run(build_cmd, cwd=root, capture_output=True, text=True)

if result.returncode != 0:
    print("❌ Build failed:\n", result.stderr)
    exit(1)

print("✅ Build succeeded.")

# --- Step 4: Locate and optionally sign .framework ---
framework_path = root / ".build" / "release" / f"{framework_name}.swiftmodule"
binary_path = root / ".build" / "release" / framework_name

# Sign with ad hoc identity (optional)
print("Signing binary...")
sign_result = subprocess.run([
    "codesign",
    "--force",
    "--sign", "-",
    str(binary_path)
], capture_output=True, text=True)

if sign_result.returncode != 0:
    print("❌ Codesign failed:\n", sign_result.stderr)
else:
    print("✅ Codesigned successfully.")

# --- Step 5: Archive framework ---
archive_name = f"{framework_name}_release"
shutil.make_archive(archive_name, "zip", root_dir=root / ".build" / "release")
print(f"📦 Archived to {archive_name}.zip")
