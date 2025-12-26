# test_llm_stub.py
"""
LLM模块测试桩
模拟大语言模型API调用，避免真实API调用成本
"""


class MockLLM:
    """模拟LLM响应测试桩"""

    def __init__(self):
        self.response_patterns = {
            # 书法家查询模式
            "书法家": [
                "查询书法家王羲之的生平事迹和艺术成就",
                "查找颜真卿的书法作品和风格特点",
                "搜索苏轼在书法史上的地位和影响"
            ],
            # 作品查询模式
            "作品": [
                "查询《兰亭序》的创作背景和艺术价值",
                "查找《多宝塔碑》的书法特点和历史意义",
                "搜索《黄州寒食诗帖》的鉴赏要点"
            ],
            # 书体风格查询模式
            "书体": [
                "查询楷书的基本特征和代表书法家",
                "查找行书与草书的区别和联系",
                "搜索篆书的发展历程和艺术特色"
            ],
            # 问候语句模式
            "问候": [
                "您好！我是书法咨询助手，请问有什么可以帮您？",
                "欢迎使用书法专业咨询系统，请提出您的问题。",
                "您好，我可以帮助您查询书法相关的知识。"
            ]
        }
        self.call_count = 0
        self.call_history = []

    def deepseekchat(self, query):
        """模拟LLM API调用"""
        self.call_count += 1
        self.call_history.append(query)

        # 根据查询内容模式匹配返回相应的响应
        if any(keyword in query for keyword in ["你好", "您好", "hello", "hi"]):
            return self.response_patterns["问候"][self.call_count % len(self.response_patterns["问候"])]
        elif any(keyword in query for keyword in ["书法家", "书家", "书法大师"]):
            return self.response_patterns["书法家"][self.call_count % len(self.response_patterns["书法家"])]
        elif any(keyword in query for keyword in ["作品", "字帖", "碑文"]):
            return self.response_patterns["作品"][self.call_count % len(self.response_patterns["作品"])]
        elif any(keyword in query for keyword in ["书体", "字体", "楷书", "行书", "草书"]):
            return self.response_patterns["书体"][self.call_count % len(self.response_patterns["书体"])]
        else:
            return "查询书法相关的知识信息"

    def reset(self):
        """重置测试桩状态"""
        self.call_count = 0
        self.call_history = []


class ErrorProneLLM:
    """异常测试桩 - 模拟各种错误情况"""

    def __init__(self, error_type="timeout", error_rate=0.3):
        self.error_type = error_type
        self.error_rate = error_rate
        self.call_count = 0

    def deepseekchat(self, query):
        """模拟异常情况的LLM调用"""
        self.call_count += 1

        if self.call_count / 10 < self.error_rate:  # 模拟错误率
            if self.error_type == "timeout":
                raise TimeoutError("LLM API请求超时")
            elif self.error_type == "network":
                raise ConnectionError("网络连接错误")
            elif self.error_type == "invalid_response":
                return ""  # 空响应
            else:
                raise Exception("未知错误")

        # 正常响应
        return f"查询{query}的相关信息"