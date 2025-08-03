#!/usr/bin/env python3
"""
DCD Pricer - Easy Setup for International Users
Automatically detects system and installs everything needed
"""

import subprocess
import sys
import os
import platform
import locale

def get_user_language():
    """Detect user's language for localized messages"""
    try:
        lang = locale.getdefaultlocale()[0]
        if lang:
            return lang[:2].lower()  # Get language code (e.g., 'fr' from 'fr_FR')
    except:
        pass
    return 'en'

def print_localized(messages, lang='en'):
    """Print message in user's language if available"""
    message = messages.get(lang, messages.get('en', messages['en']))
    print(message)

def run_command(command, description, silent=False):
    """Run a command and handle errors"""
    if not silent:
        print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if not silent:
            print(f"✅ {description} completed successfully")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        if not silent:
            print(f"❌ Error during {description}:")
            print(f"Error: {e.stderr}")
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    user_lang = get_user_language()
    
    messages = {
        'en': f"✅ Python version {sys.version.split()[0]} is compatible",
        'fr': f"✅ Version Python {sys.version.split()[0]} est compatible",
        'de': f"✅ Python Version {sys.version.split()[0]} ist kompatibel",
        'es': f"✅ Versión de Python {sys.version.split()[0]} es compatible",
        'it': f"✅ Versione Python {sys.version.split()[0]} è compatibile"
    }
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        error_messages = {
            'en': f"❌ Python 3.8 or higher is required. Current version: {sys.version}",
            'fr': f"❌ Python 3.8 ou supérieur est requis. Version actuelle: {sys.version}",
            'de': f"❌ Python 3.8 oder höher ist erforderlich. Aktuelle Version: {sys.version}",
            'es': f"❌ Se requiere Python 3.8 o superior. Versión actual: {sys.version}",
            'it': f"❌ È richiesto Python 3.8 o superiore. Versione attuale: {sys.version}"
        }
        print_localized(error_messages, user_lang)
        return False
    
    print_localized(messages, user_lang)
    return True

def detect_python_command():
    """Detect the correct Python command to use"""
    commands = ['python', 'python3', 'py']
    
    for cmd in commands:
        success, output = run_command(f"{cmd} --version", f"Testing {cmd}", silent=True)
        if success and "Python 3." in output:
            return cmd
    
    return None

def detect_pip_command():
    """Detect the correct pip command to use"""
    python_cmd = detect_python_command()
    if not python_cmd:
        return None
    
    # Try pip commands in order of preference
    pip_commands = [
        'pip',
        'pip3',
        f'{python_cmd} -m pip'
    ]
    
    for cmd in pip_commands:
        success, _ = run_command(f"{cmd} --version", f"Testing {cmd}", silent=True)
        if success:
            return cmd
    
    return f'{python_cmd} -m pip'  # Fallback

def install_requirements():
    """Install all required packages"""
    user_lang = get_user_language()
    
    progress_messages = {
        'en': "📦 Installing required packages...",
        'fr': "📦 Installation des packages requis...",
        'de': "📦 Installiere erforderliche Pakete...",
        'es': "📦 Instalando paquetes requeridos...",
        'it': "📦 Installazione dei pacchetti richiesti..."
    }
    
    print_localized(progress_messages, user_lang)
    
    pip_cmd = detect_pip_command()
    if not pip_cmd:
        error_messages = {
            'en': "❌ Could not find pip command",
            'fr': "❌ Impossible de trouver la commande pip",
            'de': "❌ Pip-Kommando nicht gefunden",
            'es': "❌ No se pudo encontrar el comando pip",
            'it': "❌ Impossibile trovare il comando pip"
        }
        print_localized(error_messages, user_lang)
        return False
    
    # Essential packages with fallback versions
    packages = [
        "streamlit>=1.28.0",
        "numpy>=1.24.0", 
        "pandas>=2.0.0",
        "plotly>=5.15.0"
    ]
    
    # QuantLib is tricky - try different approaches
    quantlib_packages = [
        "QuantLib-Python>=1.30",
        "QuantLib-Python",
        "QuantLib"
    ]
    
    # Install basic packages first
    for package in packages:
        success, _ = run_command(f"{pip_cmd} install {package}", f"Installing {package}")
        if not success:
            # Try without version constraint
            package_name = package.split('>=')[0]
            success, _ = run_command(f"{pip_cmd} install {package_name}", f"Installing {package_name}")
            if not success:
                return False
    
    # Try to install QuantLib
    quantlib_installed = False
    for ql_package in quantlib_packages:
        success, _ = run_command(f"{pip_cmd} install {ql_package}", f"Installing {ql_package}")
        if success:
            quantlib_installed = True
            break
    
    if not quantlib_installed:
        warning_messages = {
            'en': "⚠️ QuantLib installation failed. The app may work with limited functionality.",
            'fr': "⚠️ L'installation de QuantLib a échoué. L'app peut fonctionner avec des fonctionnalités limitées.",
            'de': "⚠️ QuantLib-Installation fehlgeschlagen. Die App funktioniert möglicherweise mit eingeschränkter Funktionalität.",
            'es': "⚠️ La instalación de QuantLib falló. La aplicación puede funcionar con funcionalidad limitada.",
            'it': "⚠️ Installazione di QuantLib fallita. L'app potrebbe funzionare con funzionalità limitate."
        }
        print_localized(warning_messages, user_lang)
    
    return True

