@echo off
REM ========================================
REM 运行测试套件
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

echo.
echo ========================================
echo  GST 在线问诊测试套件
echo ========================================
echo.

:menu
echo 请选择要运行的测试:
echo   1. P0 冒烟测试 (核心流程)
echo   2. P1 回归测试 (重要功能)
echo   3. P2 边缘场景测试
echo   4. 所有测试
echo   5. 仅运行测试 (不打开报告)
echo   6. 生成静态 HTML 报告
echo   0. 退出
echo.
set /p choice=请输入选项 (0-6):

if "%choice%"=="1" goto run_p0
if "%choice%"=="2" goto run_p1
if "%choice%"=="3" goto run_p2
if "%choice%"=="4" goto run_all
if "%choice%"=="5" goto run_only
if "%choice%"=="6" goto generate_html
if "%choice%"=="0" goto end

echo 无效选项，请重新选择
echo.
goto menu

:run_p0
echo.
if "%USE_ALLURE%"=="1" (
    echo 使用 Allure 运行 P0 冒烟测试...
    pytest tests/test_cases/test_online_consultation.py -m P0 --tb=short
    echo.
    echo 测试完成，正在打开 Allure 报告...
    start allure serve reports/allure
) else (
    echo 使用 pytest-html 运行 P0 冒烟测试...
    pytest tests/test_cases/test_online_consultation.py -m P0 --tb=short --html=reports/html/report.html --self-contained-html
    echo.
    echo 测试完成，正在打开报告...
    start reports/html/report.html
)
goto end

:run_p1
echo.
if "%USE_ALLURE%"=="1" (
    echo 使用 Allure 运行 P1 回归测试...
    pytest tests/test_cases/test_online_consultation.py -m P1 --tb=short
    echo.
    echo 测试完成，正在打开 Allure 报告...
    start allure serve reports/allure
) else (
    echo 使用 pytest-html 运行 P1 回归测试...
    pytest tests/test_cases/test_online_consultation.py -m P1 --tb=short --html=reports/html/report.html --self-contained-html
    echo.
    echo 测试完成，正在打开报告...
    start reports/html/report.html
)
goto end

:run_p2
echo.
if "%USE_ALLURE%"=="1" (
    echo 使用 Allure 运行 P2 边缘场景测试...
    pytest tests/test_cases/test_online_consultation.py -m P2 --tb=short
    echo.
    echo 测试完成，正在打开 Allure 报告...
    start allure serve reports/allure
) else (
    echo 使用 pytest-html 运行 P2 边缘场景测试...
    pytest tests/test_cases/test_online_consultation.py -m P2 --tb=short --html=reports/html/report.html --self-contained-html
    echo.
    echo 测试完成，正在打开报告...
    start reports/html/report.html
)
goto end

:run_all
echo.
if "%USE_ALLURE%"=="1" (
    echo 使用 Allure 运行所有测试...
    pytest tests/test_cases/test_online_consultation.py --tb=short
    echo.
    echo 测试完成，正在打开 Allure 报告...
    start allure serve reports/allure
) else (
    echo 使用 pytest-html 运行所有测试...
    pytest tests/test_cases/test_online_consultation.py --tb=short --html=reports/html/report.html --self-contained-html
    echo.
    echo 测试完成，正在打开报告...
    start reports/html/report.html
)
goto end

:run_only
echo.
echo 正在运行测试 (报告不自动打开)...
pytest tests/test_cases/test_online_consultation.py --tb=short
echo.
echo 测试完成！运行以下命令查看报告:
if "%USE_ALLURE%"=="1" (
    echo   allure serve reports/allure
) else (
    echo   allure serve reports/allure (安装 Allure 后)
    echo   或使用 pytest-html: pytest --html=reports/html/report.html --self-contained-html
)
goto end

:generate_html
echo.
if "%USE_ALLURE%"=="1" (
    echo 正在生成 Allure 静态 HTML 报告...
    allure generate reports/allure --clean -o reports/allure-html
    echo.
    echo 报告已生成到: reports/allure-html/index.html
    start reports/allure-html/index.html
) else (
    echo 正在使用 pytest-html 生成报告...
    pytest tests/test_cases/test_online_consultation.py --html=reports/html/report.html --self-contained-html
    echo.
    echo 报告已生成到: reports/html/report.html
    start reports/html/report.html
)
goto end

:end
echo.
pause