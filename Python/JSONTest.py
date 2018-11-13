import json
name = ["Scott","Larry", "Tim"]
website = ["google.com","wikipedia.com","twitter.com"]
ffrom = ["Chile", "China", "USA"]
data = {}  
data['people'] = []  
for t in range(3):
    data['people'].append({  
        'name': name[t],
        'website': website[t],
        'from': ffrom[t]
    })


with open('Desktop/data.txt', 'w') as outfile:  
    json.dump(data, outfile)