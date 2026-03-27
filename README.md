# 禅道测试用例智能助手（zentao-test-assistant）

## 项目简介
基于 LangChain + 通义千问 + 禅道 API 开发的智能测试用例助手，支持自然语言创建、查询、修改禅道测试用例，实现对话式用例管理，具备记忆、校验、异常处理、日志记录等完整工程能力。

## 功能特性
- ✅ 自然语言创建测试用例
- ✅ 自然语言修改测试用例（支持局部修改）
- ✅ 查询测试用例详情
- ✅ 对话记忆功能
- ✅ 完善的异常处理与日志
- ✅ 交互确认机制
- ✅ 用例格式强校验
- ✅ 产品ID引导输入

## 技术栈
- LangChain（Agent、Tools、Memory）
- 通义千问（Qwen-Turbo）
- 禅道 API
- Python
- logging 日志系统
- dotenv 环境配置

## 项目结构
```
zentao-test-assistant/
├── Client/
│   └── zentao_client.py    # 禅道 API 客户端封装
├── Tools/
│   └── zentao_tools.py     # LangChain 工具与校验逻辑
├── Agent/
│   └── agent_core.py       # Agent、Prompt、LLM 配置
├── main.py                 # 程序入口
├── .env                    # 环境变量配置
├── .gitignore              # Git 忽略文件
├── requirements.txt        # 依赖清单
└── README.md               # 项目说明
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 .env 文件
```plaintext
ZENTAO_URL=http://你的禅道地址/api/v1
ZENTAO_ACCOUNT=禅道账号
ZENTAO_PASSWORD=禅道密码
DASHSCOPE_API_KEY=通义千问API Key
```

### 3. 启动项目
```bash
python main.py
```

## 演示流程
1. 输入产品ID
2. 创建登录测试用例
3. 修改用例步骤/预期
4. 查询用例详情
5. 退出程序

## 项目说明
- 日志文件：zentao-test-assistant.log
- 支持对话记忆，可直接修改上一条用例
- 所有接口异常统一捕获，程序稳定不崩溃
- 代码模块化拆分，易于维护与扩展