def create_launch_scripts():
    """Create platform-specific launch scripts with multiple language support"""
    system = platform.system()
    user_lang = get_user_language()
    
    # Detect correct streamlit command
    python_cmd = detect_python_command()
    streamlit_commands = [
        "streamlit",
        f"{python_cmd} -m streamlit"
    ]
    
    streamlit_cmd = "streamlit"  # Default
    for cmd in streamlit_commands:
        success, _ = run_command(f"{cmd} --version", f"Testing {cmd}", silent=True)
        if success:
            streamlit_cmd = cmd
            break
    
    if system == "Windows":
        # Windows batch file with language support
        batch_content = f"""@echo off
chcp 65001 >nul
title DCD Pricer
echo.
echo ====================================
echo       DCD Pricer - Starting...
echo ====================================
echo.
echo Browser will open at: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
echo Starting application...
{streamlit_cmd} run main.py
if errorlevel 1 (
    echo.
    echo ❌ Error starting application
    echo Try running: {python_cmd} -m streamlit run main.py
    echo.
)
pause
"""
        with open("launch_dcd_pricer.bat", "w", encoding='utf-8') as f:
            f.write(batch_content)
        
        success_messages = {
            'en': "✅ Created launch_dcd_pricer.bat for Windows",
            'fr': "✅ Créé launch_dcd_pricer.bat pour Windows", 
            'de': "✅ launch_dcd_pricer.bat für Windows erstellt",
            'es': "✅ Creado launch_dcd_pricer.bat para Windows",
            'it': "✅ Creato launch_dcd_pricer.bat per Windows"
        }
        print_localized(success_messages, user_lang)
    
    else:
        # Unix/Linux/macOS shell script
        shell_content = f"""#!/bin/bash

echo ""
echo "===================================="
echo "      DCD Pricer - Starting..."
echo "===================================="
echo ""
echo "Browser will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""
echo "Starting application..."
echo ""

# Try to start streamlit
if ! {streamlit_cmd} run main.py; then
    echo ""
    echo "❌ Error starting application"
    echo "Try running: {python_cmd} -m streamlit run main.py"
    echo ""
    read -p "Press Enter to continue..."
fi
"""
        with open("launch_dcd_pricer.sh", "w") as f:
            f.write(shell_content)
        os.chmod("launch_dcd_pricer.sh", 0o755)  # Make executable
        
        success_messages = {
            'en': "✅ Created launch_dcd_pricer.sh for Unix/Linux/macOS",
            'fr': "✅ Créé launch_dcd_pricer.sh pour Unix/Linux/macOS",
            'de': "✅ launch_dcd_pricer.sh für Unix/Linux/macOS erstellt", 
            'es': "✅ Creado launch_dcd_pricer.sh para Unix/Linux/macOS",
            'it': "✅ Creato launch_dcd_pricer.sh per Unix/Linux/macOS"
        }
        print_localized(success_messages, user_lang)

def create_desktop_shortcut():
    """Create desktop shortcut if possible"""
    system = platform.system()
    
    try:
        if system == "Windows":
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "DCD Pricer.lnk")
            target = os.path.join(os.getcwd(), "launch_dcd_pricer.bat")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.IconLocation = target
            shortcut.save()
            
            print("✅ Created desktop shortcut")
            
    except ImportError:
        pass  # Skip if modules not available
    except Exception:
        pass  # Skip if shortcut creation fails

