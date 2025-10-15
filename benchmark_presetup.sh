#!/bin/bash

set -e

# Helper function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check for required runtimes
echo "Checking required runtimes..."

runtimes=(python3 go node bun deno php java dotnet)

for runtime in "${runtimes[@]}"; do
  if command_exists "$runtime"; then
    echo "$runtime is installed."
  else
    echo "Error: $runtime is not installed. Please install it before continuing."
    exit 1
  fi
done

# Install Python packages psutil and distro globally (assumes pip is available)
echo "Installing required Python packages: psutil, distro"
if [ -f /etc/debian_version ]; then
  echo "🟢 Detected Debian/Ubuntu - installing via apt"
  apt update && apt install -y python3-psutil python3-distro
else
  echo "🟡 Non-Debian system - installing via pip using venv"
  python3 -m venv .venv
  . .venv/bin/activate
  pip install --upgrade pip
  pip install psutil distro
fi

# Find and run install.sh scripts inside subfolders of the script directory
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Searching for install.sh scripts in subdirectories of $script_dir ..."

sh_scripts_found=0

for dir in "$script_dir"/*/; do
  if [[ -f "$dir/install.sh" ]]; then
    echo "Running $dir/install.sh..."
    (cd "$dir" && bash install.sh)
    sh_scripts_found=1
  fi
done

if [[ $sh_scripts_found -eq 0 ]]; then
  echo "No install.sh scripts found in subdirectories."
fi

echo "Setup completed successfully."