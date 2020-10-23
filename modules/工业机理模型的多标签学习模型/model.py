import jieba.analyse
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--test_dir', type=str, default='./sample.txt')
parser.add_argument('--tags_dir', type=str, default='./result/predictResult.txt')
parser.add_argument('--method', type=str, default='tf-idf')
parser.add_argument('--topK', type=int, default=20)
args = parser.parse_args()

if __name__ == "__main__":
    k=args.topK
    method=args.method
    test_dir=args.test_dir
    tags_dir=args.tags_dir
    with open(test_dir,'r',encoding='UTF-8') as f:
        lines=f.readlines()
        text=''.join(lines)
        jieba.analyse.set_stop_words("./stop_words.txt")
        if method=='tf-idf':
            #tags = jieba.analyse.extract_tags(text, topK=k,allowPOS=('n', 'vn','m','q'))
            tags = jieba.analyse.extract_tags(text, topK=k)
            print(u"关键词:")
            print(" ".join(tags))
            with open(tags_dir,'w',encoding='UTF-8') as w:
                w.write(" ".join(tags))
        elif method=='textrank':
            #tags=jieba.analyse.textrank(text,topK=k,allowPOS=('n', 'vn', 'm','q'))
            tags=jieba.analyse.textrank(text,topK=k)
            print(u"关键词:")
            print(" ".join(tags))
            with open(tags_dir,'w',encoding='UTF-8') as w:
                w.write(" ".join(tags))
        else:
            print("请输入正确的method")
