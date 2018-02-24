def reverse(string):

    s=tolist(string)
    l=0
    r=len(s)-1
    while(l<r):
        if not isalphabet(s[l]):
            l+=1
        elif not isalphabet(s[l]):
            R-=1
        else:
            s[l],s[r]=swap(s[l],s[r])
            l+=1
            r-=1
    return tostring(s)

def isalphabet(x):
    return x.isalpha()

def tolist(string):
    s=[]
    for i in string:
        s.append(i)
    return s

def tostring(s):
    return ''.join(s)

def swap(a,b):
    return (b,a)



string="a!!!b.c.d,e'f,ghi"
string=reverse(string)
print("the output is:"+string)
