import pandas as pd
 
img_list=[]
lable_list=[]
for i in range(1,10):
    i = i +1
    img_list.append(i)
    label="aa"
    lable_list.append(label)
 
df = pd.DataFrame({"filename": img_list, "label": lable_list})
df.to_csv('result.csv',index=False)

# df = pd.DataFrame({'name': ['Raphael', 'Donatello'],
#                    'mask': ['red', 'purple'],
#                    'weapon': ['sai', 'bo staff']})
# df.to_csv('name.csv',index=False)