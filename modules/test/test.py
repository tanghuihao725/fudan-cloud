import time

# path_arr = __file__.split('/')
# path = "/".join(path_arr[0: -1])
path = "."

localtime = time.asctime( time.localtime(time.time()) )

with open('./prediction.txt', 'r') as f:
    content = []
    line = f.readline()
    while line:
        content.append(line[:])
        line = f.readline()
    content_str = "".join(content)


with open('./result.txt', 'w') as f:
    f.write('Your Data: ' + content_str + " ")
    f.write(localtime + " result for module test")
    print("result done")