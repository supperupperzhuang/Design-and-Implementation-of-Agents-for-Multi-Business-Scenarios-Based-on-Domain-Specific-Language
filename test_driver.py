# test_driver.py
"""
测试驱动框架
提供完整的测试用例管理和执行功能
"""

import unittest
import time
import json
from datetime import datetime
from typing import List, Tuple, Dict, Any


class CalligraphySystemTestDriver:
    """书法系统测试驱动类"""

    def __init__(self):
        self.test_cases = []
        self.test_results = []
        self.start_time = None
        self.end_time = None

    def load_test_cases_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """从文件加载测试用例"""
        test_cases = []

        # 模拟测试用例数据
        sample_cases = [
            {
                "id": 1,
                "description": "书法家查询测试",
                "input": "王羲之的书法特点是什么？",
                "expected_type": "查询类",
                "should_pass": True
            },
            {
                "id": 2,
                "description": "作品查询测试",
                "input": "《兰亭序》的创作背景",
                "expected_type": "查询类",
                "should_pass": True
            },
            {
                "id": 3,
                "description": "问候语句测试",
                "input": "你好，请介绍书法知识",
                "expected_type": "问候类",
                "should_pass": True
            },
            {
                "id": 4,
                "description": "空输入测试",
                "input": "",
                "expected_type": "错误类",
                "should_pass": False
            }
        ]

        self.test_cases = sample_cases
        return self.test_cases

    def execute_single_test(self, test_case: Dict[str, Any],
                            llm_stub, dsl_stub) -> Dict[str, Any]:
        """执行单个测试用例"""
        test_result = {
            "id": test_case["id"],
            "description": test_case["description"],
            "input": test_case["input"],
            "status": "未执行",
            "result": None,
            "execution_time": 0,
            "error": None
        }

        start_time = time.time()

        try:
            # 模拟系统处理流程
            llm_response = llm_stub.deepseekchat(test_case["input"])

            # 判断响应类型
            if llm_response.startswith(('查询', '查找', '搜索', '找', '请问', '我想知道', '了解', '显示', '展示')):
                dsl_result = dsl_stub.parse(llm_response)
                test_result["result"] = {
                    "llm_response": llm_response,
                    "dsl_result": dsl_result,
                    "type": "查询类"
                }
            else:
                test_result["result"] = {
                    "llm_response": llm_response,
                    "dsl_result": "N/A",
                    "type": "问候类"
                }

            test_result["status"] = "通过" if test_case["should_pass"] else "失败"

        except Exception as e:
            test_result["status"] = "错误"
            test_result["error"] = str(e)

        test_result["execution_time"] = time.time() - start_time
        return test_result

    def run_test_suite(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """运行完整测试套件"""
        self.start_time = time.time()
        self.test_results = []

        # 初始化测试桩
        llm_stub = MockLLM()
        dsl_stub = MockCalligraphyDSL()

        print("=" * 60)
        print("书法系统测试套件执行开始")
        print("=" * 60)

        for test_case in test_cases:
            result = self.execute_single_test(test_case, llm_stub, dsl_stub)
            self.test_results.append(result)

            # 实时输出测试结果
            status_icon = "✅" if result["status"] == "通过" else "❌"
            print(f"{status_icon} 测试用例 {result['id']}: {result['description']}")
            print(f"   输入: {result['input']}")
            print(f"   状态: {result['status']} (耗时: {result['execution_time']:.3f}s)")
            if result["error"]:
                print(f"   错误: {result['error']}")
            print()

        self.end_time = time.time()
        return self.generate_test_report()

    def generate_test_report(self) -> Dict[str, Any]:
        """生成详细测试报告"""
        total_cases = len(self.test_results)
        passed_cases = len([r for r in self.test_results if r["status"] == "通过"])
        failed_cases = len([r for r in self.test_results if r["status"] == "失败"])
        error_cases = len([r for r in self.test_results if r["status"] == "错误"])

        total_time = self.end_time - self.start_time
        avg_time = total_time / total_cases if total_cases > 0 else 0

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_cases": total_cases,
                "passed": passed_cases,
                "failed": failed_cases,
                "errors": error_cases,
                "pass_rate": (passed_cases / total_cases * 100) if total_cases > 0 else 0,
                "total_execution_time": total_time,
                "average_execution_time": avg_time
            },
            "detailed_results": self.test_results,
            "llm_usage_stats": {
                "total_calls": total_cases,
                "average_response_time": avg_time
            }
        }

        return report

    def save_report_to_file(self, report: Dict[str, Any], file_path: str):
        """保存测试报告到文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"测试报告已保存到: {file_path}")


class AutomatedTestRunner:
    """自动化测试运行器"""

    @staticmethod
    def run_comprehensive_tests():
        """运行全面测试套件"""
        test_driver = CalligraphySystemTestDriver()

        # 加载测试用例
        test_cases = test_driver.load_test_cases_from_file("test_cases.json")

        # 运行测试
        report = test_driver.run_test_suite(test_cases)

        # 生成报告
        print("=" * 60)
        print("测试执行完成")
        print("=" * 60)
        print(f"总计用例: {report['summary']['total_cases']}")
        print(f"通过: {report['summary']['passed']}")
        print(f"失败: {report['summary']['failed']}")
        print(f"错误: {report['summary']['errors']}")
        print(f"通过率: {report['summary']['pass_rate']:.1f}%")
        print(f"总耗时: {report['summary']['total_execution_time']:.2f}秒")

        # 保存详细报告
        test_driver.save_report_to_file(report, "test_report.json")

        return report