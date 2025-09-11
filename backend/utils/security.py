# 安全相关工具函数
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from cryptography.fernet import Fernet
import os
import base64

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """解码访问令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

# API密钥加密相关
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", SECRET_KEY)

def get_encryption_key() -> bytes:
    """获取加密密钥"""
    # 使用SECRET_KEY生成固定的加密密钥
    key = base64.urlsafe_b64encode(ENCRYPTION_KEY.encode()[:32].ljust(32, b'0'))
    return key

def encrypt_api_key(api_key: str) -> str:
    """加密API密钥"""
    if not api_key or api_key.startswith("your-"):
        return api_key  # 不加密占位符
    
    try:
        f = Fernet(get_encryption_key())
        encrypted = f.encrypt(api_key.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception:
        return api_key  # 加密失败时返回原值

def decrypt_api_key(encrypted_api_key: str) -> str:
    """解密API密钥"""
    if not encrypted_api_key or encrypted_api_key.startswith("your-"):
        return encrypted_api_key  # 不解密占位符
    
    try:
        f = Fernet(get_encryption_key())
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_api_key.encode())
        decrypted = f.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception:
        return encrypted_api_key  # 解密失败时返回原值