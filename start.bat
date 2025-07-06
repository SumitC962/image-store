@echo off
echo Starting Secure Image Storage Website...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting the server...
echo.
echo The website will be available at: http://localhost:5000
echo Default password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
pause 