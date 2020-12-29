import time

lst = []
f = time.time() + 2
while f > time.time():
    #x = getch.getch()
    x = 5
    print(x)
    lst.append(x)
print("\n")
print(lst)
