from django.shortcuts import render
from django.http import JsonResponse
from .forms import SelectCharacter
from django.views.generic import View
from pprint import pprint
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 '}

cookies = {'POESESSID': '16418e854515def66e5d3a14c74bfc6a'}

def characterList(request):


    if request.method == 'GET':

        url = 'https://www.pathofexile.com/character-window/get-characters?accountName=R33son'

        r = requests.get(url, headers=headers, cookies=cookies)

        results = r.json()

        characters = [{'name': character['name'], 'class': character['class'], 'level': character['level'], 'league': character['league']} for character in results]
       
        context = {
            'characters': characters,
            'title': 'Select character',
        }


        return render(request, 'user/detail.html', context)

    elif request.method == 'POST':

        
        url = f"https://www.pathofexile.com/character-window/get-items?accountName=R33son&character={request.POST['character']}"

        r = requests.get(url, headers=headers, cookies=cookies)

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
                rarity = item.get('frameType')
                name = item.get('name')
                height = item.get('h')
            
                items.append({
                        'typeLine': item['typeLine'], 
                        'icon': item['icon'], 
                        'type': item['inventoryId'],
                        'flask': flask_id,
                        'implicitMods': implicitMods,
                        'explicitMods': explicitMods,
                        'craftedMods': craftedMods,
                        'enchantMods': enchantMods,
                        'name': name,
                        'rarity': rarity,
                        'height': height
                    })

        context = {
            'title': 'Character equipement',
            'items': items,
        }

        return render(request, 'user/detail.html', context)


def characterDetail(request):

    if request.is_ajax and request.method == "GET":


        if "character_name" in request.GET:

            url = f"https://www.pathofexile.com/character-window/get-items?accountName=R33son&character={request.GET['character_name']}"

            r = requests.get(url, headers=headers, cookies=cookies)

            results = r.json()

            items = []
            for item in results['items']:
                if item['inventoryId'] != 'MainInventory' and item['inventoryId'] !='Offhand2'and item['inventoryId'] != 'Weapon2':

                    
                    if item['inventoryId'] == 'Flask':
                        flask_id = str(item['x']+1)
                    else:
                        flask_id = ''

                    fracturedMods = item.get('fracturedMods')
                    implicitMods = item.get('implicitMods')
                    explicitMods = item.get('explicitMods')
                    craftedMods = item.get('craftedMods')
                    enchantMods = item.get('enchantMods')
                    corrupted = item.get('corrupted')
                    rarity = item.get('frameType')
                    name = item.get('name')
                    height = item.get('h')
                
                    items.append({
                            'typeLine': item['typeLine'], 
                            'icon': item['icon'], 
                            'type': item['inventoryId'],
                            'flask': flask_id,
                            'fracturedMods': fracturedMods,
                            'implicitMods': implicitMods,
                            'explicitMods': explicitMods,
                            'craftedMods': craftedMods,
                            'enchantMods': enchantMods,
                            'corrupted': corrupted,
                            'name': name,
                            'rarity': rarity,
                            'height': height
                        })

            return JsonResponse({"character_items": items} , status=200)
        else:
            return JsonResponse({"message": "Character does not exists"}, status=400)