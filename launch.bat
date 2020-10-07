START /WAIT python -m pip install --user vitualenv
START /WAIT python -m venv capstone-env
CALL .\capstone-env\Scripts\activate
START /WAIT python -m pip install -r requirements.txt
START /WAIT python -m gaming_window
deactivate