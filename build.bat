@echo off

echo cleaning...
rmdir __pycache__ /s /q
rmdir dist /s /q
rmdir build /s /q
del bot.spec

echo building...
pyinstaller -F --clean bot.py

echo cleaning unnecessary files...
rmdir build /s /q
del bot.spec

echo copying dependencies...
copy dist-depends\chromedriver.exe dist
copy dist-depends\run.bat dist

echo zipping files into archive...
cd dist
mkdir bot
copy * bot
winrar a -afzip bot.zip bot
rmdir bot /s /q

pause