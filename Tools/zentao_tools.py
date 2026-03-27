from typing import List,Optional
from langchain.tools import tool
import logging
from Client.zentao_client import zentaoclient

logger = logging.getLogger("zentao-test-assistant")

def validate_test_case(title: str, steps: List[str], expects: List[str]) -> Optional[str]:
    if not title or len(title.strip()) == 0:
        return "❌ 错误：用例标题不能为空"
    if len(steps) == 0:
        return "❌ 错误：步骤列表不能为空"
    if len(expects) == 0:
        return "❌ 错误：预期列表不能为空"
    if len(steps) != len(expects):
        return f"❌ 错误：步骤数量({len(steps)})与预期数量({len(expects)})不一致"

    for i, (s, e) in enumerate(zip(steps, expects)):
        if not s or s.strip() == "":
            return f"❌ 错误：第{i + 1}条步骤为空"
        if not e or e.strip() == "":
            return f"❌ 错误：第{i + 1}条预期为空"

    if len(title) > 200:
        return "❌ 标题不能超过200字"
    for idx, s in enumerate(steps):
        if len(s) > 500:
            return f"❌ 第{idx + 1}条步骤过长"
    for idx, e in enumerate(expects):
        if len(e) > 500:
            return f"❌ 第{idx + 1}条预期过长"
    return None


# ==============================================
# 工具1：创建用例（日志 + 异常处理）
# ==============================================
@tool
def create_zentao_testcase(
        product_id: int,
        title: str,
        steps: List[str],
        expects: List[str]
) -> str:
    """【工具】创建禅道测试用例"""
    logger.info(f"开始创建用例 | product_id={product_id}, title={title}")

    error_msg = validate_test_case(title, steps, expects)
    if error_msg:
        logger.warning(f"用例校验失败：{error_msg}")
        return error_msg

    try:
        client = zentaoclient()
        client.login()
        result = client.create_testcase(product_id=product_id, title=title, steps=steps, expects=expects)
        logger.info("用例创建成功")
        return f"✅ 创建成功！用例ID：{result}"

    except Exception as e:
        logger.error(f"创建用例失败：{str(e)}")
        if "token" in str(e):
            return "❌ 登录已过期，请重启程序"
        elif "403" in str(e):
            return "❌ 权限不足，无法创建"
        elif "404" in str(e):
            return "❌ 产品ID不存在"
        else:
            return f"❌ 创建失败：{str(e)}"


# ==============================================
# 工具2：获取用例（日志 + 异常处理）
# ==============================================
@tool
def get_testcase(product_id: int, test_id: str) -> str:
    """【工具】获取单个测试用例详情"""
    logger.info(f"开始查询用例 | product_id={product_id}, test_id={test_id}")

    try:
        client = zentaoclient()
        client.login()
        case = client.get_testcase(product_id=product_id, test_id=test_id)
        if not case:
            logger.warning(f"未找到用例 {test_id}")
            return f"❌ 未找到用例 {test_id}"
        logger.info("查询用例成功")
        return f"✅ 用例详情：\n{case}"

    except Exception as e:
        logger.error(f"查询用例失败：{str(e)}")
        if "token" in str(e):
            return "❌ 登录已过期，请重启程序"
        elif "403" in str(e):
            return "❌ 权限不足"
        elif "404" in str(e):
            return "❌ 用例/产品不存在"
        else:
            return f"❌ 获取失败：{str(e)}"


# ==============================================
# 工具3：修改用例（日志 + 异常处理）
# ==============================================
@tool
def update_testcase(
        product_id: int,
        test_id: str,
        title: Optional[str] = None,
        steps: Optional[List[str]] = None,
        expects: Optional[List[str]] = None
) -> str:
    """【工具】修改禅道测试用例"""
    logger.info(f"开始修改用例 | product_id={product_id}, test_id={test_id}")

    try:
        if steps is not None or expects is not None:
            if steps is None or expects is None:
                logger.warning("修改失败：步骤/预期必须同时传")
                return "❌ 修改步骤必须同时传预期"
            if len(steps) != len(expects):
                logger.warning("步骤与预期数量不匹配")
                return f"❌ 步骤({len(steps)})与预期({len(expects)})数量不一致"

        client = zentaoclient()
        client.login()
        success = client.update_testcase(
            product_id=product_id,
            testcase_id=test_id,
            title=title,
            steps=steps,
            expects=expects
        )

        if success:
            logger.info("用例修改成功")
            return f"✅ 用例 {test_id} 修改成功！"
        else:
            logger.error("修改失败：禅道接口返回失败")
            return "❌ 修改失败：云禅道可能不支持修改"

    except Exception as e:
        logger.error(f"修改用例异常：{str(e)}")
        if "token" in str(e):
            return "❌ 登录已过期，请重启程序"
        elif "403" in str(e):
            return "❌ 权限不足"
        elif "404" in str(e):
            return "❌ 用例/产品不存在"
        else:
            return f"❌ 修改失败：{str(e)}"