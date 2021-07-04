import json
from nameparser import HumanName

with open('ACM.json') as f:
  data = json.load(f)

num_items = len(data['documents'])

# For each item, delete unnecessary author info
for i in range(num_items):
    for j in range(len(data['documents'][i]['info']['authors']['author'])):
        del data['documents'][i]['info']['authors']['author'][j]['@pid']

# For each item, delete unnecessary info if it exists
for i in range(num_items):
    del data['documents'][i]['@score']
    del data['documents'][i]['@id']
    del data['documents'][i]['url']
    del data['documents'][i]['info']['venue'] 
    del data['documents'][i]['info']['year']
    del data['documents'][i]['info']['type']
    del data['documents'][i]['info']['key'] 
    try:
        del data['documents'][i]['info']['ee']
    except KeyError:
        print("Missing doi link for entry " + data['documents'][i]['info']['title'])
        pass   
    del data['documents'][i]['info']['url']
    try:
        del data['documents'][i]['info']['pages']
    except KeyError:
        print("Missing page numbers for entry " + data['documents'][i]['info']['title'])
        pass  
    try:
        del data['documents'][i]['info']['doi']
    except KeyError:
        print("Missing doi for entry " + data['documents'][i]['info']['title'])
        pass  

# UNCOMMENT BELOW 2 LINES WHEN RUNNING FOR THE FIRST TIME
#with open('ACM_cleaned.json', 'w') as json_file:
 #   json.dump(data, json_file) 

# I took ACM_cleaned and manually removed some errors (extra spaces, etc). Opening up this edited version...
with open('ACM_cleaned.json') as f:
    data = json.load(f)
    
# Split each author name string according to common naming formats  
for i in range(num_items):
    for j in range(len(data['documents'][i]['info']['authors']['author'])):
        name = HumanName(data['documents'][i]['info']['authors']['author'][j]['text']).as_dict(False)
        # first case: author has first, middle, and last names
        if 'first' in name and 'middle' in name and 'last' in name:
            data['documents'][i]['info']['authors']['author'][j]['first_name'] = name['first'] + ' ' + name['middle']
            data['documents'][i]['info']['authors']['author'][j]['last_name'] = name['last']
        # second case: author only has one name    
        elif 'first' in name and 'middle' not in name and 'last' not in name:
            data['documents'][i]['info']['authors']['author'][j]['first_name'] = name['first']   
        # third case: author only has first and last names
        elif 'first' in name and 'middle' not in name and 'last' in name:
            data['documents'][i]['info']['authors']['author'][j]['first_name'] = name['first']
            data['documents'][i]['info']['authors']['author'][j]['last_name'] = name['last']
        # delete the original text field that contained the author's full name, since names are split now   
        del data['documents'][i]['info']['authors']['author'][j]['text']

# Re-level the JSON data; 'info' and 'author' fields not needed            
for i in range(num_items):
    data['documents'][i] = data['documents'][i]['info']
    data['documents'][i]['authors'] = data['documents'][i]['authors']['author']                 
             
# Save to new json
with open('ACM_final.json', 'w') as json_file:
    json.dump(data, json_file) 
                    
