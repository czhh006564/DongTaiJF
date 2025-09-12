#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🚀 启动调试版后端服务...")
print(f"📁 工作目录: {current_dir}")
print(f"🐍 Python版本: {sys.version}")

try:
    # 导入调试应用
    from debug_app import app
    print("✅ 调试应用导入成功")
    
    # 启动服务器
    print("🌐 启动FastAPI服务器在 http://localhost:8000")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=False,
        log_level="info"
    )
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保所有依赖已安装: pip install fastapi uvicorn httpx")
    
except Exception as e:
    print(f"❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()