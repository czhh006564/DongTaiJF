@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo AI配置向导 - 精准动态教辅系统
echo ========================================

echo.
echo 此向导将帮助您配置AI模型API密钥
echo.

cd backend

echo [1/4] 检查配置文件...
if exist ".env" (
    echo ✅ 发现现有 .env 配置文件
    echo.
    choice /c YN /m "是否要重新配置 (Y/N)"
    if errorlevel 2 goto :skip_copy
)

echo 📋 复制配置模板...
if exist ".env.example" (
    copy ".env.example" ".env" >nul
    echo ✅ 已创建 .env 配置文件
) else (
    echo ❌ 未找到 .env.example 模板文件
    pause
    exit /b 1
)

:skip_copy
echo.
echo [2/4] 配置通义千问API密钥...
echo.
echo 📖 获取通义千问API密钥:
echo    1. 访问: https://dashscope.console.aliyun.com/
echo    2. 登录阿里云账号
echo    3. 创建API-KEY
echo    4. 复制API密钥
echo.
set /p "tongyi_key=请输入通义千问API密钥 (留空跳过): "

if not "%tongyi_key%"=="" (
    echo 🔧 配置通义千问API密钥...
    powershell -Command "(Get-Content .env) -replace 'DASHSCOPE_API_KEY=.*', 'DASHSCOPE_API_KEY=%tongyi_key%' | Set-Content .env"
    echo ✅ 通义千问API密钥已配置
) else (
    echo ⏭️ 跳过通义千问配置
)

echo.
echo [3/4] 配置DeepSeek API密钥...
echo.
echo 📖 获取DeepSeek API密钥:
echo    1. 访问: https://platform.deepseek.com/
echo    2. 注册/登录账号
echo    3. 创建API密钥
echo    4. 复制API密钥
echo.
set /p "deepseek_key=请输入DeepSeek API密钥 (留空跳过): "

if not "%deepseek_key%"=="" (
    echo 🔧 配置DeepSeek API密钥...
    powershell -Command "(Get-Content .env) -replace 'DEEPSEEK_API_KEY=.*', 'DEEPSEEK_API_KEY=%deepseek_key%' | Set-Content .env"
    echo ✅ DeepSeek API密钥已配置
) else (
    echo ⏭️ 跳过DeepSeek配置
)

echo.
echo [4/4] 测试AI连接...
echo.
echo 🧪 运行AI连通性测试...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python check_ai_connectivity.py
    if errorlevel 1 (
        echo.
        echo ⚠️ AI连接测试发现问题
        echo 请检查API密钥是否正确配置
    ) else (
        echo.
        echo ✅ AI连接测试通过
    )
) else (
    echo ⚠️ Python虚拟环境未找到
    echo 请先运行 start.bat 初始化环境
)

echo.
echo ========================================
echo 配置完成!
echo ========================================
echo.
echo 📁 配置文件位置: backend\.env
echo 🔧 如需修改配置，可直接编辑该文件
echo 🚀 现在可以运行 start.bat 启动系统
echo.
echo 💡 提示:
echo    - 通义千问适合中文场景，响应速度快
echo    - DeepSeek适合代码和逻辑推理
echo    - 建议至少配置一个API密钥
echo.
pause