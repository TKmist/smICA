@echo off
rem This file is part of the smICA repository that is distributed under the MIT license; see below.
rem
rem MIT License
rem
rem Copyright (c) 2026 Tomasz Kalwarczyk
rem
rem Permission is hereby granted, free of charge, to any person obtaining a copy
rem of this software and associated documentation files (the "Software"), to deal
rem in the Software without restriction, including without limitation the rights
rem to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
rem copies of the Software, and to permit persons to whom the Software is
rem furnished to do so, subject to the following conditions:
rem
rem The above copyright notice and this permission notice shall be included in all
rem copies or substantial portions of the Software.
rem
rem THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
rem IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
rem FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
rem AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
rem LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
rem OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
rem SOFTWARE.
rem
rem Reference end-to-end workflow for the standard Windows Command Prompt.
rem The explicit calls near the end are intended as a template for user workflows.

setlocal EnableExtensions DisableDelayedExpansion
set "SCRIPT_DIRECTORY=%~dp0"
if "%SCRIPT_DIRECTORY:~-1%"=="\" set "SCRIPT_DIRECTORY=%SCRIPT_DIRECTORY:~0,-1%"
set "DATA_ROOT=%SCRIPT_DIRECTORY%\REFERENCE_DATA\TypeOfFiltering"
set "RAW_ROOT=%DATA_ROOT%\raw"
set "GATING_ROOT=%DATA_ROOT%\gating"
set "TCSPC_ROOT=%DATA_ROOT%\tcscp"
set "STATE_FILE=%SCRIPT_DIRECTORY%\workflow_state.txt"
set "REPORT_FILE=%SCRIPT_DIRECTORY%\workflow_report.txt"
set "CAPABILITIES_FILE=%SCRIPT_DIRECTORY%\workflow_capabilities.tmp"
set "SMICA_INSTALLATION=%~1"
if not defined SMICA_AUTOMATION_PORT set "SMICA_AUTOMATION_PORT=8765"
if not defined SMICA_AUTOMATION_TIMEOUT set "SMICA_AUTOMATION_TIMEOUT=3600"
if not defined RESUME_WORKFLOW set "RESUME_WORKFLOW=true"
set /a COMPLETED_EXTRACTIONS=0,SKIPPED_EXTRACTIONS=0
set /a COMPLETED_CALCULATIONS=0,SKIPPED_CALCULATIONS=0
if not exist "%STATE_FILE%" echo # Completed extraction and calculation batches are appended below.>"%STATE_FILE%"

rem Locate the environment created by the smICA installer.
if defined SMICA_INSTALLATION if exist "%SMICA_INSTALLATION%\v_smICA_env\Scripts\activate.bat" set "SMICA_VENV=%SMICA_INSTALLATION%\v_smICA_env"
if defined SMICA_INSTALLATION if not defined SMICA_VENV if exist "%SMICA_INSTALLATION%\Scripts\activate.bat" set "SMICA_VENV=%SMICA_INSTALLATION%"
if defined SMICA_INSTALLATION if not defined SMICA_VENV (
    echo The selected smICA installation does not contain v_smICA_env: %SMICA_INSTALLATION%
    exit /b 1
)
if defined SMICA_ENV set "SMICA_VENV=%SMICA_ENV%"
if not defined SMICA_VENV if defined VIRTUAL_ENV for %%D in ("%VIRTUAL_ENV%") do if /I "%%~nxD"=="v_smICA_env" set "SMICA_VENV=%VIRTUAL_ENV%"
if not defined SMICA_VENV if exist "%SCRIPT_DIRECTORY%\..\v_smICA_env\Scripts\activate.bat" set "SMICA_VENV=%SCRIPT_DIRECTORY%\..\v_smICA_env"
if not defined SMICA_VENV if exist "%SCRIPT_DIRECTORY%\..\..\v_smICA_env\Scripts\activate.bat" set "SMICA_VENV=%SCRIPT_DIRECTORY%\..\..\v_smICA_env"
if not defined SMICA_VENV for /f "delims=" %%F in ('where /r "%SCRIPT_DIRECTORY%\..\.." smica-call.bat 2^>nul ^| findstr /i /r "\\v_smICA_env\\Scripts\\smica-call.bat$"') do if not defined SMICA_VENV for %%D in ("%%~dpF..") do set "SMICA_VENV=%%~fD"
if not defined SMICA_VENV (
    echo Cannot locate v_smICA_env.
    echo Pass the smICA installation directory as the first argument:
    echo   run_Analytical_workflow_TCP.bat C:\path\to\smICA-installation
    exit /b 1
)
call "%SMICA_VENV%\Scripts\activate.bat"
if errorlevel 1 exit /b 1
if defined SMICA_CALL (set "SMICA_CLIENT=%SMICA_CALL%") else (set "SMICA_CLIENT=%SMICA_VENV%\Scripts\smica-call.bat")
if not exist "%SMICA_CLIENT%" (
    echo Missing TCP client: %SMICA_CLIENT%
    exit /b 1
)

