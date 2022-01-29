import requests
from lxml import etree
from scan import isJudge


# 读取url并return出去
class readUrls():
    url_list = []
    def read(self):
        fp = open('./urls.txt','r')
        for u in fp:
            url = u.strip()
            self.url_list.append(url)
        print("The number of urls obtained is {}\n----------------------------------------------------------------".format(len(self.url_list)))
        fp.close()
        return self.url_list  # 返回读取到的所有url


# 请求获得的url中所有的符合条件的a标签连接，存放进列表并return返回出去
class request():
    def request_urls(self,url):
        a_list = []
        try:
            header = {
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            }
            # print("Processing in progress:",url)
            request_page = requests.get(url,headers=header).text
            page_obj = etree.HTML(request_page)
            # 获取当前url中的所有a标签中的href内容
            a = page_obj.xpath("//a/@href")
            # 添加筛选条件，选出符合条件的url
            for tag in a:
                status = tag.find("http")
                if status == -1:
                    whole_url = url + tag  # 拼接成完整的url
                    filter_url = whole_url.find("#")
                    if filter_url == -1:  # url中没有#号，为符合条件的url
                        filter_script = tag.find("script")
                        if filter_script == -1:  # url中没有script，为符合条件的url
                            filter_parm = tag.find("?")  # 选出url中带有？的加入列表
                            if filter_parm != -1:
                                a_list.append(whole_url)  # 添加进列表
                else:
                    filter_parm1 = tag.find("?")
                    if filter_parm1 != -1:
                        a_list.append(tag)
            judgeLen = len(a_list)
            if judgeLen == 0:  # 判断该页是否存在a标签
                List = -1
            else:
                List = a_list
            print("The A tag of {}'s counting:".format(url),judgeLen)
            print(List,"\n----------------------------------------------------------------")
            return List
        except Exception as error:
            print(error)


# 主程序入口
if __name__ == "__main__":
    # count = input("Please enter the number of URLs to be processed:")

    # 开始读取url
    url_obj = readUrls()
    url_list = url_obj.read()

    # 这里采用模式是：逐个去除url进行各种判断输出
    for url in url_list:
        # 开始读取url中的a标签中的连接，以列表的形式返回到req_list
        req_obj = request()
        req_list = req_obj.request_urls(url)
        if req_list == -1:
            print("{} not find a tags!".format(url))
            continue

        # 判断url的数据库类型并测试a标签
        judge_DB = isJudge()
        fixed_list = judge_DB.fixDeal(req_list)  # 将筛选后的url传入,并接受去参后的url

        result = judge_DB.testDeal(fixed_list)  # 传入去参的url，开始添加测试语句
        if result == -1:
            print("url+'has exist Firewall,next action has stop!'")
            break
        print(result)

        # 测试输入框处









