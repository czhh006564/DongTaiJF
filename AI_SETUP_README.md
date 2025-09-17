# AI模型配置指南

## 概述

精准动态教辅系统现已集成AI模型连通性检查功能，确保在系统启动时验证AI服务的可用性。

## 新增功能

### 1. 自动AI连通性检查

`start.bat` 现在包含完整的AI模型连通性检查：

- ✅ 环境变量验证
- ✅ 配置文件检查  
- ✅ 网络连通性测试
- ✅ API密钥有效性验证
- ✅ 数据库AI配置检查

### 2. AI配置向导

新增 `setup_ai_config.bat` 脚本，提供交互式AI配置：

- 🔧 自动创建配置文件
- 🔑 引导配置API密钥
- 🧪 实时连通性测试
- 📖 详细配置说明

### 3. 专业检查脚本

`backend/check_ai_connectivity.py` 提供全面的AI环境检查：

- 🔍 多维度环境检查
- 🤖 支持通义千问和DeepSeek
- 📊 详细的检查报告
- 💡 智能修复建议

## 快速开始

### 方法一：使用配置向导（推荐）

```bash
# 1. 运行AI配置向导
setup_ai_config.bat

# 2. 按提示配置API密钥

# 3. 启动系统
start.bat
```

### 方法二：手动配置

```bash
# 1. 复制配置模板
cd backend
copy .env.example .env

# 2. 编辑 .env 文件，配置API密钥
notepad .env

# 3. 启动系统
cd ..
start.bat
```

## API密钥获取

### 通义千问 (推荐)

1. 访问 [阿里云灵积平台](https://dashscope.console.aliyun.com/)
2. 登录阿里云账号
3. 创建API-KEY
4. 复制密钥到 `DASHSCOPE_API_KEY`

**优势：**
- 🇨🇳 中文优化，理解更准确
- ⚡ 响应速度快
- 💰 价格相对便宜
- 🛡️ 数据安全合规

### DeepSeek (备选)

1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册/登录账号
3. 创建API密钥
4. 复制密钥到 `DEEPSEEK_API_KEY`

**优势：**
- 🧠 逻辑推理能力强
- 💻 代码生成优秀
- 🔬 数学计算精确
- 🌍 国际化支持好

## 配置文件说明

### .env 配置项

```bash
# AI模型配置
DASHSCOPE_API_KEY=sk-xxx...        # 通义千问API密钥
DEEPSEEK_API_KEY=sk-xxx...         # DeepSeek API密钥

# 模型参数
DEFAULT_AI_MODEL=tongyi            # 默认使用的模型
TONGYI_MAX_TOKENS=2000            # 通义千问最大token数
DEEPSEEK_MAX_TOKENS=2000          # DeepSeek最大token数
```

## 启动流程变化

### 原始流程 (6步)
1. 检查Python环境
2. 检查Node.js环境
3. 安装后端依赖
4. 初始化数据库
5. 安装前端依赖
6. 启动系统服务

### 新流程 (7步)
1. 检查Python环境
2. 检查Node.js环境
3. 安装后端依赖
4. 初始化数据库
5. **🆕 检查AI模型连通性**
6. 安装前端依赖
7. 启动系统服务

## 检查结果说明

### ✅ 检查通过
```
✅ AI connectivity check passed successfully
All AI features should work properly
```
- 所有AI功能正常可用
- 系统将使用真实AI响应

### ⚠️ 检查警告
```
⚠️ AI connectivity check completed with warnings
System will continue but AI features may be limited
```
- 系统可以启动但AI功能受限
- 将使用模拟响应或降级功能

## 故障排除

### 常见问题

#### 1. API密钥未配置
```
⚠️ DASHSCOPE_API_KEY 未设置
```
**解决方案：**
- 运行 `setup_ai_config.bat`
- 或手动编辑 `.env` 文件

#### 2. 网络连接问题
```
❌ 通义千问服务 网络不通
```
**解决方案：**
- 检查网络连接
- 确认防火墙设置
- 尝试使用VPN

#### 3. API密钥无效
```
❌ 通义千问API连接失败: Invalid API key
```
**解决方案：**
- 检查API密钥是否正确
- 确认API密钥是否过期
- 重新生成API密钥

### 调试模式

如需详细调试信息，可单独运行检查脚本：

```bash
cd backend
python check_ai_connectivity.py
```

## 最佳实践

### 1. 安全建议
- 🔐 不要将API密钥提交到版本控制
- 🔄 定期轮换API密钥
- 👥 不同环境使用不同密钥

### 2. 性能优化
- ⚡ 优先使用通义千问（中文场景）
- 🔄 配置多个模型作为备选
- 📊 监控API调用频率和成本

### 3. 开发建议
- 🧪 开发环境使用测试密钥
- 🚀 生产环境使用正式密钥
- 📝 记录API使用情况

## 支持的AI功能

### 当前功能
- 📝 智能题目生成
- 🔍 拍照作业批阅
- 📊 错题分析报告
- 💡 学习建议生成

### 计划功能
- 🎯 个性化学习路径
- 🗣️ 语音交互
- 📈 学习效果预测
- 🤝 智能答疑

## 更新日志

### v1.1.0 (当前版本)
- ✨ 新增AI连通性检查
- 🔧 添加配置向导
- 📖 完善配置文档
- 🛡️ 增强错误处理

### v1.0.0 (基础版本)
- 🚀 基础系统功能
- 🤖 简单AI集成
- 📱 前端界面

## 技术支持

如遇到问题，请：

1. 📖 查看本文档
2. 🔍 运行诊断脚本
3. 📝 查看错误日志
4. 💬 联系技术支持

---

**注意：** 请确保遵守各AI服务商的使用条款和数据隐私政策。