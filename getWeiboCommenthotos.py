import os
import time
import requests


class CommentPhotoCrawler(object):
    #weibo评论爬图


    def __init__(self, sleep_time=2):
        """
        初始化函数
        :param sleep_time: int, 默认为2, 爬取评论数据及图片的间隔时间
        :attr mid: string, 初始化为None, 由get_m_url方法爬取
        :attr login_headers: dict, 模拟登录请求头
        :attr session: requests Session
        """

        self.sleep_time = sleep_time
        self.mid = None
        self.login_headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection':'keep-alive',
            'Origin': 'https://passport.weibo.cn',
            'Referer':'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=https%3A%2F%2Fm.weibo.cn%2Fstatus%2F{}%3F'.format(self.mid)
        }
        self.session = None


   
    def get_mid(self):
        self.mid = input('请输入要爬的16位手机客户端ID：')    
        
    

    def login(self):
        user = input('请输入你的账号：')
        password = input('请输入你的密码：')
        internetaddress = 'https://m.weibo.cn/detail/{}'.format(self.mid)
        self.session = requests.Session()
        login_data = {
            'username':user,
            'password':password,
            'savestate':'1',
            'r': internetaddress,
            'ec': '0',
            'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=https%3A%2F%2Fm.weibo.cn%2Fstatus%2F{}%3F'.format(self.mid),
            'entry': 'mweibo',
            'mainpageflag': '1'
        }
        login_url = 'http://passport.weibo.cn/sso/login'
        self.session.post(login_url, headers=self.login_headers, data=login_data)
        print('登录手机网页微博成功！')


    def get_comments(self):
        max_page = int(input('请输入需要爬的页数:'))
        if isinstance(max_page, int):
            url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(self.mid, self.mid)
            response = self.session.get(url, headers=self.login_headers)
            max_id = response.json()['data']['max_id']
            max_id_type = response.json()['data']['max_id_type']
            self._store_pic_url(response)
            print('成功抓取第一页的图片链接！')


            if max_page > 1:
                for page in range(1, max_page):
                    url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'.format(self.mid, self.mid, max_id, max_id_type)
                    response = self.session.get(url, headers=self.login_headers)
                    max_id = response.json()['data']['max_id']
                    max_id_type = response.json()['data']['max_id_type']
                    self._store_pic_url(response)
                    print('成功抓取第{}页的图片链接！'.format(page + 1))
                    time.sleep(self.sleep_time)


    def _store_pic_url(self, response):
        for comment in response.json()['data']['data']:
            if 'pic' in comment.keys():
                with open('photourl.txt','a') as f:
                    f.write(comment['pic']['large']['url']+'\n')

    def download_photo(self, output='.'):
        os.mkdir(output+'/photos')
        with open('photourl.txt', 'r') as f:
            photo_urls = [url.strip() for url in f.readlines()]
        for url in photo_urls:
            res = requests.get(url)
            name = url.split('/')[-1]
            with open(output+'/photos/'+name, 'wb') as f:
                f.write(res.content)
            print('成功保存图片：{}'.format(name))
            time.sleep(self.sleep_time)


if __name__ == '__main__':
    com = CommentPhotoCrawler()
    com.get_mid()
    com.login()
    com.get_comments()
    com.download_photo()
        
