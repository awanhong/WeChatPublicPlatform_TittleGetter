import urllib.request
import http.cookiejar
import re
 
# head: dict of header
def makeMyOpener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

#Initialize
pagenumber = 150
final_date='2017-01-30'
fout = open("Titles.txt", "w+", encoding="utf-8")

for i in range(pagenumber):
    pagemark = (i)*12
    #央视新闻 pagename = 'http://chuansong.me/account/cctvnewscenter?start='
    #中国青年报 pagename = 'http://chuansong.me/account/zqbcyol?start='
    #中国新闻网 pagename = 'http://chuansong.me/account/cns2012?start='
    #China Daily pagename = 'http://chuansong.me/account/RealTimeChina?start='
    pagename = 'http://chuansong.me/account/BeijingHour?start='
    pagename = pagename + str(pagemark)
    #Get Web Content 
    oper = makeMyOpener()
    uop = oper.open(pagename, timeout = 1000)
    data = uop.read()
    content = data.decode()
    #Get Titles
    pattern_title = re.compile('<a class="question_link" href="(.*?)" target="_blank">(.*?)</a>',re.S)
    items_title = re.findall(pattern_title,content)
    pattern_date = re.compile('<span class="timestamp" style="color: #999">(.*?)</span>',re.S)
    items_date = re.findall(pattern_date,content)
    final_date_number = -1
    i=0
    for item in items_date:
        if item==final_date:
            final_date_number = i
            break
        i=i+1
    i=0
    for item in items_title:
        print(items_date[i],item[1])
        fout.write(items_date[i])
        fout.write(item[1])
        if i==final_date_number:
            break
        i=i+1
    if final_date_number!=-1:
        break
fout.close()
#print(data.decode())
