@echo off
echo Starting SayDeck server...
C:/Users/bestcomp/AppData/Local/Programs/Python/Python313/python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
