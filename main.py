import urllib.parse
from compare import Compare


class Relate(object):
    def __init__(self, Left_URL, Right_URL):
        self.Left_URL = Left_URL
        self.Right_URL = Right_URL
        self.Left_URL_Object = None
        self.Right_URL_Object = None
        self.semblance = 0

    def parseURL(self):
        '''
        使用urllib.parse.urlparse分析URL并创建对应对象，对象形式如下
        ParseResult(scheme='https', netloc='ssl.zc.qq.com', path='/v3/index-chs.html', params='', query='', fragment='')
        '''
        self.Left_URL_Object = urllib.parse.urlparse(self.Left_URL)
        self.Right_URL_Object = urllib.parse.urlparse(self.Right_URL)

    def compareURL(self):
        '''
        比对URL并更新相似度self.semblance
        '''
        self.semblance = Compare(self.Left_URL_Object, self.Right_URL_Object).get_score()

    def main_run(self):
        '''
        main运行函数
        :return: 相似度分数
        '''
        self.parseURL()
        self.compareURL()
        return self.semblance


if __name__ == '__main__':
    # left = 'https://www.baidu.com/1?wd=%27NoneType%27%20object%20is%20not%20callable&rsv_spt=1&rsv_iqid=0xa836ab8a00020647&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=0&rsv_n=2&rsv_sug3=1&inputT=1042&rsv_sug4=1042'
    # right = 'https://www.baidu.com/2?wd=%27NoneType%27%20object%20is%20not%20callable&rsv_spt=1&rsv_iqid=0xa836ab8a00020647&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=0&rsv_n=2&rsv_sug3=1&inputT=1042&rsv_sug4=1042'
    left = 'https://bbs.deepin.org/forum.php?mod=viewthread&tid=156276&extra='
    right = 'https://bbs.deepin.org/forum.php?mod=viewthread&tid=156845&extra='
    main = Relate(Left_URL=left, Right_URL=right).main_run()
    print(main)
