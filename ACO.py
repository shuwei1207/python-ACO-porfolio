# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:51:56 2019

@author: USER
"""
import pandas as pd
import matplotlib.pyplot as plt

n=737 #天數
stock = pd.read_excel("stock.xlsx")
data = pd.read_excel("data.xlsx")

#報酬率
ROI1 = []
ROI2 = []
ROI3 = []
ROI4=  []

for i in range(n-1+6):
    R1=(stock.iloc[0,i+1]-stock.iloc[0,i]) / stock.iloc[0,i]
    R2=(stock.iloc[1,i+1]-stock.iloc[1,i]) / stock.iloc[1,i]
    R3=(stock.iloc[2,i+1]-stock.iloc[2,i]) / stock.iloc[2,i]
    R4= 0.00001
    
    ROI1.append(R1)
    ROI2.append(R2)
    ROI3.append(R3)
    ROI4.append(R4)

#個股能見度
r11 = []
r12 = []
r13 = []
    
for i in range(6,n-1+6):
    r1 = ROI1[i] + 0.15
    r2 = ROI2[i] + 0.15
    r3 = ROI3[i] + 0.15
        
    r11.append(r1)
    r12.append(r2)
    r13.append(r3)
    
    
#類股能見度
r21 = []
r22 = []
r23 = []
    
for i in range(6,n-1+6):
    s1 = ROI1[i] + 0.1
    s2 = ROI2[i] + 0.1
    s3 = ROI3[i] + 0.1
        
    r21.append(s1)
    r22.append(s2)
    r23.append(s3)
    
#銀行能見度
r14 = []
r24 = []
r34 = []

for i in range(6,n-1+6):
    b1 = 0.00001 + 0.15
    b2 = 0.00001 + 0.1
    b3 = 0.00001 + 0.1
        
    r14.append(b1)
    r24.append(b2)
    r34.append(b3)
    
#漲跌幅能見度
r31 = []
r32 = []
r33 = []

for i in range(6,n-1+6):
    t1 = 0.1-( max(0,ROI1[i-3]) * max(0,ROI1[i-2]) *max(0,ROI1[i-1])+ min(0,ROI1[i-3]) * min(0,ROI1[i-2]) *min(0,ROI1[i-1]) )*1000
    t2 = 0.1-( max(0,ROI2[i-3]) * max(0,ROI2[i-2]) *max(0,ROI2[i-1])+ min(0,ROI2[i-3]) * min(0,ROI2[i-2]) *min(0,ROI2[i-1]) )*1000
    t3 = 0.1-( max(0,ROI3[i-3]) * max(0,ROI3[i-2]) *max(0,ROI3[i-1])+ min(0,ROI3[i-3]) * min(0,ROI3[i-2]) *min(0,ROI3[i-1]) )*1000
        
    r31.append(t1)
    r32.append(t2)
    r33.append(t3)

#交易量變化量
D1 = []
D2 = []
D3 = []

for i in range(n-1+6):
    d1= data.iloc[0,i+1] / data.iloc[0,i]
    d2= data.iloc[1,i+1] / data.iloc[1,i]
    d3= data.iloc[2,i+1] / data.iloc[2,i]
    
    D1.append(d1)
    D2.append(d2)
    D3.append(d3)

#殘留費洛蒙
delta_f1 = []
delta_f2 = []
delta_f3 = []
delta_f4 = []

for i in range(6,n-1+6):
    z1= D1[i] / (1/6 *(D1[i-6]+D1[i-5]+D1[i-4]+D1[i-3]+D1[i-2]+D1[i-1])) 
    z2= D2[i] / (1/6 *(D2[i-6]+D2[i-5]+D2[i-4]+D2[i-3]+D2[i-2]+D2[i-1]))
    z3= D3[i] / (1/6 *(D3[i-6]+D3[i-5]+D3[i-4]+D3[i-3]+D3[i-2]+D3[i-1]))
    
    delta_f1.append(z1)
    delta_f2.append(z2)
    delta_f3.append(z3)
    
for i in range(n-1):
    delta_f4.append( (1/3) * (pow(delta_f1[i],-1)+pow(delta_f2[i],-1)+pow(delta_f3[i],-1)) )
    
s = 0.0 #蒸發費洛蒙比率

#真正的費洛蒙
f1 = []
f2 = []
f3 = []
f4 = []
f1.append(1.0)#要留值
f2.append(1.0)
f3.append(1.0)
f4.append(1.0)

for i in range(n-2):
    y1= s*f1[i] + delta_f1[i+1]
    y2= s*f2[i] + delta_f2[i+1]
    y3= s*f3[i] + delta_f3[i+1]
    y4= s*f4[i] + delta_f4[i+1]
    
    f1.append(y1)
    f2.append(y2)
    f3.append(y3)
    f4.append(y4)

#weight
alpha = 1
beta = 1
gama = 1
lamda =1

w1 = []
w2 = []
w3 = []
w4 = []

for i in range(n-1):
    z1= pow(f1[i],alpha)* pow(r11[i],beta)*pow(r21[i],gama)*pow(r31[i],lamda)
    z2= pow(f2[i],alpha)* pow(r12[i],beta)*pow(r22[i],gama)*pow(r32[i],lamda)
    z3= pow(f3[i],alpha)* pow(r13[i],beta)*pow(r23[i],gama)*pow(r33[i],lamda)
    z4= pow(f4[i],alpha)* pow(r14[i],beta)*pow(r24[i],gama)*pow(r34[i],lamda)
    
    w1.append(z1)
    w2.append(z2)
    w3.append(z3)
    w4.append(z4)

#各資產比例
    
p1=[]
p2=[]
p3=[]
p4=[]

for i in range(n-1):
    x1= w1[i] / ( w1[i]+ w2[i]+ w3[i]+ w4[i])
    x2= w2[i] / ( w1[i]+ w2[i]+ w3[i]+ w4[i])
    x3= w3[i] / ( w1[i]+ w2[i]+ w3[i]+ w4[i])
    x4= w4[i] / ( w1[i]+ w2[i]+ w3[i]+ w4[i])
    
    p1.append(x1)
    p2.append(x2)
    p3.append(x3)
    p4.append(x4)

#資產配置ACO
initmoney = 10000000 #初始金額

money1 =[]
money2 =[]
money3 =[]
money4 =[]
total=[]

m1= initmoney*p1[i]
m2= initmoney*p2[i]
m3= initmoney*p3[i]
m4= initmoney*p4[i]
mr= m1 + m2 + m3 + m4

money1.append(m1)
money2.append(m2)
money3.append(m3)
money4.append(m4)
total.append(mr)
    
for i in range(n-1):
    m1= total[i]*p1[i]*(1+ROI1[i])
    m2= total[i]*p2[i]*(1+ROI2[i])
    m3= total[i]*p3[i]*(1+ROI3[i])
    m4= total[i]*p4[i]*(1+ROI4[i])
    mr= m1 + m2 + m3 + m4
    
    money1.append(m1)
    money2.append(m2)
    money3.append(m3)
    money4.append(m4)
    total.append(mr)

#標準系統
st_initmoney = 10000000 #初始金額

st_money1 =[]
st_money2 =[]
st_money3 =[]
st_money4 =[]
st_total=[]

st_m1= st_initmoney*0.25
st_m2= st_initmoney*0.25
st_m3= st_initmoney*0.25
st_m4= st_initmoney*0.25
st_mr= st_m1 + st_m2 + st_m3 + st_m4

st_money1.append(st_m1)
st_money2.append(st_m2)
st_money3.append(st_m3)
st_money4.append(st_m4)
st_total.append(st_mr)
    
for i in range(n-1):
    st_m1= st_total[i]*0.25*(1+ROI1[i])
    st_m2= st_total[i]*0.25*(1+ROI2[i])
    st_m3= st_total[i]*0.25*(1+ROI3[i])
    st_m4= st_total[i]*0.25*(1+ROI4[i])
    st_mr= st_m1 + st_m2 + st_m3 + st_m4
    
    st_money1.append(st_m1)
    st_money2.append(st_m2)
    st_money3.append(st_m3)
    st_money4.append(st_m4)
    st_total.append(st_mr)

plt.plot(total, color='red', label="ACO") #ACO
plt.plot(st_total, color='blue',label="標準系統") #標準系統
plt.show()