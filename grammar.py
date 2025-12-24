import ply.lex as lex
import ply.yacc as yacc


class CalligraphyDSL:
    """
    基于PLY的书法领域特定语言(DSL)类
    支持查询书法家、作品、风格等专业信息
    """

    def __init__(self):
        # 书法家数据库
        self.calligraphers = {
            '王羲之': {
                'dynasty': '东晋',
                'style': '行书',
                'works': ['兰亭序', '黄庭经'],
                'description': '书圣，行书代表作《兰亭序》被誉为天下第一行书'
            },
            '颜真卿': {
                'dynasty': '唐代',
                'style': '楷书',
                'works': ['祭侄文稿', '多宝塔碑'],
                'description': '楷书四大家之一，创立颜体'
            },
            '苏轼': {
                'dynasty': '宋代',
                'style': '行书',
                'works': ['黄州寒食诗帖'],
                'description': '宋代书法四大家之一，尚意书风代表'
            },
            '柳公权': {
                'dynasty': '唐代',
                'style': '楷书',
                'works': ['玄秘塔碑', '神策军碑'],
                'description': '楷书四大家之一，创立柳体'
            },
            '张旭': {
                'dynasty': '唐代',
                'style': '草书',
                'works': ['古诗四帖'],
                'description': '草圣，狂草书法代表人物'
            },
            '欧阳询': {
                'dynasty': '唐代',
                'style': '楷书',
                'works': ['九成宫醴泉铭'],
                'description': '楷书四大家族之一，欧体创始人'
            }
        }

        # 书法风格数据库
        self.styles = {
            '行书': {
                'description': '笔势流畅、动静相宜，介于楷书和草书之间',
                'masters': ['王羲之', '苏轼', '颜真卿'],
                'features': ['用笔灵活', '结构自如', '书写便捷']
            },
            '楷书': {
                'description': '结构严谨、笔画端正，法度森严',
                'masters': ['颜真卿', '柳公权', '欧阳询'],
                'features': ['横平竖直', '结构方正', '笔力劲健']
            },
            '草书': {
                'description': '纵任奔逸、赴速急就，艺术性极强',
                'masters': ['张旭', '怀素', '王献之'],
                'features': ['笔势连绵', '气势贯通', '变化多端']
            },
            '隶书': {
                'description': '字形扁平、笔画波磔，古朴典雅',
                'masters': ['蔡邕', '钟繇', '邓石如'],
                'features': ['蚕头雁尾', '一波三折', '结构严谨']
            }
        }

        # 定义词法单元 - 简化令牌列表
        self.tokens = (
            'FIND', 'CALLIGRAPHER', 'WORK', 'STYLE', 'DYNASTY',
            'INFO', 'CHINESE_NAME'
        )

        # 构建词法分析器和语法分析器
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self, debug=False)

    # 词法规则 - 保持"的"字作为忽略字符
    t_ignore = ' \t\r\n的'

    def t_CALLIGRAPHER(self, t):
        r'书法家|书家|书法大师|书法名家'
        return t

    def t_WORK(self, t):
        r'作品|书法作品|著名作品|墨宝|代表作'
        return t

    def t_STYLE(self, t):
        r'风格|书体|字体|书法风格|书风'
        return t

    def t_DYNASTY(self, t):
        r'唐代|宋代|晋代|明代|清代|唐朝|宋朝|晋朝|明朝|清朝|东晋'
        # 统一朝代名称
        dynasty_map = {'唐朝': '唐代', '宋朝': '宋代', '晋朝': '晋代',
                       '明朝': '明代', '清朝': '清代'}
        t.value = dynasty_map.get(t.value, t.value)
        return t

    def t_INFO(self, t):
        r'信息'
        return t

    def t_FIND(self, t):
        r'查询|查找|搜索|找|请问|我想知道|了解|显示|展示'
        return t

    def t_CHINESE_NAME(self, t):
        r'[王羲之颜真卿苏轼柳公权张旭欧阳询兰亭序黄庭经祭侄文稿多宝塔碑黄州寒食诗帖玄秘塔碑神策军碑古诗四帖九成宫醴泉铭行书楷书草书隶书]+'
        # 只匹配已知的书法家姓名、作品名称和书体名称
        if not t.value.strip():
            return None
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        # 对于无法识别的字符，跳过继续分析
        t.lexer.skip(1)

    # 语法规则 - 简化语法规则，删除依赖"的"字的规则
    def p_query(self, p):
        """
        query : find_calligrapher_detail
              | find_work_representative
              | find_style
              | find_dynasty_calligraphers
              | find_calligrapher_info
              | find_direct
              | find_calligrapher_style
        """
        p[0] = p[1]

    # 规则1: 详细书法家查询 - "查询书法家王羲之"
    def p_find_calligrapher_detail(self, p):
        """find_calligrapher_detail : FIND CALLIGRAPHER CHINESE_NAME"""
        name = p[3]
        if name in self.calligraphers:
            info = self.calligraphers[name]
            p[0] = f"📖 {name}书法家信息：\n" \
                   f"   朝代：{info['dynasty']}\n" \
                   f"   擅长书体：{info['style']}\n" \
                   f"   代表作品：{'、'.join(info['works'])}\n" \
                   f"   简介：{info['description']}"
        else:
            p[0] = f"❌ 未找到书法家'{name}'的信息"

    # 规则2: 作品查询- "查询王羲之作品"
    def p_find_work_representative(self, p):
        """find_work_representative : FIND CHINESE_NAME WORK"""
        calligrapher = p[2]
        if calligrapher in self.calligraphers:
            works = self.calligraphers[calligrapher]['works']
            style = self.calligraphers[calligrapher]['style']
            p[0] = f"🎨 {calligrapher}的代表作品（{style}）：\n" \
                   f"   {'、'.join(works)}"
        else:
            p[0] = f"❌ 未找到{calligrapher}的作品记录"

    # 规则3: 直接作品查询 - "查询兰亭序"
    def p_find_direct(self, p):
        """find_direct : FIND CHINESE_NAME"""
        work_name = p[2]

        # 检查是否是作品名称
        found = False
        for calligrapher, info in self.calligraphers.items():
            if work_name in info['works']:
                p[0] = f"📜 {work_name}是{calligrapher}的代表作\n" \
                       f"   书体：{info['style']}\n" \
                       f"   朝代：{info['dynasty']}\n" \
                       f"   书法家简介：{info['description']}"
                found = True
                break

        if not found:
            # 如果不是作品，检查是否是书法家简单查询
            if work_name in self.calligraphers:
                info = self.calligraphers[work_name]
                p[0] = f"📖 {work_name}书法家信息：\n" \
                       f"   朝代：{info['dynasty']}\n" \
                       f"   擅长书体：{info['style']}\n" \
                       f"   代表作品：{'、'.join(info['works'])}\n" \
                       f"   简介：{info['description']}"
            else:
                p[0] = f"❌ 未找到'{work_name}'的相关信息"

    # 规则4: 风格查询 - "查询风格行书"
    def p_find_style(self, p):
        """find_style : FIND STYLE CHINESE_NAME"""
        style = p[3]
        if style in self.styles:
            info = self.styles[style]
            p[0] = f"🖋️ {style}书体信息：\n" \
                   f"   特点：{info['description']}\n" \
                   f"   代表书家：{'、'.join(info['masters'])}\n" \
                   f"   艺术特征：{'、'.join(info['features'])}"
        else:
            p[0] = f"❌ 未找到{style}书体的详细说明"

    # 规则5: 书法家风格查询 - "搜索苏轼书法风格"（无"的"字）
    def p_find_calligrapher_style(self, p):
        """find_calligrapher_style : FIND CHINESE_NAME STYLE"""
        calligrapher = p[2]
        if calligrapher in self.calligraphers:
            style = self.calligraphers[calligrapher]['style']
            style_desc = self.styles.get(style, {}).get('description', '暂无详细描述')
            p[0] = f"🎯 {calligrapher}的书法风格：\n" \
                   f"   擅长{style}书体\n" \
                   f"   风格特点：{style_desc}"
        else:
            p[0] = f"❌ 未找到{calligrapher}的书法风格信息"

    # 规则6: 朝代书法家查询 - "查询唐代书法家"
    def p_find_dynasty_calligraphers(self, p):
        """find_dynasty_calligraphers : FIND DYNASTY CALLIGRAPHER"""
        dynasty = p[2]
        artists = [name for name, info in self.calligraphers.items()
                   if info['dynasty'] == dynasty]
        if artists:
            artist_info = []
            for artist in artists:
                style = self.calligraphers[artist]['style']
                artist_info.append(f"{artist}（{style}）")
            p[0] = f"🏛️ {dynasty}著名书法家：\n" \
                   f"   {'、'.join(artist_info)}"
        else:
            p[0] = f"❌ 未找到{dynasty}的书法家记录"

    # 规则7: 书法家信息查询 - "查询张旭信息"
    def p_find_calligrapher_info(self, p):
        """find_calligrapher_info : FIND CHINESE_NAME INFO"""
        name = p[2]
        if name in self.calligraphers:
            info = self.calligraphers[name]
            p[0] = f"📖 {name}书法家信息：\n" \
                   f"   朝代：{info['dynasty']}\n" \
                   f"   擅长书体：{info['style']}\n" \
                   f"   代表作品：{'、'.join(info['works'])}\n" \
                   f"   简介：{info['description']}"
        else:
            p[0] = f"❌ 未找到书法家'{name}'的信息"

    # 错误处理
    def p_error(self, p):
        if p:
            return f"语法错误 near '{p.value}'"
        else:
            return "无法理解您的查询，请尝试重新表述"

    def parse(self, text):
        """解析输入文本并返回查询结果"""
        try:
            # 重置词法分析器状态
            self.lexer.lineno = 1
            result = self.parser.parse(text, lexer=self.lexer)
            return result if result else "无法理解您的查询，请尝试重新表述"
        except Exception as e:
            return f"解析过程中出现错误：{str(e)}"


def test_calligraphy_dsl():
    """测试书法DSL的完整功能"""
    dsl = CalligraphyDSL()

    test_queries = [
        "查询书法家王羲之",
        "查询王羲之作品",
        "查询王羲之的作品",  # "的"字将被忽略
        "查询风格行书",
        "查询唐代书法家",
        "查找颜真卿的代表作",  # "的"字将被忽略
        "搜索苏轼的书法风格",  # "的"字将被忽略
        "查询张旭信息",
        "请问柳公权的作品",  # "的"字将被忽略
        "了解欧阳询",
        "查询兰亭序",
        "展示颜真卿代表作",  # "的"字将被忽略
        '查询王羲之',
        '查询张旭的代表作',  # "的"字将被忽略
        '查询唐代书法家',
    ]

    print("=" * 60)
    print("书法专业领域咨询DSL测试结果")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Q: {query}")
        result = dsl.parse(query)
        print(f"A: {result}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == '__main__':
    # 运行测试
    test_calligraphy_dsl()