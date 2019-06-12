import requests
from lxml import etree
import time
import re
def search_baidu(keyword,nums=10,page=1):
    total_datas=[]
    get_num=0
    page=(page-1)*10
    while True:
        print('222',keyword,page)
        data_tuple=get_datas(keyword, page)
        datas=data_tuple[0]
        get_num += len(datas)  # 条数统计
        #当页面没有下一页时跳出循环，输出数据
        if not data_tuple[1] and int(nums) > get_num:
            total_datas += datas
            print('不够')
            return total_datas
        if int(nums) <= get_num:
            total_datas += datas[:len(datas) - (int(get_num) - int(nums))]  # 列表合并，保证最终输出一个列表
            print('够',len(total_datas))
            return total_datas
        total_datas += datas
        page+=10
    # print(total_datas)
    # print('yyyyyyyy',len(total_datas))
def get_datas(keyword,pn):
    url_baidu="https://www.baidu.com/s?wd=%s&pn=%s"%(keyword,pn)
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    result_list=requests.get(url=url_baidu,headers=headers).content.decode()
    html_content=etree.HTML(result_list)
    # 搜说首页百度查出的条数
    if int(pn)==0:
        num1=html_content.xpath('//span[@class="nums_text"]/text()')[0]
        num=re.compile('(\d.*\d)').findall(num1)[0].replace(',','')
        if num=='0':
            return
    #得到通过百度进入的url
    url_list=html_content.xpath('//div[@id="content_left"]//h3/a[1]/@href')
    #得到标题
    titles=[i.xpath('string(.)') for i in html_content.xpath('//div[@id="content_left"]//h3/a[1]')]
    #是否有下一页
    try:
        next_page=html_content.xpath('//div[@id="page"]//a[last()]/text()')[0]
        # print('/////////',next_page)
        if next_page=='下一页>':
            next_page=1
        else:
            next_page=0
    except:
        next_page=0
    # print('*********',next_page)
    urls=[]
    for i in url_list:
        try:
            res=requests.get(url=i).url
            urls.append(res)
        except:
            titles.pop(url_list.index(i))
    return data_format(urls,titles,keyword),next_page
def data_format(urls,titles,keyword):
    datas = []
    for i in urls:
        one_data = {}
        one_data['url']=i
        #去除非详情页地址，因有得到仍为列表地址页，需再次进入
        if re.compile(".*(www.baidu.com).*").findall(i):
            continue
        one_data['title']=titles[urls.index(i)]
        one_data['time_find']=time.time()
        one_data['engine']='www.baidu.con'
        one_data['key']=keyword
        one_data['ids']=urls.index(i)
        datas.append(one_data)
    return datas







if __name__ == '__main__':
    for i in ['text','python','hah','php']:
        print(search_baidu(i,10))





