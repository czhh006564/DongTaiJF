#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API密钥迁移验证脚本
检查项目中所有硬编码API密钥是否已正确迁移到环境变量
"""

import os
import re
import glob
from typing import List, Dict, Tuple

def scan_file_for_hardcoded_keys(file_path: str) -> List[Tuple[int, str]]:
    """扫描文件中的硬编码API密钥"""
    issues = []
    
    # 要检查的模式
    patterns = [
        r'sk-[a-zA-Z0-9]{32,}',  # Dashscope API密钥格式
        r'DASHSCOPE_API_KEY\s*=\s*["\']sk-[^"\']+["\']',  # 硬编码的环境变量赋值
        r'api_key\s*=\s*["\']sk-[^"\']+["\']',  # 硬编码的api_key赋值
    ]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                matches = re.findall(pattern, line)
                if matches:
                    # 排除注释行和.env文件
                    if not line.strip().startswith('#') and not file_path.endswith('.env'):
                        issues.append((line_num, line.strip()))
                        
    except Exception as e:
        print(f"⚠️ 无法读取文件 {file_path}: {e}")
        
    return issues

def check_environment_variable_usage(file_path: str) -> bool:
    """检查文件是否正确使用环境变量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否使用了os.getenv或环境变量加载
        has_env_usage = (
            'os.getenv(' in content or 
            'load_dotenv()' in content or
            'from dotenv import' in content
        )
        
        return has_env_usage
        
    except Exception:
        return False

def main():
    print("=" * 60)
    print("🔍 API密钥迁移验证报告")
    print("=" * 60)
    
    # 扫描后端Python文件
    backend_files = glob.glob('backend/**/*.py', recursive=True)
    
    total_issues = 0
    files_with_issues = []
    files_without_env = []
    
    print("\n📂 扫描后端Python文件...")
    
    for file_path in backend_files:
        # 跳过一些特殊文件
        if any(skip in file_path for skip in ['__pycache__', '.pyc', 'venv', 'node_modules']):
            continue
            
        print(f"   检查: {file_path}")
        
        # 检查硬编码密钥
        issues = scan_file_for_hardcoded_keys(file_path)
        if issues:
            total_issues += len(issues)
            files_with_issues.append((file_path, issues))
            
        # 检查环境变量使用
        if not check_environment_variable_usage(file_path):
            # 只对包含API相关代码的文件报告
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'api_key' in content.lower() or 'dashscope' in content.lower():
                    files_without_env.append(file_path)
    
    print("\n" + "=" * 60)
    print("📊 检查结果汇总")
    print("=" * 60)
    
    if total_issues == 0:
        print("✅ 未发现硬编码API密钥问题")
    else:
        print(f"❌ 发现 {total_issues} 个硬编码API密钥问题:")
        for file_path, issues in files_with_issues:
            print(f"\n📁 {file_path}:")
            for line_num, line in issues:
                print(f"   第{line_num}行: {line}")
    
    if not files_without_env:
        print("✅ 所有相关文件都正确使用环境变量")
    else:
        print(f"\n⚠️ 以下文件可能需要添加环境变量加载:")
        for file_path in files_without_env:
            print(f"   - {file_path}")
    
    # 检查.env文件
    print(f"\n📋 环境变量配置检查:")
    if os.path.exists('backend/.env'):
        print("✅ .env 文件存在")
        with open('backend/.env', 'r', encoding='utf-8') as f:
            env_content = f.read()
            if 'DASHSCOPE_API_KEY=' in env_content:
                print("✅ DASHSCOPE_API_KEY 已配置")
            else:
                print("❌ DASHSCOPE_API_KEY 未在.env中配置")
    else:
        print("❌ .env 文件不存在")
    
    # 测试环境变量加载
    print(f"\n🧪 环境变量加载测试:")
    try:
        from dotenv import load_dotenv
        load_dotenv('backend/.env')
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if api_key and api_key != 'your-dashscope-api-key-here':
            print("✅ 环境变量加载成功，API密钥可用")
        else:
            print("⚠️ 环境变量加载成功，但API密钥未设置或为默认值")
    except ImportError:
        print("⚠️ python-dotenv 未安装，无法测试环境变量加载")
    except Exception as e:
        print(f"❌ 环境变量加载测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("💡 修复建议")
    print("=" * 60)
    
    if total_issues > 0:
        print("1. 将所有硬编码的API密钥替换为 os.getenv('DASHSCOPE_API_KEY')")
        print("2. 在文件开头添加环境变量加载代码:")
        print("   try:")
        print("       from dotenv import load_dotenv")
        print("       load_dotenv()")
        print("   except ImportError:")
        print("       pass")
    
    if files_without_env:
        print("3. 为相关文件添加环境变量支持")
    
    print("4. 确保 .env 文件包含正确的API密钥配置")
    print("5. 运行 start.bat 进行完整的AI连通性测试")
    
    print(f"\n🎯 总结: ", end="")
    if total_issues == 0 and not files_without_env:
        print("✅ API密钥迁移完成，所有文件都正确使用环境变量")
        return True
    else:
        print("⚠️ 仍有部分问题需要修复")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)