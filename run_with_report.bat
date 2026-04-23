@echo off
REM ========================================
REM 运行测试并打开报告
REM ========================================

REM 加载 Allure 环境变量（如果存在）
if exist "%~dp0allure_env.bat" (
    call "%~dp0allure_env.bat"
)

REM 检查 Allure 是否可用
set USE_ALLURE=0
where allure >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set USE_ALLURE=1
)

REM 默认参数
set MARKER=
set TEST_FILE=tests/test_cases/test_online_consultation.py

REM 解析参数
if "%1"=="--p0" set MARKER=-m P0
if "%1"=="--p1" set MARKER=-m P1
if "%1"=="--p2" set MARKER=-m P2
if "%1"=="--all" set MARKER=
if "%1"=="--smoke" set MARKER=-m smoke
if "%1"=="--regression" set MARKER=-regression

if not "%MARKER%"=="" (
    if not "%2"=="" (
        set TEST_FILE=%2
    )
) else (
    if not "%1"=="" (
        set TEST_FILE=%1
    )
)

echo.
echo ========================================
echo  正在运行测试...
echo ========================================
echo 测试文件: %TEST_FILE%
if not "%MARKER%"=="" echo 标记: %MARKER%
if "%USE_ALLURE%"=="1" (
    echo 报告: Allure
) else (
    echo 报告: pytest-html
)
echo ========================================
echo.

REM 运行测试
if "%USE_ALLURE%"=="1" (
    pytest %TEST_FILE% %MARKER% --tb=short
) else (
    pytest %TEST_FILE% %MARKER% --tb=short --html=reports/html/report.html --self-contained-html
)

echo.
echo ========================================
echo  测试完成，正在打开报告...
echo ========================================
echo.

REM 生成并打开报告
if "%USE_ALLURE%"=="1" (
    start allure serve reports/allure
) else (
    start reports/html/report.html
)