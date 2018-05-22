from tldextract import tldextract
import urllib.parse


def checkContinue_flag(func):
    '''
    检查continue_flag的装饰器。continue_flag的作用是：如果前面权值重的因素不同，则认为相似度为0，即没有继续分析的必要。
    :param func:要进行装饰的函数
    :return:
    '''
    def wrapper(self, *args, **kwargs):
        if self.continue_flag is True:
            return func(self, *args, **kwargs)
        return None
    return wrapper

class Compare(object):
    def __init__(self, Left_URL_Object, Right_URL_Object):
        '''
        :param Left_URL_Object:

        得到的Left_URL_Object如下例
        ParseResult(
            scheme='https',
            netloc='ssl.zc.qq.com',
            path='/v3/index-chs.html',
            params='',
            query='',
            fragment=''
        )
        '''
        self.Left_URL_Object = Left_URL_Object
        self.Right_URL_Object = Right_URL_Object
        self.continue_flag = True
        # self.score应设置为数字，此处设置为字符串和以下增加字母，是为了测试时找出哪些地方计算进了分数
        # self.score = ''
        self.score = 0

    @checkContinue_flag
    def cmpNetloc(self):
        '''
        调用第三方库，得到的Left_Netloc_Object如下例
        ExtractResult(
            subdomain='ssl.zc',
            domain='qq',
            suffix='com'
        )
        registered_domain='qq.com',
        fqdn='ssl.zc.qq.com',
        '''
        Left_Netloc_Object = tldextract.extract(self.Left_URL_Object.netloc)
        Right_Netloc_object = tldextract.extract(self.Right_URL_Object.netloc)

        # 比较registered_domain
        if self.checkValue(Left_Netloc_Object.registered_domain, Right_Netloc_object.registered_domain, 2 ** 5) is False:
        # if self.checkValue(Left_Netloc_Object.registered_domain, Right_Netloc_object.registered_domain, 'a') is False:
            self.continue_flag = False

        # 比较subdomain
        if self.checkValue(Left_Netloc_Object.subdomain, Right_Netloc_object.subdomain, 2 ** 4) is False:
        # if self.checkValue(Left_Netloc_Object.subdomain, Right_Netloc_object.subdomain, 'b') is False:
            self.continue_flag = False

    @checkContinue_flag
    def cmpPath(self):
        # 根据'/'分割URL中的路径部分
        Left_Path_List = self.Left_URL_Object.path.split('/')
        while '' in Left_Path_List:
            Left_Path_List.remove('')
        Right_Path_List = self.Right_URL_Object.path.split('/')
        while '' in Right_Path_List:
            Right_Path_List.remove('')

        # 检查路径深度，不相等则不相似 fixme 若路径过长会使此处权值增大，暂未参取措施限制此处最多加多少分数
        if self.checkValue(len(Left_Path_List), len(Right_Path_List), 2 ** 3) is True:
        # if self.checkValue(len(Left_Path_List), len(Right_Path_List), 'c') is True:

            for left, right in zip(Left_Path_List, Right_Path_List):
                # 比对每一层路径是否相等
                if self.checkValue(left, right, 2 ** 2) is False:
                # if self.checkValue(left, right, 'd') is False:

                #     当当前层路径不相等时，比对是否都为数字
                    self.checkDigit(left, right, 2 ** 1)
                    # self.checkDigit(left, right, 'e')

    @checkContinue_flag
    def cmpParams(self):
        # print(self.Left_URL_Object)
        pass

    @checkContinue_flag
    def cmpQuery(self):
        # 将字符串转化为字典
        def Query_to_Dict(query):
            return dict([(k, v[0]) for k, v in urllib.parse.parse_qs(query).items()])

        Left_Query_Dict = Query_to_Dict(self.Left_URL_Object.query)
        Right_Query_Dict = Query_to_Dict(self.Right_URL_Object.query)

        # 比对是否参数个数相等
        if self.checkValue(len(Left_Query_Dict), len(Right_Query_Dict), 2 ** 1) is True:
        # if self.checkValue(len(Left_Query_Dict), len(Right_Query_Dict), 'f') is True:

            # 比对是否都含有同一参数奸 fixme 和路径深度有相同问题，暂未参取措施限制此处最多加多少分数
            for left_key, left_value in Left_Query_Dict.items():
                if left_key in Right_Query_Dict:
                    self.score += 2 ** 0
                    # self.score += 'g'

                    # 比较是否相同键也有相同值
                    self.checkValue(left_value, Right_Query_Dict.get(left_key), 2 ** 0)
                    # self.checkValue(left_value, Right_Query_Dict.get(left_key), 'h')

    @checkContinue_flag
    def cmpFragment(self):
        pass

    @checkContinue_flag
    def cmpScheme(self):
        pass

    @checkContinue_flag
    def checkValue(self, left, right, addScore):
        '''
        检查值是否相同，相同则加上相应权值分数并返回True，不相同则不加并返回False
        :param left:
        :param right:
        :param addScore:
        :return:
        '''
        if left == right:
            self.score += addScore
            return True
        else:
            return False

    def checkDigit(self, left, right, addScore):
        '''
        检查类型是否都是数字，相同则加上相应权值分数并返回True，不相同则不加并返回False
        :param left:
        :param right:
        :param addScore:
        :return:
        '''
        if left.isdigit() is True and right.isdigit() is True:
            self.score += addScore
            return True
        else:
            return False

    def get_score(self):
        '''The main function'''
        self.cmpNetloc()
        self.cmpPath()
        self.cmpParams()
        self.cmpQuery()
        self.cmpFragment()
        self.cmpScheme()
        return self.score


if __name__ == '__main__':
    co = Compare()