import json
data = json.load(open('animals_data_verified.json','r',encoding='utf-8'))
zero_face = ['Roloway Monkey','Sunda Pangolin','Chinese Alligator','African Wild Dog','Okapi','Dhole','Hirola','Black-footed Ferret']
for a in data:
    if a['name'] in zero_face:
        img_path = 'images/' + a['image_url'].split('/')[-1]
        print(a['name'], '->', img_path)
