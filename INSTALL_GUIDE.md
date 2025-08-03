# DCD Pricer - Complete Installation Guide

## 🌍 For International Users

This guide will help you set up the DCD Pricer on any computer, regardless of your technical background.

## 📋 What You Need

- A computer with Windows, Mac, or Linux
- Internet connection
- About 10 minutes

## 🚀 Step-by-Step Installation

### Step 1: Download Python (if not installed)

**Check if Python is already installed:**
- **Windows**: Open Command Prompt (press Windows + R, type `cmd`, press Enter) and type: `python --version`
- **Mac**: Open Terminal (press Cmd + Space, type "Terminal") and type: `python3 --version`
- **Linux**: Open Terminal and type: `python3 --version`

If you see a version number like "Python 3.x.x", skip to Step 2.

**Install Python if needed:**
1. Go to https://python.org/downloads/
2. Download the latest Python version (3.8 or higher)
3. **IMPORTANT**: During installation, check "Add Python to PATH" ✅
4. Complete the installation

### Step 2: Download DCD Pricer Files

1. Download all the DCD Pricer files to a folder (e.g., Desktop/DCD_Pricer)
2. Make sure you have these files:
   - `main.py`
   - `setup.py`
   - `requirements.txt`
   - `README.md`

### Step 3: Run Automatic Setup

#### Windows Users:
1. Navigate to your DCD Pricer folder
2. **Method A**: Double-click `setup.py`
3. **Method B**: 
   - Right-click in the folder while holding Shift
   - Select "Open PowerShell window here" or "Open command window here"
   - Type: `python setup.py`
   - Press Enter

#### Mac/Linux Users:
1. Open Terminal
2. Navigate to your DCD Pricer folder:
   ```bash
   cd /path/to/your/DCD_Pricer_folder
   ```
3. Run setup:
   ```bash
   python3 setup.py
   ```

### Step 4: Launch the Application

After setup completes successfully:

#### Windows:
- Double-click `launch_dcd_pricer.bat`
- Or run: `streamlit run main.py`

#### Mac/Linux:
- Double-click `launch_dcd_pricer.sh`
- Or run: `./launch_dcd_pricer.sh`
- Or run: `streamlit run main.py`

### Step 5: Access the Application

1. The application will automatically open in your web browser
2. If not, manually go to: http://localhost:8501
3. You should see the DCD Pricer interface

## 🔧 Manual Installation (If Automatic Fails)

If the automatic setup doesn't work, follow these manual steps:

### 1. Install Required Packages

Open Terminal/Command Prompt and run these commands one by one:

```bash
pip install streamlit
pip install QuantLib-Python
pip install numpy
pip install pandas
pip install plotly
```

**For Mac/Linux users, use `pip3` instead of `pip`:**
```bash
pip3 install streamlit
pip3 install QuantLib-Python
pip3 install numpy
pip3 install pandas
pip3 install plotly
```

### 2. Run the Application

Navigate to your DCD Pricer folder and run:
```bash
streamlit run main.py
```

## 🌐 Language-Specific Instructions

### 🇫🇷 Instructions en Français

1. **Télécharger Python**: Allez sur https://python.org/downloads/
2. **Installer les packages**: Ouvrez l'invite de commande et tapez `python setup.py`
3. **Lancer l'application**: Double-cliquez sur `launch_dcd_pricer.bat` (Windows) ou `launch_dcd_pricer.sh` (Mac/Linux)

### 🇩🇪 Anweisungen auf Deutsch

1. **Python herunterladen**: Gehen Sie zu https://python.org/downloads/
2. **Pakete installieren**: Öffnen Sie die Eingabeaufforderung und geben Sie `python setup.py` ein
3. **Anwendung starten**: Doppelklicken Sie auf `launch_dcd_pricer.bat` (Windows) oder `launch_dcd_pricer.sh` (Mac/Linux)

### 🇪🇸 Instrucciones en Español

1. **Descargar Python**: Vaya a https://python.org/downloads/
2. **Instalar paquetes**: Abra el símbolo del sistema y escriba `python setup.py`
3. **Iniciar aplicación**: Haga doble clic en `launch_dcd_pricer.bat` (Windows) o `launch_dcd_pricer.sh` (Mac/Linux)

### 🇮🇹 Istruzioni in Italiano

1. **Scaricare Python**: Andare su https://python.org/downloads/
2. **Installare pacchetti**: Aprire il prompt dei comandi e digitare `python setup.py`
3. **Avviare applicazione**: Fare doppio clic su `launch_dcd_pricer.bat` (Windows) o `launch_dcd_pricer.sh` (Mac/Linux)

## ❌ Common Problems & Solutions

### Problem: "python: command not found"
**Solution**: 
- Reinstall Python and make sure to check "Add Python to PATH"
- On Mac/Linux, try using `python3` instead of `python`

### Problem: "pip: command not found"
**Solution**:
- Python installation may be incomplete
- Try: `python -m pip install package_name`
- On Mac: `python3 -m pip install package_name`

### Problem: "Permission denied"
**Solution**:
- **Windows**: Run Command Prompt as Administrator
- **Mac/Linux**: Add `sudo` before commands: `sudo pip3 install package_name`

### Problem: "Port 8501 is already in use"
**Solution**:
- Use a different port: `streamlit run main.py --server.port 8502`
- Or close other applications using that port

### Problem: Application doesn't open in browser
**Solution**:
- Manually go to: http://localhost:8501
- Check if firewall is blocking the connection
- Try: http://127.0.0.1:8501

## 📞 Getting Help

1. **Check this guide first** - most issues are covered here
2. **Verify Python installation**: Run `python --version` or `python3 --version`
3. **Check internet connection** - required for package downloads
4. **Try manual installation** if automatic setup fails

## 🎯 Success Indicators

You know everything is working when:
- ✅ Setup script completes without errors
- ✅ Browser opens automatically
- ✅ You see "DCD (Dual Currency Deposit) Pricer" at the top
- ✅ You can change parameters and see results update

## 💡 Pro Tips

1. **Create a desktop shortcut** to the launch script for easy access
2. **Bookmark http://localhost:8501** in your browser
3. **Keep the DCD Pricer folder** in an easy-to-find location
4. **Update packages occasionally**: Run `pip install --upgrade streamlit QuantLib-Python`

## 🔐 Security Note

The DCD Pricer runs locally on your computer. No data is sent to external servers - everything stays on your machine.
