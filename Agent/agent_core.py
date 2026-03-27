from langchain_community.chat_models import ChatTongyi
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import trim_messages
from dotenv import load_dotenv

# 导入工具
from Tools.zentao_tools import create_zentao_testcase, get_testcase, update_testcase

load_dotenv()

trimmer = trim_messages(
    max_messages=3,
    strategy="last",
    token_count=len,
    include_system=True
)

llm = ChatTongyi(
    model="qwen-turbo",
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    你是专业的禅道测试用例助手。

    【功能】
    1. 创建测试用例
    2. 修改测试用例
    3. 查询测试用例

    【输出规则 · 必须严格遵守】
    1. 修改用例不需要先查询，直接根据用户指令生成新的 steps 和 expects
    2. steps 和 expects 必须是完整数组格式，数量必须一致
    3. 输出必须结构化、干净、可直接解析
    4. 禁止多余解释，只输出标准格式

    【Few-shot 示例 1：创建用例】
    用户：创建产品2登录用例
    你输出：
    标题：用户登录功能测试
    步骤：["打开页面","输入账号","点击登录"]
    预期：["页面正常","账号正确","登录成功"]

    【Few-shot 示例 2：修改用例】
    用户：修改产品2用例8步骤2为1，期望2为11
    你输出：
    标题：测试登录功能
    步骤：["打开页面","1","点击登录"]
    预期：["页面正常","11","登录成功"]
    """),
    MessagesPlaceholder("chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

tools = [create_zentao_testcase, get_testcase, update_testcase]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors="return")

agent_with_memory = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    trim_messages=trimmer
)