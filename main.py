import LLM
ds=LLM.ds()
if __name__=='__main__':
    q=input('请问有什么要咨询的吗？')
    ds.deepseekchat(q)
    while True:
        flag=input('请问还有其他问题吗？Y/N')
        if flag=='N':
            break
        elif flag=='Y':
            q=input('请问：')
            ds.deepseekchat(q)
        else:
            print('syntax error')

