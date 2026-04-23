@echo off
REM ========================================
REM Allure 安装脚本
REM ========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Allure 安装工具
echo ========================================
echo.

REM 配置
set ALLURE_VERSION=2.29.0
set ALLURE_URL=https://github.com/allure-framework/allure2/releases/download/%ALLURE_VERSION%/allure-%ALLURE_VERSION%.zip
set INSTALL_DIR=%USERPROFILE%\allure
set ZIP_FILE=%TEMP%\allure-%ALLURE_VERSION%.zip

REM 检查是否已安装
if exist "%INSTALL_DIR%\allure-%ALLURE_VERSION%\bin\allure.bat" (
    echo Allure 已安装: %INSTALL_DIR%\allure-%ALLURE_VERSION%
    echo.
    choice /C YN /M "是否重新安装"
    if errorlevel 2 (
        goto configure_path
    )
)

REM 检查 PowerShell
where powershell >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 错误: 需要 PowerShell 才能下载 Allure
    pause
    exit /b 1
)

echo 正在下载 Allure %ALLURE_VERSION%...
echo 下载地址: %ALLURE_URL%
echo.

REM 下载
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%ALLURE_URL%' -OutFile '%ZIP_FILE%' -UseBasicParsing}"

if not exist "%ZIP_FILE%" (
    echo 错误: 下载失败
    pause
    exit /b 1
)

echo.
echo 正在解压到: %INSTALL_DIR%...

REM 创建安装目录
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM 解压
powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%INSTALL_DIR%' -Force"

if not exist "%INSTALL_DIR%\allure-%ALLURE_VERSION%\bin\allure.bat" (
    echo 错误: 解压失败或文件不完整
    pause
    exit /b 1
)

REM 清理临时文件
del "%ZIP_FILE%"

echo.
echo ========================================
echo   安装成功！
echo ========================================
echo 安装路径: %INSTALL_DIR%\allure-%ALLURE_VERSION%
echo.

:configure_path
REM 配置环境变量
set ALLURE_BIN=%INSTALL_DIR%\allure-%ALLURE_VERSION%\bin
set ALLURE_PATH=%ALLURE_BIN%\allure.bat

REM 保存到项目配置文件
set CONFIG_FILE=%~dp0.allure_config.bat
echo REM Allure 配置文件 > "%CONFIG_FILE%"
echo set ALLURE_HOME=%INSTALL_DIR%\allure-%ALLURE_VERSION% >> "%CONFIG_FILE%"
echo set ALLURE_BIN=%ALLURE_BIN% >> "%CONFIG_FILE%"
echo set ALLURE_PATH=%ALLURE_PATH% >> "%CONFIG_FILE%"

echo 配置文件已创建: %CONFIG_FILE%
echo.

REM 检查 PATH 环境变量
echo ========================================
echo   配置环境变量
echo ========================================
echo.
echo 请手动将以下路径添加到系统 PATH 环境变量:
echo   %ALLURE_BIN%
echo.
echo 或者运行以下命令（当前会话有效）:
echo   set PATH=%ALLURE_BIN%;%%PATH%%
echo.

REM 尝试添加到用户 PATH
reg add "HKCU\Environment" /v PATH /t REG_EXPAND_SZ /d "%ALLURE_BIN%;%PATH%" /f >nul 2>&1

if %ERRORLEVEL% equ 0 (
    echo 已尝试自动添加到用户 PATH 环境变量
    echo 注意: 重启终端后生效
) else (
    echo 自动添加失败，请手动添加
)

echo.
echo 验证安装...
"%ALLURE_PATH%" --version

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================
    echo   Allure 安装并配置成功！
    echo ========================================
) else (
    echo.
    echo 警告: Allure 命令可能未在 PATH 中
    echo 请手动添加: %ALLURE_BIN%
)

echo.
pause