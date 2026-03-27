import logging
from Agent.agent_core import agent_with_memory

# ======================
# 全局唯一日志配置
# ======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("zentao-test-assistant.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("zentao-test-assistant")

# ======================
# 主程序入口
# ======================
if __name__ == "__main__":
    print("=== zentao-test-assistant 禅道测试用例智能助手 ===")

    # 引导输入产品ID
    while True:
        pid = input("请输入产品ID：").strip()
        if pid.isdigit():
            PRODUCT_ID = int(pid)
            logger.info(f"用户选择产品ID：{PRODUCT_ID}")
            break
        print("❌ 必须输入数字，请重试")

    print(f"✅ 当前产品ID：{PRODUCT_ID}")
    print("输入 '退出' 结束对话\n")

    # 主对话循环
    while True:
        user_input = input("你：").strip()
        if not user_input:
            continue

        if user_input.lower() in ["退出", "quit", "exit"]:
            logger.info("用户退出程序")
            print("👋 再见！")
            break

        # 创建用例二次确认
        if "创建" in user_input or "新建" in user_input:
            confirm = input("⚠️ 确认创建测试用例？(y/n)：")
            if confirm.lower() != "y":
                print("✅ 已取消创建")
                continue

        # 执行AI请求
        try:
            response = agent_with_memory.invoke(
                {"input": f"产品ID={PRODUCT_ID}，{user_input}"},
                config={"configurable": {"session_id": "demo"}}
            )
            print("AI 回复：", response["output"])

        except Exception as e:
            logger.error(f"系统异常：{str(e)}")
            print(f"❌ 程序异常：{str(e)}")