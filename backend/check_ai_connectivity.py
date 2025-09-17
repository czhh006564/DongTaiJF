#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI模型连通性检查脚本
用于在系统启动时验证AI服务的可用性
"""

import os
import sys
import asyncio
import aiohttp
from typing import Dict, Any
import json

# 加载环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv 未安装，尝试从系统环境变量读取配置")

def check_environment_variables():
    """检查必要的环境变量"""
    print("🔍 检查环境变量配置...")
    
    required_vars = {
        'DASHSCOPE_API_KEY': '通义千问API密钥',
        'DEEPSEEK_API_KEY': 'DeepSeek API密钥'
    }
    
    missing_vars = []
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if not value:
            print(f"⚠️  {var} 未设置 ({desc})")
            missing_vars.append(var)
        elif value.startswith('your-') or value == 'your_api_key_here':
            print(f"⚠️  {var} 使用默认占位符，需要配置真实密钥")
            missing_vars.append(var)
        else:
            print(f"✅ {var} 已配置")
    
    return missing_vars

def check_config_files():
    """检查配置文件"""
    print("\n📁 检查配置文件...")
    
    config_files = [
        ('.env', '环境变量配置文件'),
        ('.env.example', '环境变量示例文件'),
    ]
    
    for file_path, desc in config_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在 ({desc})")
        else:
            print(f"⚠️  {file_path} 不存在 ({desc})")

async def test_tongyi_api():
    """测试通义千问API连通性"""
    print("\n🤖 测试通义千问API连通性...")
    
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key or api_key.startswith('your-'):
        print("❌ 通义千问API密钥未配置，跳过连通性测试")
        return False
    
    try:
        # 使用Dashscope SDK测试
        import dashscope
        from http import HTTPStatus
        
        dashscope.api_key = api_key
        
        # 简单的文本生成测试
        response = dashscope.Generation.call(
            model='qwen-turbo',
            prompt='测试连接',
            max_tokens=10
        )
        
        if response.status_code == HTTPStatus.OK:
            print("✅ 通义千问API连接成功")
            return True
        else:
            print(f"❌ 通义千问API连接失败: {response.message}")
            return False
            
    except ImportError:
        print("⚠️  dashscope库未安装，跳过API测试")
        return False
    except Exception as e:
        print(f"❌ 通义千问API测试异常: {str(e)}")
        return False

async def test_deepseek_api():
    """测试DeepSeek API连通性"""
    print("\n🧠 测试DeepSeek API连通性...")
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key or api_key.startswith('your-'):
        print("❌ DeepSeek API密钥未配置，跳过连通性测试")
        return False
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "测试连接"}],
                "max_tokens": 10
            }
            
            async with session.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    print("✅ DeepSeek API连接成功")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ DeepSeek API连接失败: HTTP {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ DeepSeek API测试异常: {str(e)}")
        return False

def check_database_ai_config():
    """检查数据库中的AI配置"""
    print("\n💾 检查数据库AI配置...")
    
    try:
        from models.database import SessionLocal
        from models.config import AIModelConfig
        
        db = SessionLocal()
        try:
            # 检查是否有AI模型配置
            configs = db.query(AIModelConfig).all()
            if configs:
                print(f"✅ 数据库中找到 {len(configs)} 个AI模型配置")
                for config in configs:
                    status = "启用" if config.is_active else "禁用"
                    default = " (默认)" if config.is_default else ""
                    print(f"   - {config.display_name}: {status}{default}")
            else:
                print("⚠️  数据库中未找到AI模型配置")
                print("   系统将使用默认配置")
        finally:
            db.close()
            
    except ImportError:
        print("⚠️  无法导入数据库模型，跳过数据库检查")
    except Exception as e:
        print(f"❌ 数据库AI配置检查失败: {str(e)}")

def check_network_connectivity():
    """检查网络连通性"""
    print("\n🌐 检查网络连通性...")
    
    import socket
    
    test_hosts = [
        ('dashscope.aliyuncs.com', 443, '通义千问服务'),
        ('api.deepseek.com', 443, 'DeepSeek服务'),
    ]
    
    for host, port, desc in test_hosts:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            print(f"✅ {desc} 网络连通")
        except Exception as e:
            print(f"❌ {desc} 网络不通: {str(e)}")

async def main():
    """主检查函数"""
    print("=" * 50)
    print("🚀 AI模型连通性检查开始")
    print("=" * 50)
    
    # 1. 检查环境变量
    missing_vars = check_environment_variables()
    
    # 2. 检查配置文件
    check_config_files()
    
    # 3. 检查网络连通性
    check_network_connectivity()
    
    # 4. 检查数据库配置
    check_database_ai_config()
    
    # 5. 测试API连通性
    tongyi_ok = await test_tongyi_api()
    deepseek_ok = await test_deepseek_api()
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 检查结果总结")
    print("=" * 50)
    
    if missing_vars:
        print("⚠️  环境变量配置不完整:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 建议:")
        print("   1. 复制 .env.example 为 .env")
        print("   2. 在 .env 中配置真实的API密钥")
        print("   3. 重新运行此检查脚本")
    
    api_status = []
    if tongyi_ok:
        api_status.append("通义千问")
    if deepseek_ok:
        api_status.append("DeepSeek")
    
    if api_status:
        print(f"✅ 可用的AI服务: {', '.join(api_status)}")
    else:
        print("⚠️  所有AI服务均不可用")
        print("   系统将使用模拟响应模式")
    
    print("\n🎯 系统启动建议:")
    if not missing_vars and (tongyi_ok or deepseek_ok):
        print("   ✅ AI环境配置良好，可以正常使用AI功能")
    elif missing_vars:
        print("   ⚠️  请先配置API密钥，否则AI功能将受限")
    else:
        print("   ⚠️  AI服务连接异常，请检查网络和密钥配置")
    
    print("\n" + "=" * 50)
    return len(missing_vars) == 0 and (tongyi_ok or deepseek_ok)

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n❌ 检查被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 检查过程发生异常: {str(e)}")
        sys.exit(1)