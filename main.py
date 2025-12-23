import LLM
import grammar

if __name__=='__main__':
    ds = LLM.ds()
    dsl = grammar.CalligraphyDSL()
    print("🎨 书法专业领域咨询系统")
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
            if query.lower() in ['退出', 'quit', 'exit']:
                print("感谢使用书法咨询系统！")
                break

            if query.lower() in ['你好']:
                print(ds.deepseekchat(query))

            else:
                result = dsl.parse(ds.deepseekchat(query))
                print(f"{result}")
                print("-" * 50)
        except KeyboardInterrupt:
            print("\n感谢使用书法咨询系统！")
            break
        except Exception as e:
            print(f"系统错误：{e}")

