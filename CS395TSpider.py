""" 
Created on Wed Jan 09 10:33:29 2013 
 
@Author: lanbing510 
"""  
  
from bs4 import BeautifulSoup  
import re  
import urllib  
import urlparse  
import os  
import sys  
import threading   
import traceback  
full_url='http://www.cs.utexas.edu/~cv-fall2012/schedule.html'  
response=urllib.urlopen(full_url)  
  
soup = BeautifulSoup(response.read())  
  
#import codecs, sys  
#old=sys.stdout  
#sys.stdout = codecs.lookup('utf-8')[-1]( sys.stdout)  
#print soup.prettify()  
down_count=0  
  
def downLoad(url,path):  
    def cbk(a, b, c):  
          
        """回调函数  
        @a: 已经下载的数据块  
        @b: 数据块的大小  
        @c: 远程文件的大小  
        """  
        per = 100.0 * a * b / c    
        if per>100:    
            per=100    
            #print '%.2f%%' % per    
    urllib.urlretrieve(url,path,cbk)  
    global down_count  
    down_count+=1;  
    print path.split("\\")[-1],'has download'  
    print 'have finished %d files ^_^' % down_count  
      
  
"""测试downLoad函数用"""  
#url='http://www.sina.com.cn'    
#local='d:\\sina.html'    
#downLoad(url,local)  
      
  
def main():  
    #f=open('path.txt','w+')#测试用  
    threads=[]#线程池  
    local_path='.\\Lan\\'#根目录  
    c1_path=''#一级目录  
    c2_path=''#二级目录  
    count=0;c=0;#for test  
    for sibling in soup.tr.next_siblings:  
        if sibling!='\n':  
            #count+=1  
            #print "[%d]: %s" %(count,repr(sibling))  
            #print type(sibling)  
            sibstr=repr(sibling)  
            if (re.search('rgb204,204,255',sibstr))!=None:  
                """注意括号的正则"""  
                #c+=1  
                print sibling.a['name']  
                c1_path=local_path+repr(sibling.a['name'])  
                if os.path.exists(c1_path)==False:  
                    os.mkdir(c1_path)  
                #continue  
            slist=sibling.find_all('a')  
            if slist!=[]:  
                try :  
                    c2_path=c1_path+'\\'+repr(slist[0]['name'])  
                except KeyError:  
                    continue  
                #print c2_path  
                c2_path=c1_path+'\\'+repr(slist[0]['name'])  
                if os.path.exists(c2_path)==False:  
                    os.mkdir(c2_path)  
                      
                  
                for li in slist[1:]:  
                    temp_url=li.get('href')  
                    count+=1  
                    if temp_url!=None:   
                        patt='http.+|ftp.+|www.+'  
                        if re.match(patt,temp_url)==None:  
                            temp_url=r'http://www.cs.utexas.edu/~cv-fall2012/'+temp_url#处理本服务器上的文件  
                        url_split_temp=temp_url.split('/')  
                        url_sp=url_split_temp[-1]if url_split_temp[-1]!='' else (url_split_temp[-2]+'.html')  
                        patt2='\.pdf$|\.html$|\.ppt$|\.doc$|\.docx$|\.pptx$|\.rar$|\.htm$|\.gz$|\.xml$'  
                        if re.search(patt2,url_sp)==None:  
                            url_sp=url_sp+'.html'  
                        temp_path=c2_path+'\\'+url_sp  
                    else:continue  
                   # print >>f,temp_url,'\n'  
                   # print >>f,temp_path,'\n'  
                #print count  
    #print 'c=',c  
                    t=threading.Thread(target=downLoad,args=(temp_url,temp_path))  
                    threads.append(t)  
                    t.start()  
  
    #f.close()  
  
if __name__=='__main__':      
    fe=open("error.txt",'w')#except的信息  
    sys.stderr=fe  
    try:  
        main()  
    finally:  
        fe.close()  
        sys.stderr=sys.stdout 