for /f %%T in ('"%SMICA_VENV%\Scripts\python.exe" -c "import time; print(int(time.time()))"') do set "START_TIME=%%T"
set "STARTED_AT=%DATE% %TIME%"

call :tcp system.health "{}" || goto :failed
call :tcp system.version "{}" || goto :failed
call "%SMICA_CLIENT%" --port "%SMICA_AUTOMATION_PORT%" --timeout "%SMICA_AUTOMATION_TIMEOUT%" system.capabilities "{}" >"%CAPABILITIES_FILE%"
if errorlevel 1 goto :failed
type "%CAPABILITIES_FILE%"
findstr /c:"phot2conc.load_calibration" "%CAPABILITIES_FILE%" >nul
if errorlevel 1 (
    echo The running smICA does not provide phot2conc.load_calibration.
    goto :failed
)
del /q "%CAPABILITIES_FILE%" >nul 2>nul

call :tcp gui.select_mode "{\"mode\":\"extract\"}" || goto :failed

rem Raw extraction. Each dataset call is intentionally visible.
call :extract raw standard_2022_10_frames/5uW false 1 0 || goto :failed
call :extract raw standard_2022_10_frames/10uW false 1 0 || goto :failed
call :extract raw standard_2022_10_frames/20uW false 1 0 || goto :failed
call :extract raw standard_2022_10_frames/40uW false 1 0 || goto :failed
call :extract raw standard_2025_frame_series/19_09_60 false 1 0 || goto :failed
call :extract raw standard_2025_frame_series/19_09_80 false 1 0 || goto :failed
call :extract raw standard_2025_frame_series/19_09_100 false 1 0 || goto :failed
call :extract raw standard_2025_frame_series/22_09_60 false 1 0 || goto :failed
call :extract raw standard_2025_frame_series/22_09_100 false 1 0 || goto :failed
call :extract raw pie_dual_channel_128x128_100_frames/imaging_new_ptu true 1 2 || goto :failed
call :extract raw pie_dual_channel_128x128_100_frames/imaging2_17_07_23 true 1 2 || goto :failed
call :extract raw pie_gfp_256x256_200_frames/shared_pie_calibration true 0 2 || goto :failed
call :extract raw pie_mrna_256x256_200_frames/shared_pie_calibration true 1 0 || goto :failed

rem Standard PIE gating.
call :extract gating pie_dual_channel_128x128_100_frames/imaging_new_ptu true 1 2 || goto :failed
call :extract gating pie_dual_channel_128x128_100_frames/imaging2_17_07_23 true 1 2 || goto :failed
call :extract gating pie_gfp_256x256_200_frames/shared_pie_calibration true 0 2 || goto :failed
call :extract gating pie_mrna_256x256_200_frames/shared_pie_calibration true 1 0 || goto :failed

