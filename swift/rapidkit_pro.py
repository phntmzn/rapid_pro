import os
import subprocess
from pathlib import Path
import shutil

# --- Configuration ---
framework_name = "MIDIKit"
sources = {
    "MIDISession.swift": """
import Foundation
import CoreMIDI

public class MIDISession {
    public init() {
        print("Initializing MIDI Session")
    }

    public func listMIDIDevices() {
        let count = MIDIGetNumberOfDevices()
        for i in 0..<count {
            let device = MIDIGetDevice(i)
            var name: Unmanaged<CFString>?
            if MIDIObjectGetStringProperty(device, kMIDIPropertyName, &name) == noErr,
               let nameStr = name?.takeRetainedValue() {
                print("Device #\\(i): \\(nameStr)")
            }
        }
    }
}
""",
    "InternalUtils.swift": """
import CoreMIDI

func midiClient() -> MIDIClientRef {
    var client = MIDIClientRef()
    MIDIClientCreate("PythonSwiftClient" as CFString, nil, nil, &client)
    return client
}
"""
}

# --- Paths ---
root = Path(framework_name)
src_dir = root / "Sources" / framework_name
root.mkdir(parents=True, exist_ok=True)
src_dir.mkdir(parents=True, exist_ok=True)

# --- Step 1: Write Swift Source Files ---
for filename, content in sources.items():
    with open(src_dir / filename, "w") as f:
        f.write(content.strip() + "\n")

# --- Step 2: Write Package.swift ---
package_file = root / "Package.swift"
package_file.write_text(f"""// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "{framework_name}",
    platforms: [.macOS(.v10_15)],
    products: [
        .library(name: "{framework_name}", type: .dynamic, targets: ["{framework_name}"])
    ],
    targets: [
        .target(
            name: "{framework_name}",
            dependencies: [],
            path: "Sources/{framework_name}",
            linkerSettings: [.linkedFramework("CoreMIDI")]
        )
    ]
)
""")

# --- Step 3: Build Framework ---
print("🎹 Building Swift MIDI framework...")
build_cmd = ["swift", "build", "-c", "release"]
result = subprocess.run(build_cmd, cwd=root, capture_output=True, text=True)

if result.returncode != 0:
    print("❌ Build failed:\n", result.stderr)
    exit(1)
else:
    print("✅ Build succeeded.")

# --- Step 4: Sign the Dynamic Binary ---
binary_path = root / ".build" / "release" / framework_name
print("🔏 Signing binary with ad hoc identity...")
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

# --- Step 5: Archive Result ---
archive_name = f"{framework_name}_release"
shutil.make_archive(archive_name, "zip", root_dir=root / ".build" / "release")
print(f"📦 Archived to {archive_name}.zip")
