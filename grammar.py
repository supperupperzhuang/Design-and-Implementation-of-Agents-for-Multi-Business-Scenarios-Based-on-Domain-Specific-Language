import ply.yacc as yacc
import ply.lex as lex


class ds:
    pass
tokens = ('SCRIPT','STYLE','WRITER','ITEM')

lexer=lex.lex()
parser = yacc.yacc()