rem TCSPC background filtering.
call :extract tcscp standard_2022_10_frames/5uW false 1 0 || goto :failed
call :extract tcscp standard_2022_10_frames/10uW false 1 0 || goto :failed
call :extract tcscp standard_2022_10_frames/20uW false 1 0 || goto :failed
call :extract tcscp standard_2022_10_frames/40uW false 1 0 || goto :failed
call :extract tcscp standard_2025_frame_series/19_09_60 false 1 0 || goto :failed
call :extract tcscp standard_2025_frame_series/19_09_80 false 1 0 || goto :failed
call :extract tcscp standard_2025_frame_series/19_09_100 false 1 0 || goto :failed
call :extract tcscp standard_2025_frame_series/22_09_60 false 1 0 || goto :failed
call :extract tcscp standard_2025_frame_series/22_09_100 false 1 0 || goto :failed
call :extract tcscp pie_mrna_256x256_200_frames/shared_pie_calibration true 1 0 || goto :failed
call :extract tcscp pie_gfp_256x256_200_frames/shared_pie_calibration true 0 2 || goto :failed
call :extract tcscp pie_dual_channel_128x128_100_frames/imaging_new_ptu true 1 2 || goto :failed
call :extract tcscp pie_dual_channel_128x128_100_frames/imaging2_17_07_23 true 1 2 || goto :failed

call :tcp gui.select_mode "{\"mode\":\"phot2conc\"}" || goto :failed
rem Disable "Errors as SEM" so the end-to-end test uses combined uncertainty.
call :tcp phot2conc.set_error_mode "{\"sem\":false}" || goto :failed

rem Standard single-channel calculations load calibration files supplied with data.
call :calculate_all raw standard_2022_10_frames/5uW Calib_5uW.json "" || goto :failed
call :calculate_all raw standard_2022_10_frames/10uW Calib_10uW.json "" || goto :failed
call :calculate_all raw standard_2022_10_frames/20uW Calib_20uW.json "" || goto :failed
call :calculate_all raw standard_2022_10_frames/40uW Calib_40uW.json "" || goto :failed
call :calculate_all raw standard_2025_frame_series/19_09_60 calib_19_09_60.json "" || goto :failed
call :calculate_all raw standard_2025_frame_series/19_09_80 calib_19_09_80.json "" || goto :failed
call :calculate_all raw standard_2025_frame_series/19_09_100 calib_19_09_100.json "" || goto :failed
call :calculate_all raw standard_2025_frame_series/22_09_60 calib_22_09_60.json "" || goto :failed
call :calculate_all raw standard_2025_frame_series/22_09_100 calib_22_09_100.json "" || goto :failed
call :calculate_all tcscp standard_2022_10_frames/5uW Calib_5uW.json "" || goto :failed
call :calculate_all tcscp standard_2022_10_frames/10uW Calib_10uW.json "" || goto :failed
call :calculate_all tcscp standard_2022_10_frames/20uW Calib_20uW.json "" || goto :failed
call :calculate_all tcscp standard_2022_10_frames/40uW Calib_40uW.json "" || goto :failed
call :calculate_all tcscp standard_2025_frame_series/19_09_60 calib_19_09_60.json "" || goto :failed
call :calculate_all tcscp standard_2025_frame_series/19_09_80 calib_19_09_80.json "" || goto :failed
call :calculate_all tcscp standard_2025_frame_series/19_09_100 calib_19_09_100.json "" || goto :failed
call :calculate_all tcscp standard_2025_frame_series/22_09_60 calib_22_09_60.json "" || goto :failed
call :calculate_all tcscp standard_2025_frame_series/22_09_100 calib_22_09_100.json "" || goto :failed

rem Raw PIE examples with automatic ROI configuration.
call :calculate_raw_mrna || goto :failed
call :calculate_raw_gfp || goto :failed
call :calculate_raw_dual_new || goto :failed
call :calculate_raw_dual_imaging2 || goto :failed

