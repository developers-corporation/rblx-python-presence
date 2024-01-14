
python3 -m pip install --upgrade pip
python3 -m pip install wheel
python3 -m pip install -r ../requirements.txt
cd ..
# use pyinstaller to compile the python script into a console unix executable universal2 binary
python3 -m PyInstaller --onefile --console  --name="rblx-python-presence" main.py