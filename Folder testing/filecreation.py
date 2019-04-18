
def create_file():
    file = open("test.txt","w+")

def create_n_file(n):
    for i in range(n):
        filename = "test"+str(i)+".txt"
        file = open(filename,"w+")


create_n_file(3)