rem Filtered PIE data reuse ROI files from the matching raw datasets.
call :calculate_all gating pie_mrna_256x256_200_frames/shared_pie_calibration calib.json raw/pie_mrna_256x256_200_frames/shared_pie_calibration/ROI || goto :failed
call :calculate_all gating pie_gfp_256x256_200_frames/shared_pie_calibration calib.json raw/pie_gfp_256x256_200_frames/shared_pie_calibration/ROI || goto :failed
call :calculate_all gating pie_dual_channel_128x128_100_frames/imaging_new_ptu calib_imaging_new_ptu.json raw/pie_dual_channel_128x128_100_frames/imaging_new_ptu/ROI || goto :failed
call :calculate_all gating pie_dual_channel_128x128_100_frames/imaging2_17_07_23 calib_imaging2_17_07_23.json raw/pie_dual_channel_128x128_100_frames/imaging2_17_07_23/ROI || goto :failed
call :calculate_all tcscp pie_mrna_256x256_200_frames/shared_pie_calibration calib.json raw/pie_mrna_256x256_200_frames/shared_pie_calibration/ROI || goto :failed
call :calculate_all tcscp pie_gfp_256x256_200_frames/shared_pie_calibration calib.json raw/pie_gfp_256x256_200_frames/shared_pie_calibration/ROI || goto :failed
call :calculate_all tcscp pie_dual_channel_128x128_100_frames/imaging_new_ptu calib_imaging_new_ptu.json raw/pie_dual_channel_128x128_100_frames/imaging_new_ptu/ROI || goto :failed
call :calculate_all tcscp pie_dual_channel_128x128_100_frames/imaging2_17_07_23 calib_imaging2_17_07_23.json raw/pie_dual_channel_128x128_100_frames/imaging2_17_07_23/ROI || goto :failed

set "WORKFLOW_STATUS=COMPLETED"
set "WORKFLOW_EXIT_CODE=0"
goto :report

:tcp
echo.
echo ^>^>^> %~1 %~2
call "%SMICA_CLIENT%" --port "%SMICA_AUTOMATION_PORT%" --timeout "%SMICA_AUTOMATION_TIMEOUT%" "%~1" "%~2"
exit /b %errorlevel%

:resume_has
if /I not "%RESUME_WORKFLOW%"=="true" exit /b 1
findstr /x /l /c:"%~1" "%STATE_FILE%" >nul 2>nul
exit /b %errorlevel%

:mark_done
findstr /x /l /c:"%~1" "%STATE_FILE%" >nul 2>nul
if errorlevel 1 echo %~1>>"%STATE_FILE%"
exit /b 0

:extract
set "FILTER=%~1"
set "RELATIVE=%~2"
set "SKIP_ROWS=%~3"
set "CHANNEL_1=%~4"
set "CHANNEL_2=%~5"
set "KEY=extraction:%FILTER%:%RELATIVE%"
call :resume_has "%KEY%" && (set /a SKIPPED_EXTRACTIONS+=1 & echo RESUME: skipping %KEY% & exit /b 0)
set "DIRECTORY=%DATA_ROOT%\%FILTER%\%RELATIVE:/=\%"
set "JSON_DIRECTORY=%DIRECTORY:\=/%"
call :tcp extract.load_directory "{\"directory\":\"%JSON_DIRECTORY%\"}" || exit /b 1
call :tcp extract.set_rows_to_skip "{\"enabled\":%SKIP_ROWS%,\"rows\":15}" || exit /b 1
if "%CHANNEL_1%"=="1" call :tcp extract.set_statistical_filter "{\"channel\":1,\"enabled\":false}" || exit /b 1
if "%CHANNEL_2%"=="2" call :tcp extract.set_statistical_filter "{\"channel\":2,\"enabled\":false}" || exit /b 1
if /I "%FILTER%"=="raw" if "%SKIP_ROWS%"=="true" (
    if "%CHANNEL_1%"=="1" call :tcp extract.set_gate "{\"channel\":1,\"lower_ns\":0,\"upper_ns\":50}" || exit /b 1
    if "%CHANNEL_2%"=="2" call :tcp extract.set_gate "{\"channel\":2,\"lower_ns\":0,\"upper_ns\":50}" || exit /b 1
)
if /I "%FILTER%"=="tcscp" (
    if "%CHANNEL_1%"=="1" call :background 1 || exit /b 1
    if "%CHANNEL_2%"=="2" call :background 2 || exit /b 1
)
call :tcp extract.apply_all "{}" || exit /b 1
call :mark_done "%KEY%"
set /a COMPLETED_EXTRACTIONS+=1
exit /b 0

:background
call :tcp extract.set_statistical_filter "{\"channel\":%~1,\"enabled\":true}" || exit /b 1
call :tcp extract.open_filter_setup "{\"channel\":%~1}" || exit /b 1
call :tcp extract.set_background_range "{\"channel\":%~1,\"enabled\":true}" || exit /b 1
call :tcp extract.calculate_filters "{\"channel\":%~1}" || exit /b 1
call :tcp extract.accept_filters "{\"channel\":%~1}" || exit /b 1
call :tcp extract.select_filter "{\"channel\":%~1,\"name\":\"Current decay; CH %~1\"}" || exit /b 1
exit /b 0

