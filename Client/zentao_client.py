from dotenv import load_dotenv
import requests
import os
load_dotenv()

class zentaoclient():
    def __init__(self):
        self.base_url = os.getenv("ZENTAO_URL")
        self.account = os.getenv("ZENTAO_ACCOUNT")
        self.password = os.getenv("ZENTAO_PASSWORD")
        self.token = None

    def login(self):
        # ✅ 匹配你截图里的接口地址 /tokens
        url = f"{self.base_url}/tokens"
        payload = {
            "account": self.account,
            "password": self.password
        }
        headers = {"Content-Type": "application/json"}
        try:
            r = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10,
            )
            data = r.json()

            if data.get("token"):
                self.token = data.get("token")
                print("✅ 登录成功！token =", self.token)
                return self.token
            else:
                raise RuntimeError(f"登录失败，未获取到token：{data}")

        except Exception as e:
            raise RuntimeError(f"请求失败：{e}")

    def get_token(self):
        if not self.token:
            return self.login()
        return self.token

    def create_testcase(self, product_id, title, steps, expects, pri=3, case_type="feature"):
        """
        创建禅道测试用例
        :param product_id: 产品ID（会拼到URL里）
        :param title: 用例标题
        :param steps: 步骤列表，如 ["输入用户名", "点击登录"]
        :param expects: 期望列表，如 ["用户名正确", "登录成功"]
        :param pri: 优先级
        :param case_type: 用例类型
        :return: 用例ID
        """
        if len(steps) != len(expects):
            raise ValueError("steps和expects数量必须一致！")
        if not title.strip():
            raise ValueError("用例标题不能为空！")

        url = f"{self.base_url}/products/{product_id}/testcases"

        # ✅ 步骤格式必须是对象数组：[{desc: "步骤1", expect: "期望1"}, ...]
        step_list = []
        for step_desc, step_expect in zip(steps, expects):
            step_list.append({
                "desc": step_desc,
                "expect": step_expect
            })

        payload = {
            "title": title,
            "type": case_type,
            "pri": pri,
            "steps": step_list
        }

        headers = {
            "Token": self.token
        }

        r = requests.post(url, json=payload, headers=headers)
        data = r.json()

        if "id" in data:
            return data["id"]

        error_msg = data.get("error") or data.get("message") or str(data)
        raise Exception(f"创建用例失败：{error_msg}")

    def get_testcase(self, product_id, test_id):

        url = f"{self.base_url}/testcases/{test_id}"
        headers = {"Token": self.token}
        r = requests.get(url, headers=headers)
        data = r.json()

        if "error" in data:
            return None

        return data

    def update_testcase(self, product_id, testcase_id, title=None, steps=None, expects=None, pri=None, module=None):
        """
        【修复版】修改测试用例（适配云禅道免费版）
        注意：云禅道免费版修改接口可能不支持，建议先测试
        """
        payload = {}

        if title:
            payload["title"] = title

        # 2. 处理步骤（必须合并成对象数组）
        if steps is not None and expects is not None:
            if len(steps) != len(expects):
                raise ValueError("steps和expects数量必须一致！")

            step_list = []
            for step_desc, step_expect in zip(steps, expects):
                step_list.append({
                    "desc": step_desc,
                    "expect": step_expect
                })
            payload["steps"] = step_list

        if pri:
            payload["pri"] = pri

        if module:
            payload["module"] = module

        if not payload:
            raise ValueError("没有要修改的内容！")

        url = f"{self.base_url}/testcases/{testcase_id}"

        headers = {"Token": self.token}

        r = requests.put(url, json=payload, headers=headers)
        data = r.json()

        if "error" not in data:
            return True

        raise ValueError(f"修改失败：{data.get('error', '未知错误')}")

    def get_product_list(self):
        url=f"{self.base_url}/products"
        headers={"Token":self.token}
        r=requests.get(url,headers=headers)
        data=r.json()
        products=[]

        for p in data["products"]:
            products.append({
                "name":p["name"],
                "id":p["id"]
            })
        return products

    def choose_products(self):
        # 获取产品列表
        products = self.get_product_list()

        if not products:
            print("没有找到任何产品！")
            return None

        print("请选择产品：")
        for i, product in enumerate(products):
            # 这里是关键！！！
            print(f"{i + 1}. {product['name']} (ID:{product['id']})")

        # 让用户输入
        choice = int(input("请输入产品序号：")) - 1
        return products[choice]["id"]