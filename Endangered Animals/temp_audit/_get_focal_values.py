import json
data = json.load(open('animals_data_verified.json','r',encoding='utf-8'))
problems = ['Malayan Tiger','Pygmy Hog','Roloway Monkey','Sunda Pangolin','Chinese Alligator','African Wild Dog','Okapi','Radiated Tortoise','Cuban Crocodile','Chinese Giant Salamander','Red Panda','Axolotl','Bog Turtle','Numbat','Dhole','Hirola','Asian Elephant','Malayan Tapir','Black-footed Ferret','Amami Rabbit']
for a in data:
    if a['name'] in problems:
        print(f"{a['name']:30s} fx={a.get('focal_x','center'):8s} fy={a.get('focal_y','center'):8s} spread={a.get('is_spread',False)}")
