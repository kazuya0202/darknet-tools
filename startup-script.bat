@echo off

rem == not argument ==
if "%1" == "" (
	echo Usage:
	echo   Drag and drop '.py' or '.sh' file.

	echo.
	pause
	exit /b
)

rem == BBox ==
if "%~n1%~x1" == "BBox-Label-Tool.py" (
	echo Exec: [python %~n1%~x1]
	python %1 datasets

	if not errorlevel 0 (call :errOccured)

rem == convert ==
) else if "%~n1%~x1" == "convert.py" (
	echo Exec: [python %~n1%~x1]
	python %1 datasets

	if not errorlevel 0 (call :errOccured)

rem == inflate ==
) else if "%~n1%~x1" == "inflate_images.py" (
	echo Exec: [python %~n1%~x1]
	rem スクリプト実行
	python %1 datasets

	if not errorlevel 0 (call :errOccured)

rem == .sh ==
) else if %~n1%~x1 == seqrename.sh (
	cd seqrename-images/
	ren *.JPG *.jpg
	cd ..

	echo Exec: [bash %~n1%~x1]
	bash "%~n1%~x1"
	if not errorlevel 0 (call :errOccured)

	rem ren .\\seqrename-images\\*.JPG .\\seqrename-images\\*.jpg

rem == not any ==
) else (
	echo This extension is not '.py' or '.sh'.
	echo Please drag and drop '.py' or '.sh' file.
	
	call :normal
)

echo.
pause
exit /b

:errOccured
	echo. 
	echo Error occurred.
