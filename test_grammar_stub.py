# test_grammar_stub.py
"""
Grammar模块测试桩
模拟DSL解析器行为
"""


class MockCalligraphyDSL:
    """模拟书法DSL解析器测试桩"""

    def __init__(self):
        self.parse_rules = {
            "查询书法家": "书法家信息检索",
            "查找作品": "作品信息检索",
            "搜索书体": "书体知识检索",
            "了解历史": "书法史检索"
        }
        self.parse_count = 0
        self.parse_history = []

    def parse(self, statement):
        """模拟DSL解析过程"""
        self.parse_count += 1
        self.parse_history.append(statement)

        # 模拟解析逻辑
        for pattern, response in self.parse_rules.items():
            if pattern in statement:
                return f"DSL解析结果: {response} - 查询条件: {statement}"

        # 默认响应
        return f"DSL解析结果: 通用查询 - 语句: {statement}"

    def simulate_parse_error(self, statement):
        """模拟解析错误"""
        raise ValueError(f"DSL语法解析错误: 无法解析语句 '{statement}'")

    def reset(self):
        """重置解析器状态"""
        self.parse_count = 0
        self.parse_history = []


class ValidatingDSL:
    """带验证的DSL测试桩"""

    def __init__(self):
        self.valid_prefixes = ['查询', '查找', '搜索', '了解', '显示', '展示']

    def parse(self, statement):
        """带验证的解析方法"""
        if not any(statement.startswith(prefix) for prefix in self.valid_prefixes):
            raise ValueError(f"无效的查询前缀: {statement}")

        return f"验证通过: {statement}"