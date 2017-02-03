from bs4 import BeautifulSoup
import requests
import time

url = 'http://sh.58.com/diannao/25501981856952x.shtml'  # 25501981856952正好是id

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
    'Cookie': 'userid360_xml=D28DF54CB323DCED2CFA18A1C7CEEBBC; time_create=1462777542676; f=n; bangbangid=1080863914006730649; bj58_id58s="ZzV3NTJaNTVmSndhMTgyNw=="; id58=c5/njVcFsX9HOwa7CITsAg==; als=0; myfeet_tooltip=end; mcity=sh; sessionid=359058c2-4a08-42e0-8107-36c729b78f14; city=sh; 58home=sh; ipcity=sh%7C%u4E0A%u6D77%7C0; CNZZDATA1253723458=774823064-1460104326-http%253A%252F%252Fbzclk.baidu.com%252F%7C1460182207; bdshare_firstime=1460190813132; uuid=0d2254a0-9b18-42ed-90ba-d667f33f48de; bj58_new_uv=8; 58tj_uuid=e2f806b6-2f9c-41e7-a3aa-bda0da47de44; new_uv=9; final_history=25501981856952%2C25621815919413%2C25611239057723%2C25587817870121%2C25214284901551; br58=index_old; f=n',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://sh.58.com/diannao/0/pn2/'
    # 加上Referer  不然爬不到views
}


def get_links_from(nums):
    urls = []
    list_view = 'http://sh.58.com/pbdn/{}/pn2/'.format(str(nums))
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    for link in soup.select('td.t a.t'):
        urls.append(link.get('href').split('?')[0])

    return urls


def get_views_from(url):
    id = url.split('/')[-1].strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(id)
    js = requests.get(api, headers=headers)
    views = js.text.split('=')[
        -1]  # 这是一个js   Counter58.userlist[0]={uid:'0',uname:'',face:'',vt:''};Counter58.total=1503
    return views


def get_item_info(nums):
    urls = get_links_from(nums)
    for url in urls:
        wb_data = requests.get(url, headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        data = {
            'title': soup.title.text,
            'price': None if len(soup.select('span.price')) == 0 else soup.select('span.price')[0].text,
            'date': None if len(soup.select('.time')) == 0 else soup.select('.time')[0].text,
            'area': list(soup.select('.c_25d')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None,
            # stripped_strings 输出多个字符串并去掉了空格 使用soup.find_all()方法找到有没有这个
            'cate': u'商家' if nums == 1 else u'个人',  # 分类
            'views': get_views_from(url)  # 浏览量  与id有关
        }

        print(data)


get_item_info(0)
