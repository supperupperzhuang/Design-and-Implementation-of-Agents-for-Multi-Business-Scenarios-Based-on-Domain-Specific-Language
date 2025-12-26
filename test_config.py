# test_config.py
"""
测试配置文件
定义测试参数和用例数据
"""

TEST_CONFIG = {
    "performance": {
        "max_response_time": 5.0,  # 最大响应时间（秒）
        "concurrent_users": 10,    # 并发用户数
        "load_test_duration": 60   # 负载测试持续时间
    },
    "validation": {
        "required_fields": ["query", "response", "timestamp"],
        "response_formats": ["查询类", "问候类", "错误类"]
    },
    "test_data": {
        "sample_queries": [
            "王羲之的书法特点",
            "颜真卿的代表作品",
            "楷书的基本特征",
            "行书和草书的区别",
            "书法发展历史",
            "你好，我想了解书法",
            "请问如何学习书法"
        ],
        "edge_cases": [
            "",  # 空输入
            "   ",  # 空格
            "!@#$%",  # 特殊字符
            "a" * 1000,  # 长文本
            "书法书法书法" * 50  # 重复内容
        ]
    }
}

# 预期响应模式
EXPECTED_RESPONSE_PATTERNS = {
    "书法家查询": ["王羲之", "颜真卿", "苏轼", "柳公权", "欧阳询"],
    "作品查询": ["兰亭序", "多宝塔碑", "祭侄文稿", "黄州寒食诗帖"],
    "书体查询": ["楷书", "行书", "草书", "隶书", "篆书"]
}