import time

localtime = time.asctime( time.localtime(time.time()) )

with open('./predictData.txt', 'r') as f:
    content = []
    line = f.readline()
    while line:
        content.append(line[:])
        line = f.readline()
    content_str = "".join(content)


with open('result/predictResult.txt', 'w') as f:
    f.write('Your Data: ' + content_str + " ")
    f.write(localtime + " result for module test")
    print("result done")