:prepare_calculation
set "FILTER=%~1"
set "RELATIVE=%~2"
set "CALIBRATION_NAME=%~3"
set "DIRECTORY=%DATA_ROOT%\%FILTER%\%RELATIVE:/=\%"
set "OUTPUT=%DIRECTORY%\results.csv"
set "KEY=calculation:%FILTER%/%RELATIVE%/results.csv"
call :resume_has "%KEY%"
if %errorlevel% equ 0 if exist "%OUTPUT%" for %%F in ("%OUTPUT%") do if %%~zF GTR 0 (
    set /a SKIPPED_CALCULATIONS+=1
    echo RESUME: skipping %KEY%
    exit /b 2
)
set "JSON_DIRECTORY=%DIRECTORY:\=/%"
set "CALIBRATION=%DIRECTORY%\%CALIBRATION_NAME%"
set "JSON_CALIBRATION=%CALIBRATION:\=/%"
set "JSON_OUTPUT=%OUTPUT:\=/%"
call :tcp phot2conc.load_directory "{\"directory\":\"%JSON_DIRECTORY%\"}" || exit /b 1
call :tcp phot2conc.set_roi_source "{\"source\":\"none\"}" || exit /b 1
call :tcp phot2conc.load_calibration "{\"path\":\"%JSON_CALIBRATION%\"}" || exit /b 1
exit /b 0

:finish_calculation
call :tcp phot2conc.export_results "{\"path\":\"%JSON_OUTPUT%\"}" || exit /b 1
call :mark_done "%KEY%"
set /a COMPLETED_CALCULATIONS+=1
exit /b 0

:calculate_all
call :prepare_calculation "%~1" "%~2" "%~3"
if %errorlevel% equ 2 exit /b 0
if errorlevel 1 exit /b 1
if not "%~4"=="" (
    set "ROI_DIRECTORY=%DATA_ROOT%\%~4"
    set "ROI_DIRECTORY=%ROI_DIRECTORY:/=\%"
    set "JSON_ROI=%ROI_DIRECTORY:\=/%"
    call :tcp phot2conc.load_roi_directory "{\"directory\":\"%JSON_ROI%\"}" || exit /b 1
    call :tcp phot2conc.set_roi_source "{\"source\":\"file\"}" || exit /b 1
)
call :tcp phot2conc.calculate_all "{}" || exit /b 1
call :finish_calculation
exit /b %errorlevel%

:calculate_raw_mrna
call :prepare_calculation raw pie_mrna_256x256_200_frames/shared_pie_calibration calib.json
if %errorlevel% equ 2 exit /b 0
if errorlevel 1 exit /b 1
call :tcp phot2conc.set_roi_source "{\"source\":\"auto\"}" || exit /b 1
call :tcp phot2conc.select_file "{\"filename\":\"cell3-1240-cyt1-mRNA-None_200nm_4.36us_4uW.ptu\"}" || exit /b 1
call :tcp phot2conc.set_auto_roi "{\"channel\":1,\"cell_threshold\":0.1}" || exit /b 1
call :tcp phot2conc.calculate "{}" || exit /b 1
call :tcp phot2conc.add_result "{}" || exit /b 1
call :tcp phot2conc.select_file "{\"filename\":\"cell3-1910-cyt1-mRNA-None_200nm_4.36us_4uW.ptu\"}" || exit /b 1
call :tcp phot2conc.set_auto_roi "{\"channel\":1,\"cell_threshold\":0.05}" || exit /b 1
call :tcp phot2conc.calculate "{}" || exit /b 1
call :tcp phot2conc.add_result "{}" || exit /b 1
call :finish_calculation
exit /b %errorlevel%