def test_installation():
    """Test if the installation works"""
    user_lang = get_user_language()
    
    test_messages = {
        'en': "🧪 Testing installation...",
        'fr': "🧪 Test de l'installation...",
        'de': "🧪 Installation wird getestet...",
        'es': "🧪 Probando instalación...",
        'it': "🧪 Test dell'installazione..."
    }
    print_localized(test_messages, user_lang)
    
    # Test if we can import the main modules
    test_code = """
try:
    import streamlit
    import numpy
    import pandas
    import plotly
    print("SUCCESS: All basic modules imported")
except ImportError as e:
    print(f"ERROR: {e}")
    exit(1)

try:
    import QuantLib
    print("SUCCESS: QuantLib imported")
except ImportError:
    print("WARNING: QuantLib not available")
"""
    
    python_cmd = detect_python_command()
    success, output = run_command(f'{python_cmd} -c "{test_code}"', "Testing imports", silent=True)
    
    if success and "SUCCESS: All basic modules imported" in output:
        success_messages = {
            'en': "✅ Installation test passed!",
            'fr': "✅ Test d'installation réussi!",
            'de': "✅ Installationstest bestanden!",
            'es': "✅ ¡Prueba de instalación exitosa!",
            'it': "✅ Test di installazione superato!"
        }
        print_localized(success_messages, user_lang)
        return True
    else:
        error_messages = {
            'en': "❌ Installation test failed",
            'fr': "❌ Test d'installation échoué",
            'de': "❌ Installationstest fehlgeschlagen",
            'es': "❌ Prueba de instalación falló",
            'it': "❌ Test di installazione fallito"
        }
        print_localized(error_messages, user_lang)
        return False

def main():
    """Main setup function with multi-language support"""
    user_lang = get_user_language()
    
    title_messages = {
        'en': "🏦 DCD Pricer - International Setup",
        'fr': "🏦 DCD Pricer - Configuration Internationale", 
        'de': "🏦 DCD Pricer - Internationale Einrichtung",
        'es': "🏦 DCD Pricer - Configuración Internacional",
        'it': "🏦 DCD Pricer - Configurazione Internazionale"
    }
    
    print_localized(title_messages, user_lang)
    print("=" * 50)
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Language: {user_lang}")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        error_messages = {
            'en': "\n❌ Setup failed during package installation",
            'fr': "\n❌ Configuration échouée lors de l'installation des packages",
            'de': "\n❌ Setup während Paketinstallation fehlgeschlagen",
            'es': "\n❌ Configuración falló durante la instalación de paquetes", 
            'it': "\n❌ Configurazione fallita durante l'installazione dei pacchetti"
        }
        print_localized(error_messages, user_lang)
        return False
    
    # Create launch scripts
    create_launch_scripts()
    
    # Create desktop shortcut (optional)
    create_desktop_shortcut()
    
    # Test installation
    if not test_installation():
        warning_messages = {
            'en': "\n⚠️ Setup completed but with warnings. The application might still work.",
            'fr': "\n⚠️ Configuration terminée mais avec des avertissements. L'application peut encore fonctionner.",
            'de': "\n⚠️ Setup abgeschlossen, aber mit Warnungen. Die Anwendung könnte trotzdem funktionieren.",
            'es': "\n⚠️ Configuración completada pero con advertencias. La aplicación aún podría funcionar.",
            'it': "\n⚠️ Configurazione completata ma con avvisi. L'applicazione potrebbe ancora funzionare."
        }
        print_localized(warning_messages, user_lang)
    
    # Success message
    success_messages = {
        'en': "\n🎉 Setup completed successfully!",
        'fr': "\n🎉 Configuration terminée avec succès!",
        'de': "\n🎉 Setup erfolgreich abgeschlossen!",
        'es': "\n🎉 ¡Configuración completada exitosamente!",
        'it': "\n🎉 Configurazione completata con successo!"
    }
    print_localized(success_messages, user_lang)
    
    # Instructions
    instruction_messages = {
        'en': "\nTo run the DCD Pricer:",
        'fr': "\nPour exécuter le DCD Pricer:",
        'de': "\nSo starten Sie den DCD Pricer:",
        'es': "\nPara ejecutar el DCD Pricer:",
        'it': "\nPer eseguire il DCD Pricer:"
    }
    print_localized(instruction_messages, user_lang)
    
    system = platform.system()
    if system == "Windows":
        print("  • Double-click 'launch_dcd_pricer.bat'")
        print("  • Or run: streamlit run main.py")
    else:
        print("  • Run: ./launch_dcd_pricer.sh")
        print("  • Or run: streamlit run main.py")
    
    url_messages = {
        'en': "\nThe application will open in your web browser at:",
        'fr': "\nL'application s'ouvrira dans votre navigateur web à:",
        'de': "\nDie Anwendung wird in Ihrem Webbrowser geöffnet unter:",
        'es': "\nLa aplicación se abrirá en su navegador web en:",
        'it': "\nL'applicazione si aprirà nel vostro browser web all'indirizzo:"
    }
    print_localized(url_messages, user_lang)
    print("http://localhost:8501")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
        
        # Wait for user input before closing
        user_lang = get_user_language()
        wait_messages = {
            'en': "\nPress Enter to exit...",
            'fr': "\nAppuyez sur Entrée pour quitter...",
            'de': "\nDrücken Sie Enter zum Beenden...",
            'es': "\nPresione Enter para salir...",
            'it': "\nPremere Invio per uscire..."
        }
        input(wait_messages.get(user_lang, wait_messages['en']))
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
