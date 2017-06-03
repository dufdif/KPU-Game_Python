from http.client import HTTPConnection
from xml.etree import ElementTree
import smtplib
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from tkinter import *

host = 'smtp.gmail.com'
port = '587'
sender='dufdif10@gmail.com'
reciver=''

app=''
radiostate='normal'
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
    원전목록 = []
    ele = tree.getiterator('item')

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
    원전목록=[]
    ele = tree.getiterator('item')
#--------------------------------------------------------------------------#

def uSort():
    global 원자력리스트
    원자력리스트.원전정렬()
    원자력리스트.목록출력()

def dSort():
    global 원자력리스트
    원자력리스트.원전정렬(upper=False)
    원자력리스트.목록출력()

def sel():
   selection = "You selected the option " + str(radiostate.get())
   label=Label()
   label.config(text = selection)
   label.place(x=500,y=300)

def Menu():
    global app
    global radiostate
    app=Tk()
    app.title('원전 주변 방사능')

    title=Label(app,text='* 원전 방사능 측정 *',font='helvetica 17')
    title.pack()
    title.place(x=340,y=20)

    b1=Button(app,text='모든원전',font='bold 15',fg='red',bg='yellow')
    b1.pack()
    b1.place(x=265,y=77)
    search=Entry(app,bg='black',fg='white',borderwidth=6,relief='sunken')
    search.pack()
    search.place(x=50,y=80)
    b2=Button(app,text='검색!',bg='white',fg='black',font='helvetica 15')
    b2.pack()
    b2.place(x=200,y=77)

    lb=Listbox(app,width=50,height=20)

    lb.pack()
    lb.place(x=50, y=220)
    lb.config(relief='solid', borderwidth=3)

    lblabel=Label(app,text='원전 목록',font='bold 15')
    lblabel.place(x=175,y=200)

    radiolabel=Label(app,text='정렬',font='bold 11',fg='black',bg='gold')
    radiolabel.place(x=50,y=120)

    radiostate=IntVar()
    rb1=Radiobutton(app,text='오름차순',variable=radiostate,value=1,command=sel)
    rb2=Radiobutton(app,text='내림차순',variable=radiostate,value=2,command=sel)
    rb1.place(x=90,y=120)
    rb2.place(x=160,y=120)

    for i in range(50):
        lb.insert(i,str(i))


    app.configure(width=900, height=600)
Menu()
app.mainloop()



