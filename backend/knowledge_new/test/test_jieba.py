
import jieba

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  






step1=jieba.lcut("如何学习Python") 
print(step1)
seg_set1=set(step1)

step2=jieba.lcut("如何学习Java")  

seg_set2=set(step2)


print(seg_set1)
print(seg_set2)
