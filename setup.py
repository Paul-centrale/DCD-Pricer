#!/usr/bin/env python3
"""
DCD Pricer Setup Script
Automatically installs all dependencies and sets up the environment
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def install_requirements():
    """Install all required packages"""
    requirements = [
        "streamlit>=1.28.0",
        "QuantLib-Python>=1.30",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "plotly>=5.15.0"
    ]
    
    print("📦 Installing required packages...")
    for package in requirements:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    
    return True

def create_launch_scripts():
    """Create platform-specific launch scripts"""
    system = platform.system()
    
    if system == "Windows":
        # Windows batch file
        batch_content = """@echo off
echo Starting DCD Pricer...
echo.
echo Opening browser at: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
streamlit run main.py
pause
"""
        with open("launch_dcd_pricer.bat", "w") as f:
            f.write(batch_content)
        print("✅ Created launch_dcd_pricer.bat for Windows")
    
    else:
        # Unix/Linux/macOS shell script
        shell_content = """#!/bin/bash
echo "Starting DCD Pricer..."
echo ""
echo "Opening browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""
streamlit run main.py
"""
        with open("launch_dcd_pricer.sh", "w") as f:
            f.write(shell_content)
        os.chmod("launch_dcd_pricer.sh", 0o755)  # Make executable
        print("✅ Created launch_dcd_pricer.sh for Unix/Linux/macOS")

def main():
    """Main setup function"""
    print("🏦 DCD Pricer Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation")
        return False
    
    # Create launch scripts
    create_launch_scripts()
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the DCD Pricer:")
    
    system = platform.system()
    if system == "Windows":
        print("  • Double-click 'launch_dcd_pricer.bat'")
        print("  • Or run: streamlit run main.py")
    else:
        print("  • Run: ./launch_dcd_pricer.sh")
        print("  • Or run: streamlit run main.py")
    
    print("\nThe application will open in your web browser at:")
    print("http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
