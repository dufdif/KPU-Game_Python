from http.client import HTTPConnection
from xml.etree import ElementTree
import smtplib
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

host = 'smtp.gmail.com'
port = '587'
sender='dufdif10@gmail.com'
reciver=''


원전목록=[]

class 원자력발전소:
    name=''
    code=''
    time=''
    val=''

    def __init__(self,n='',c='',t='',v=''):
        self.name=n
        self.code=c
        self.time=t
        self.val=v



class 원전리스트:
    목록=[]

    def 원전추가(self,data):
        self.목록+=[data]
    def 원전초기화(self):
        self.목록=[]
    def 원전정렬(self,upper=True):
        if upper == True:
            self.목록.sort(key=lambda d :  d.val)
        else:
            self.목록.sort(key=lambda d: d.val,reverse=True)
    def 목록출력(self):
        for i in self.목록:
            print('이름 : {0} , 코드명 : {1}, 시간 :{2} , 방사능 수치: {3} '.format(i.name,i.code,i.time,i.val))
    def 메일발송(self):
        st=''
        if len(self.목록) != 0:
            for i in self.목록:
                st+='이름 : '    + str(i.name) +  '코드명 : ' + str(i.code) + ' 시간 : ' + str(i.time) + ' 방사능 수치 : '+ str(i.val) +'\n'
            reciver=input('받는 사람 이메일 주소 입력')
            msg=MIMEText(st)
            msg['Subject']='원전 주변 방사능 측정 정보'
            msg['From']=sender
            msg['To']=reciver
            s=smtplib.SMTP(host,port)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender,'2rhksrn7493')
            s.sendmail(sender,reciver,msg.as_string())
            print('전송완료')
            s.close()




원자력리스트=원전리스트()



conn = HTTPConnection('khnp.co.kr')
conn.request('GET',
             'http://www.khnp.co.kr/environ/service/realtime/radiorate?userkey=zuxJrlJij2dzU48AWBr2F02LjlKKdW8qLfCb7vimllYvqNyj6d02rPkiTqnHojcA3px9EKugkbmgLVTJuujfEg%3D%3D')
req = conn.getresponse()
print(req.status)
data = req.read()
tree = ElementTree.fromstring(data)
ele = tree.getiterator('item')

mquit=1


#원자력리스트.목록출력()
#원자력리스트.원전정렬()
#원자력리스트.목록출력()


def AllList():
    global 원전목록
    global ele
    global 원자력리스트
    원자력리스트.원전초기화()

    for item in ele:
        원전목록 += [item]


    for i in 원전목록:
        n = i.find('expl')
        c = i.find('name')
        t = i.find('time')
        v = i.find('value')
        원자력리스트.원전추가(원자력발전소(n.text, c.text, t.text, v.text))
    원자력리스트.목록출력()

#--------------------------------------------------------------------------#
def mSearch():
    global ele
    global 원전목록
    global 원자력리스트

    원자력리스트.원전초기화()
    원전이름 = 0
    st = input('원전 검색.  : 월성 고리 한빛  한울 ')

    if st == '월성':
        원전이름 = 2100
    elif st == '고리':
        원전이름 = 2200
    elif st == '한빛':
        원전이름 = 2300
    elif st == '한울':
        원전이름 = 2400
    else:
        print('없는 원전 입니다.')
        return False

    for item in ele:
        val = item.find('name')
        s=val.text
        if s.find(str(원전이름)) != -1:
            원전목록+=[item]

    for i in 원전목록:
        n=i.find('expl')
        c=i.find('name')
        t=i.find('time')
        v=i.find('value')
        원자력리스트.원전추가(원자력발전소(n.text,c.text,t.text,v.text))
    원자력리스트.목록출력()

#--------------------------------------------------------------------------#

def uSort():
    global 원자력리스트
    원자력리스트.원전정렬()
    원자력리스트.목록출력()

def dSort():
    global 원자력리스트
    원자력리스트.원전정렬(upper=False)
    원자력리스트.목록출력()


def Menu():
    global mquit
    print('메뉴를 선택하시오.')
    print('원전 전체 목록 : a')
    print('원전 검색 : s')
    print('원전 오름차순 정렬 : us ')
    print('원전 내림차순 정렬 : ds ')
    print('방사능 측정값 이메일 전송 : m')
    print('종료 : q')
    s=input('원하는 메뉴를 입력')

    if s=='a':
        AllList()
    elif s=='s':
        mSearch()
    elif s == 'us':
        uSort()
    elif s == 'ds':
        dSort()
    elif s == 'q':
        mquit = -1
    elif s =='m':
        원자력리스트.메일발송()
    else:
        pass



while(mquit>0):
    Menu()
print('정상적으로 종료되었습니다.')
