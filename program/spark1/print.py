import numpy as np

v1=np.loadtxt("IM12.txt", delimiter=",")
print ("M12")
for i in v1:
    print (i)

v2=np.loadtxt("IM21.txt", delimiter=",")
print ("M21")
for x in v2:
    print (x)
v3=np.loadtxt("IM13.txt", delimiter=",")
print ("M13")
for y in v3:
    print (y)


v4=np.loadtxt("IM31.txt", delimiter=",")

print ("M31")
for z in v4:
    print (z)


v5=np.loadtxt("IM32.txt", delimiter=",")
print ("M32")
for c in v5:
    print (c)


v6=np.loadtxt("IM23.txt", delimiter=",")

print ("M23")
for z in v6:
    print (z)



v7=np.loadtxt("IC12.txt", delimiter=",")
print ("IC12")
for z in v7:
    print (z)


v8=np.loadtxt("IC21.txt", delimiter=",")
print ("C21")
for z in v8:
    print (z)
v9=np.loadtxt("IC13.txt", delimiter=",")
print ("M13")
for z in v9:
    print (z)
v10=np.loadtxt("IC31.txt", delimiter=",")
print ("C31")
for z in v10:
    print (z)
v11=np.loadtxt("IC32.txt", delimiter=",")
print ("C32")
for z in v11:
    print (z)
v12=np.loadtxt("IC23.txt", delimiter=",")
print ("C23")
for z in v12:
    print (z)