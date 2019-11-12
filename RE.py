import  requests
import  re
import  json

def parse_page(url):
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'

    }
    reeponse = requests.get(url,headers)
    text = reeponse.text
    # print(text)
    # 此处使用非贪婪模式，因为如果采用贪婪模式，re会匹配到整篇html最后一个</b>才开始“截断”，把之前的部分都当作一个被匹配的整体，最终只能获取到最后一个符合要求的字符串
    #标题获取
    titles = re.findall('<div\sclass="cont">.*?<b>(.*?)</b>',text,re.DOTALL)
    #朝代获取
    dynasties = re.findall('<p\sclass="source">.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    #作者获取
    authors = re.findall('<p\sclass="source">.*?<a.*?</span><a.*?>(.*?)</a></p>',text,re.DOTALL)
    #文章内容获取
    contents_tags = re.findall('<div\sclass="contson".*?>(.*?)</div>',text,re.DOTALL)

    contents = []
    for content in contents_tags:
        #去除标签字符
        x = re.sub('<.*?>','',content)
        #去除空格
        x = x.strip()
        #加入列表
        contents.append(x.strip())

    Poems=[]
    #列表转换成字典常用方法：for value in zip (序列解包)
    for value in zip(titles,dynasties,authors,contents):
        title, dynasty, author, content = value
        poems= {
            'title':title ,
            'dynasties':dynasty,
            'author':author,
            'content':content
            }
        #拼接成完整列表
        Poems.append(poems)



    #列表写入json文件

    with open('poems.json', 'w',encoding='utf-8') as fp:
        json.dump(Poems,fp,ensure_ascii=False)



def main():
    url = 'https://www.gushiwen.org/default_1.aspx'
    parse_page(url)

if __name__ == '__main__':
    main()