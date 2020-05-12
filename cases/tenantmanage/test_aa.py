import pytest

@pytest.fixture(scope="function")
def ff(request):
    print('ff')

    yield
    qqt(124)
 
    return 'ccc'
    
def qqt(num):
    print(num)

def pp():
    print('----pppp')

@pytest.mark.ftest
class Testaa:
    def test_01(self,ff):
        a = ff
        print(a)
        print('test01')

    def  test_02(self,ff):
        a = ff
        print(a)
        print('test01')


pytest.main(['-s','-m=ftest'])
