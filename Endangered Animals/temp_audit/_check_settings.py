import json

with open('animals_data_verified.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

names = ['Indian Rhinoceros','Bornean Elephant','Polar Bear','California Condor',
         'Northern Hoolock Gibbon','Balkan Lynx','Tasmanian Devil','Sumatran Rhinoceros',
         'Tamaraw','Wild Bactrian Camel','Aye-aye','Grevy\'s Zebra','Siberian Tiger',
         'Snow Leopard','Amami Rabbit','Tapanuli Orangutan','Pygmy Hog','Black-footed Ferret']

for a in d:
    if a['name'] in names:
        print(f"{a['name']:30s} img={a.get('image_url','?'):35s} fx={a.get('focal_x','center'):8s} fy={a.get('focal_y','center'):8s} box={a.get('BOX_POSITION','?')}")
