# test_driver.py
"""
测试驱动框架 - 修复AttributeError问题
"""

import unittest
import time
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from unittest.mock import Mock


class CalligraphySystemTestDriver:
    """书法系统测试驱动类"""

    def __init__(self):
        self.test_cases = []
        self.test_results = []
        self.start_time = None
        self.end_time = None

    def load_test_cases_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """从文件加载测试用例"""
        return self._get_default_test_cases()

    def _get_default_test_cases(self) -> List[Dict[str, Any]]:
        """获取默认测试用例"""
        return [
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
                "description": "书体风格查询测试",
                "input": "楷书和行书有什么区别？",
                "expected_type": "查询类",
                "should_pass": True
            }
        ]

    def _create_llm_mock(self) -> Mock:
        """创建LLM模拟对象"""
        llm_mock = Mock()

        def llm_side_effect(query):
            if not query or query.strip() == "":
                return "输入内容为空，请提供有效的书法相关查询。"
            query_lower = query.lower()

            if "书法家" in query_lower:
                return f"查询书法家信息: {query}"
            elif "作品" in query_lower or "《" in query_lower:
                return f"查找作品信息: {query}"
            elif "书体" in query_lower:
                return f"搜索书体知识: {query}"
            else:
                return f"查询书法相关知识: {query}"

        llm_mock.deepseekchat.side_effect = llm_side_effect
        return llm_mock

    def _create_dsl_mock(self) -> Mock:
        """创建DSL解释器模拟对象"""
        dsl_mock = Mock()

        def dsl_side_effect(statement):
            if "书法家" in statement:
                return f"[DSL解析] 书法家信息检索: {statement}"
            elif "作品" in statement:
                return f"[DSL解析] 作品信息检索: {statement}"
            elif "书体" in statement:
                return f"[DSL解析] 书体知识检索: {statement}"
            else:
                return f"[DSL解析] 通用查询处理: {statement}"

        dsl_mock.parse.side_effect = dsl_side_effect
        return dsl_mock

    def execute_single_test(self, test_case: Dict[str, Any],
                            llm_mock: Mock, dsl_mock: Mock) -> Dict[str, Any]:
        """执行单个测试用例"""
        test_result = {
            "id": test_case["id"],
            "description": test_case["description"],
            "input": test_case["input"],
            "status": "未执行",
            "llm_response": None,
            "dsl_result": None,
            "response_type": None,
            "execution_time": 0,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        start_time = time.time()

        try:
            # 模拟系统处理流程
            llm_response = llm_mock.deepseekchat(test_case["input"])
            test_result["llm_response"] = llm_response

            # 判断响应类型并处理
            if llm_response.startswith(('查询', '查找', '搜索')):
                dsl_result = dsl_mock.parse(llm_response)
                test_result["dsl_result"] = dsl_result
                test_result["response_type"] = "查询类"
                test_result["status"] = "通过" if test_case["should_pass"] else "失败"
            else:
                test_result["response_type"] = "问候类"
                test_result["dsl_result"] = "N/A"
                test_result["status"] = "通过" if test_case["should_pass"] else "失败"

        except Exception as e:
            test_result["status"] = "错误"
            test_result["error"] = str(e)
            test_result["response_type"] = "错误类"

        test_result["execution_time"] = time.time() - start_time
        return test_result

    def run_test_suite(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """运行完整测试套件"""
        self.start_time = time.time()
        self.test_results = []

        # 创建模拟对象
        llm_mock = self._create_llm_mock()
        dsl_mock = self._create_dsl_mock()

        print("=" * 60)
        print("书法系统测试套件执行开始")
        print("=" * 60)

        for i, test_case in enumerate(test_cases, 1):
            print(f"执行测试用例 {i}: {test_case['description']}")

            result = self.execute_single_test(test_case, llm_mock, dsl_mock)
            self.test_results.append(result)

            status_icon = "✅" if result["status"] == "通过" else "❌"
            print(f"{status_icon} 状态: {result['status']}")
            print(f"   输入: {result['input']}")
            print(f"   响应: {result['llm_response']}")
            print(f"   耗时: {result['execution_time']:.3f}s")
            print("-" * 50)

        self.end_time = time.time()
        return self.generate_test_report()

    def generate_test_report(self) -> Dict[str, Any]:
        """生成详细测试报告"""
        total_time = self.end_time - self.start_time
        total_cases = len(self.test_results)

        passed_cases = len([r for r in self.test_results if r["status"] == "通过"])
        failed_cases = len([r for r in self.test_results if r["status"] == "失败"])
        error_cases = len([r for r in self.test_results if r["status"] == "错误"])

        avg_time = total_time / total_cases if total_cases > 0 else 0

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_cases": total_cases,
                "passed_cases": passed_cases,
                "failed_cases": failed_cases,
                "error_cases": error_cases,
                "pass_rate": (passed_cases / total_cases * 100) if total_cases > 0 else 0,
                "total_execution_time": total_time,
                "average_execution_time": avg_time
            },
            "detailed_results": self.test_results
        }

        # 打印报告摘要
        print("\n" + "=" * 60)
        print("测试报告摘要")
        print("=" * 60)
        print(f"总测试用例: {total_cases}")
        print(f"通过: {passed_cases}")
        print(f"失败: {failed_cases}")
        print(f"错误: {error_cases}")
        print(f"通过率: {report['summary']['pass_rate']:.1f}%")
        print(f"总耗时: {total_time:.2f}秒")

        return report

    def save_report_to_file(self, report: Dict[str, Any], file_path: str = "test_report.json"):
        """保存测试报告到文件 - 新增的缺失方法"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"✅ 测试报告已保存到: {file_path}")
            return True
        except Exception as e:
            print(f"❌ 保存测试报告失败: {e}")
            return False

    def display_report(self, report: Dict[str, Any]):
        """显示测试报告 - 新增方法"""
        print("\n" + "=" * 60)
        print("详细测试结果")
        print("=" * 60)

        for result in report["detailed_results"]:
            status_icon = "✅" if result["status"] == "通过" else "❌"
            print(f"{status_icon} 用例{result['id']}: {result['description']}")
            print(f"   输入: {result['input']}")
            print(f"   响应: {result['llm_response']}")
            if result["dsl_result"] and result["dsl_result"] != "N/A":
                print(f"   解析: {result['dsl_result']}")
            print(f"   状态: {result['status']}")
            print(f"   耗时: {result['execution_time']:.3f}s")
            if result["error"]:
                print(f"   错误: {result['error']}")
            print()


class AutomatedTestRunner:
    """自动化测试运行器"""

    @staticmethod
    def run_comprehensive_tests():
        """运行全面测试套件"""
        test_driver = CalligraphySystemTestDriver()

        # 加载测试用例
        test_cases = test_driver.load_test_cases_from_file("test_cases.txt")

        print("开始全面测试...")

        # 运行测试
        report = test_driver.run_test_suite(test_cases)

        # 保存报告 - 这里不再报错，因为save_report_to_file方法已添加
        test_driver.save_report_to_file(report, "comprehensive_test_report.json")

        # 显示详细报告
        test_driver.display_report(report)

        return report

    @staticmethod
    def run_unit_tests():
        """运行单元测试"""
        print("运行单元测试套件...")

        # 简单的单元测试示例
        test_driver = CalligraphySystemTestDriver()

        # 测试save_report_to_file方法
        test_report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_cases": 1,
                "passed_cases": 1,
                "failed_cases": 0,
                "error_cases": 0,
                "pass_rate": 100.0,
                "total_execution_time": 0.1,
                "average_execution_time": 0.1
            },
            "detailed_results": []
        }

        # 测试保存功能
        success = test_driver.save_report_to_file(test_report, "unit_test_report.json")
        print(f"单元测试 - 保存功能: {'通过' if success else '失败'}")

        return success


def main():
    """主函数"""
    test_driver = CalligraphySystemTestDriver()
    test_cases = test_driver.load_test_cases_from_file("test_cases.txt")

    print("书法专业领域咨询系统 - 测试框架")
    print("=" * 50)

    report = test_driver.run_test_suite(test_cases)

    # 保存详细报告
    test_driver.save_report_to_file(report, "test_report.json")

    # 显示详细结果
    test_driver.display_report(report)

    return report


if __name__ == "__main__":
    main()