#!/usr/bin/env python3
"""
创建超级管理员账号的脚本
"""

import sys
import os

# 添加backend目录到Python路径
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from database.database import get_db, engine
from database.models import User
from utils.security import get_password_hash
from sqlalchemy.orm import Session

def create_super_admin():
    """创建超级管理员账号"""
    
    # 创建数据库会话
    db = next(get_db())
    
    try:
        # 检查是否已存在超级管理员
        existing_admin = db.query(User).filter(User.role == "super_admin").first()
        if existing_admin:
            print(f"超级管理员已存在: {existing_admin.username}")
            return existing_admin
        
        # 创建超级管理员账号
        admin_data = {
            "username": "admin",
            "email": "admin@example.com",
            "real_name": "系统管理员",
            "password": "admin123",  # 默认密码
            "role": "super_admin"
        }
        
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == admin_data["username"]).first()
        if existing_user:
            # 如果用户存在但不是超级管理员，更新其角色
            existing_user.role = "super_admin"
            existing_user.real_name = admin_data["real_name"]
            db.commit()
            print(f"已将用户 {admin_data['username']} 升级为超级管理员")
            return existing_user
        
        # 创建新的超级管理员用户
        hashed_password = get_password_hash(admin_data["password"])
        
        admin_user = User(
            username=admin_data["username"],
            email=admin_data["email"],
            real_name=admin_data["real_name"],
            hashed_password=hashed_password,
            role=admin_data["role"],
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ 超级管理员账号创建成功！")
        print(f"用户名: {admin_data['username']}")
        print(f"密码: {admin_data['password']}")
        print(f"角色: {admin_data['role']}")
        print(f"真实姓名: {admin_data['real_name']}")
        print("\n请使用以上信息登录系统")
        
        return admin_user
        
    except Exception as e:
        db.rollback()
        print(f"❌ 创建超级管理员失败: {str(e)}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("正在创建超级管理员账号...")
    create_super_admin()