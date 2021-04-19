from django.shortcuts import render
from django.http import JsonResponse
from pprint import pprint
import requests
import json


def get_user(request):

    headers = {'User-Agent': 'Mozilla/5.0 '}

    cookie = {'POESESSID': '16418e854515def66e5d3a14c74bfc6a'}

    if request.method == 'GET':

        url = 'https://www.pathofexile.com/character-window/get-characters?accountName=R33son'

        r = requests.get(url, headers=headers, cookies=cookie)

        results = r.json()

        names = [character['name'] for character in results]

        context = {
            'names': names,
            'title': 'Select character',
        }

        return render(request, 'user/user.html', context)

    elif request.method == 'POST':

        url = f"https://www.pathofexile.com/character-window/get-items?accountName=R33son&character={request.POST['character']}"

        r = requests.get(url, headers=headers, cookies=cookie)

        results = r.json()

        

        # list comprehation
        # items = [{'name': item['typeLine'], 'image': item['icon']} for item in results['items'] 
        #     if item['inventoryId'] != 'MainInventory' and
        #     item['inventoryId'] != 'Offhand2' and
        #     item['inventoryId'] != 'Weapon2']
        
        items = []
        for item in results['items']:
            if item['inventoryId'] != 'MainInventory' and item['inventoryId'] !='Offhand2'and item['inventoryId'] != 'Weapon2':

                
                if item['inventoryId'] == 'Flask':
                    flask_id = str(item['x']+1)
                else:
                    flask_id = ''

                implicitMods = item.get('implicitMods')
                explicitMods = item.get('explicitMods')
                craftedMods = item.get('craftedMods')
                enchantMods = item.get('enchantMods')
                height = item.get('h')
                
                

                items.append({
                        'name': item['typeLine'], 
                        'icon': item['icon'], 
                        'type': item['inventoryId'],
                        'flask': flask_id,
                        'implicitMods': implicitMods,
                        'explicitMods': explicitMods,
                        'craftedMods': craftedMods,
                        'enchantMods': enchantMods,
                        'height': height
                    })

        #import ipdb; ipdb.set_trace()
        
        pprint(items)

        context = {
            'title': 'Character equipement',
            'items': items,


        }
        return render(request, 'user/detail.html', context)
