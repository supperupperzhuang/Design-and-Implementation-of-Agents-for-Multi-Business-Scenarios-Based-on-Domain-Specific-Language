# optimized_main.py
"""
优化后的主程序
集成测试桩和测试驱动框架
"""

import argparse
import time
import sys
import os
from typing import List, Tuple, Any, Dict

# 导入测试桩
from test_llm_stub import MockLLM, ErrorProneLLM
from test_grammar_stub import MockCalligraphyDSL, ValidatingDSL
from test_driver import CalligraphySystemTestDriver, AutomatedTestRunner


class EnhancedCalligraphySystem:
    """增强版书法咨询系统"""

    def __init__(self, test_mode=False, use_stubs=False):
        self.test_mode = test_mode
        self.use_stubs = use_stubs
        self.initialize_components()
        self.setup_logging()

    def initialize_components(self):
        """初始化系统组件"""
        if self.use_stubs:
            # 使用测试桩
            from test_llm_stub import MockLLM
            from test_grammar_stub import MockCalligraphyDSL
            self.llm = MockLLM()
            self.dsl = MockCalligraphyDSL()
        else:
            # 使用真实组件
            import LLM
            import grammar
            self.llm = LLM.ds()
            self.dsl = grammar.CalligraphyDSL()

        self.session_stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "greeting_responses": 0,
            "failed_queries": 0,
            "start_time": time.time()
        }

    def setup_logging(self):
        """设置日志系统"""
        self.log = {
            "queries": [],
            "responses": [],
            "errors": []
        }

    def process_query(self, query: str) -> Dict[str, Any]:
        """处理用户查询"""
        result = {
            "query": query,
            "timestamp": time.time(),
            "llm_response": None,
            "dsl_result": None,
            "response_type": None,
            "success": False,
            "error": None
        }

        try:
            self.session_stats["total_queries"] += 1

            # 调用LLM处理查询
            llm_response = self.llm.deepseekchat(query)
            result["llm_response"] = llm_response

            # 判断响应类型并处理
            if llm_response.startswith(('查询', '查找', '搜索', '找', '请问', '我想知道', '了解', '显示', '展示')):
                # 查询类语句 - 使用DSL解析
                dsl_result = self.dsl.parse(llm_response)
                result["dsl_result"] = dsl_result
                result["response_type"] = "查询类"
                result["success"] = True
                self.session_stats["successful_queries"] += 1

            else:
                # 问候类或引导类语句 - 直接返回
                result["response_type"] = "问候类"
                result["success"] = True
                self.session_stats["greeting_responses"] += 1

        except Exception as e:
            result["error"] = str(e)
            result["success"] = False
            self.session_stats["failed_queries"] += 1
            self.log["errors"].append({
                "query": query,
                "error": str(e),
                "timestamp": time.time()
            })

        # 记录日志
        self.log["queries"].append(query)
        self.log["responses"].append(result)

        return result

    def interactive_mode(self):
        """交互式模式"""
        print("书法专业领域咨询系统（增强版）")
        print("支持以下查询类型：")
        print("1. 查询书法家信息")
        print("2. 查询作品信息")
        print("3. 查询书体风格")
        print("4. 查询朝代书家")
        print("5. 简单查询")
        print("输入'退出'或'quit'结束查询")
        print("-" * 50)

        while True:
            try:
                query = input("请输入查询：").strip()

                if query.lower() in ['退出', 'quit', 'exit', '再见']:
                    self.display_session_stats()
                    print("感谢使用书法咨询系统！")
                    break

                if not query:
                    print("查询不能为空，请重新输入。")
                    continue

                # 处理查询
                start_time = time.time()
                result = self.process_query(query)
                processing_time = time.time() - start_time

                # 显示结果
                if result["success"]:
                    if result["response_type"] == "查询类":
                        print(f"结果: {result['dsl_result']}")
                    else:
                        print(f"系统回复: {result['llm_response']}")
                    print(f"[处理时间: {processing_time:.2f}秒]")
                else:
                    print(f"系统错误：{result['error']}")

                print("-" * 50)

            except KeyboardInterrupt:
                self.display_session_stats()
                print("\n感谢使用书法咨询系统！")
                break
            except Exception as e:
                print(f"系统错误：{e}")

    def run_automated_test(self, test_file_path: str) -> Dict[str, Any]:
        """运行自动化测试"""
        print("=" * 60)
        print("书法专业领域咨询系统 - 自动测试模式")
        print("=" * 60)

        try:
            with open(test_file_path, 'r', encoding='utf-8') as file:
                test_queries = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"错误：找不到测试文件 '{test_file_path}'")
            return {}
        except Exception as e:
            print(f"读取测试文件时出错：{e}")
            return {}

        print(f"从文件 '{test_file_path}' 加载了 {len(test_queries)} 个测试查询")
        print("开始自动测试...\n")

        results = []
        start_time = time.time()

        for i, query in enumerate(test_queries, 1):
            print(f"{i}. 测试查询: {query}")

            try:
                query_start = time.time()
                result = self.process_query(query)
                query_time = time.time() - query_start

                print(f"   LLM转换结果: {result['llm_response']}")

                if result['response_type'] == '查询类':
                    print(f"   DSL解析结果: {result['dsl_result']}")
                    results.append((query, result['llm_response'],
                                    result['dsl_result'], "成功", query_time))
                else:
                    print(f"   系统回复: {result['llm_response']}")
                    results.append((query, result['llm_response'],
                                    "N/A", "问候/引导语句", query_time))

            except Exception as e:
                error_msg = f"处理查询时出错: {e}"
                print(f"   ❌ {error_msg}")
                results.append((query, "N/A", "N/A", f"错误: {e}", 0))

            print("-" * 50)

            if not self.test_mode:
                time.sleep(1)  # 生产环境添加延迟避免API限制

        return self.generate_test_report(results, start_time)

    def generate_test_report(self, results: List[Tuple], start_time: float) -> Dict[str, Any]:
        """生成测试报告"""
        end_time = time.time()
        total_time = end_time - start_time

        successful_queries = len([r for r in results if r[3] == "成功"])
        greeting_queries = len([r for r in results if r[3] == "问候/引导语句"])
        failed_queries = len([r for r in results if r[3].startswith("错误")])

        # 生成报告
        report = {
            "test_summary": {
                "total_queries": len(results),
                "successful_queries": successful_queries,
                "greeting_queries": greeting_queries,
                "failed_queries": failed_queries,
                "success_rate": (successful_queries / len(results)) * 100 if results else 0,
                "total_time": total_time,
                "average_time": total_time / len(results) if results else 0
            },
            "detailed_results": [
                {
                    "query": r[0],
                    "llm_response": r[1],
                    "dsl_result": r[2],
                    "status": r[3],
                    "processing_time": r[4]
                } for r in results
            ],
            "session_stats": self.session_stats
        }

        # 打印报告
        print("\n" + "=" * 60)
        print("测试报告")
        print("=" * 60)
        print(f"总测试用例: {len(results)}")
        print(f"成功解析查询: {successful_queries}")
        print(f"问候/引导语句: {greeting_queries}")
        print(f"失败查询: {failed_queries}")
        print(f"总耗时: {total_time:.2f} 秒")
        print(f"平均每个查询: {total_time / len(results):.2f} 秒" if results else "N/A")

        # 显示失败的查询
        if failed_queries > 0:
            print("\n失败的查询:")
            for query, _, _, status, _ in results:
                if status.startswith("错误"):
                    print(f"  - {query}: {status}")

        return report

    def display_session_stats(self):
        """显示会话统计信息"""
        print("\n" + "=" * 60)
        print("会话统计")
        print("=" * 60)
        print(f"总查询数: {self.session_stats['total_queries']}")
        print(f"成功查询: {self.session_stats['successful_queries']}")
        print(f"问候回复: {self.session_stats['greeting_responses']}")
        print(f"失败查询: {self.session_stats['failed_queries']}")

        if self.session_stats['total_queries'] > 0:
            success_rate = (self.session_stats['successful_queries'] /
                            self.session_stats['total_queries'] * 100)
            print(f"成功率: {success_rate:.1f}%")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='书法专业领域咨询系统')
    parser.add_argument('--test', type=str, help='运行自动测试，指定测试文件路径')
    parser.add_argument('--interactive', action='store_true',
                        help='进入交互模式（默认）')
    parser.add_argument('--use-stubs', action='store_true',
                        help='使用测试桩代替真实组件')
    parser.add_argument('--run-unit-tests', action='store_true',
                        help='运行单元测试套件')

    args = parser.parse_args()

    # 运行单元测试
    if args.run_unit_tests:
        print("运行单元测试套件...")
        report = AutomatedTestRunner.run_comprehensive_tests()
        return

    # 创建系统实例
    system = EnhancedCalligraphySystem(use_stubs=args.use_stubs)

    # 运行自动测试或交互模式
    if args.test:
        system.run_automated_test(args.test)
    else:
        system.interactive_mode()


if __name__ == '__main__':
    main()