:calculate_raw_gfp
call :prepare_calculation raw pie_gfp_256x256_200_frames/shared_pie_calibration calib.json
if %errorlevel% equ 2 exit /b 0
if errorlevel 1 exit /b 1
call :tcp phot2conc.set_roi_source "{\"source\":\"auto\"}" || exit /b 1
call :tcp phot2conc.set_auto_roi "{\"channel\":2,\"cell_threshold\":1}" || exit /b 1
call :tcp phot2conc.calculate_all "{}" || exit /b 1
call :finish_calculation
exit /b %errorlevel%

:calculate_raw_dual_new
call :prepare_calculation raw pie_dual_channel_128x128_100_frames/imaging_new_ptu calib_imaging_new_ptu.json
if %errorlevel% equ 2 exit /b 0
if errorlevel 1 exit /b 1
call :tcp phot2conc.set_roi_source "{\"source\":\"auto\"}" || exit /b 1
call :tcp phot2conc.select_file "{\"filename\":\"cell-108-01252-400nm_8.ptu\"}" || exit /b 1
call :tcp phot2conc.set_auto_roi "{\"channel\":1,\"cell_threshold\":1}" || exit /b 1
call :tcp phot2conc.set_auto_roi "{\"channel\":2,\"cell_threshold\":1}" || exit /b 1
call :tcp phot2conc.calculate "{}" || exit /b 1
call :tcp phot2conc.add_result "{}" || exit /b 1
call :finish_calculation
exit /b %errorlevel%

:calculate_raw_dual_imaging2
call :prepare_calculation raw pie_dual_channel_128x128_100_frames/imaging2_17_07_23 calib_imaging2_17_07_23.json
if %errorlevel% equ 2 exit /b 0
if errorlevel 1 exit /b 1
call :tcp phot2conc.set_roi_source "{\"source\":\"auto\"}" || exit /b 1
call :tcp phot2conc.select_file "{\"filename\":\"cell-604-02105.ptu\"}" || exit /b 1
call :tcp phot2conc.set_auto_roi "{\"channel\":2,\"cell_threshold\":1}" || exit /b 1
call :tcp phot2conc.set_auto_roi "{\"channel\":1,\"copy_from_other\":true}" || exit /b 1
call :tcp phot2conc.set_auto_roi "{\"channel\":1,\"roi_mode\":\"subtract dark\",\"object_threshold\":1.036}" || exit /b 1
call :tcp phot2conc.calculate "{}" || exit /b 1
call :tcp phot2conc.add_result "{}" || exit /b 1
call :finish_calculation
exit /b %errorlevel%

:failed
set "WORKFLOW_EXIT_CODE=%errorlevel%"
if "%WORKFLOW_EXIT_CODE%"=="0" set "WORKFLOW_EXIT_CODE=1"
set "WORKFLOW_STATUS=FAILED (exit code %WORKFLOW_EXIT_CODE%)"

:report
for /f %%T in ('"%SMICA_VENV%\Scripts\python.exe" -c "import time; print(int(time.time()))"') do set "FINISHED_TIME=%%T"
set /a ELAPSED=FINISHED_TIME-START_TIME
(
    echo smICA reference workflow report
    echo Status: %WORKFLOW_STATUS%
    echo Started: %STARTED_AT%
    echo Finished: %DATE% %TIME%
    echo Elapsed: %ELAPSED% seconds
    echo Completed extraction batches: %COMPLETED_EXTRACTIONS%
    echo Skipped extraction batches: %SKIPPED_EXTRACTIONS%
    echo Completed calculation batches: %COMPLETED_CALCULATIONS%
    echo Skipped calculation batches: %SKIPPED_CALCULATIONS%
    echo Resume state: %STATE_FILE%
    echo Host: %COMPUTERNAME%
    echo Operating system: Windows
    echo Processor: %PROCESSOR_IDENTIFIER%
    echo Logical CPUs: %NUMBER_OF_PROCESSORS%
) >"%REPORT_FILE%"
for /f "delims=" %%V in ('"%SMICA_VENV%\Scripts\python.exe" --version 2^>^&1') do echo Python: %%V>>"%REPORT_FILE%"
type "%REPORT_FILE%"
if exist "%CAPABILITIES_FILE%" del /q "%CAPABILITIES_FILE%" >nul 2>nul
call "%SMICA_VENV%\Scripts\deactivate.bat" >nul 2>nul
endlocal & exit /b %WORKFLOW_EXIT_CODE%
