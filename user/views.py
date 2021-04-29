from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .forms import SelectCharacter
from urllib.parse import (parse_qs, urlparse)
from collections import Counter
from pprint import pprint
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 '}

cookies = {'POESESSID': '16418e854515def66e5d3a14c74bfc6a'}

def amendSentence(string):
    string = list(string)
    newstring = ""
    # Traverse the string
    for i in range(len(string)):
  
        # Convert to lowercase if its
        # an uppercase character
        if string[i] >= 'A' and string[i] <= 'Z':
            string[i] = chr(ord(string[i]) + 32)
  
            # Print - before it
            # if its an uppercase character
            if i != 0:
                newstring += "-"
 
            # Print the character
            newstring += string[i]
  
        # if lowercase character
        # then just print
        else:
            newstring += string[i]
        
    return(newstring)

def getAllData(request):
    
    Currency_url = f'https://poe.ninja/api/data/currencyoverview?league=Standard&type=Currency'
    Fragment_url = f'https://poe.ninja/api/data/currencyoverview?league=Standard&type=Fragment'
    Oils_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Oil'
    Incubators_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Incubator'
    Scarabs_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Scarab'
    Fossils_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Fossil'
    Resonators_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Resonator'
    Essence_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Essence'
    DivinationCards_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=DivinationCard'
    Prophecies_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Prophecy'
    SkillGems_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=SkillGem'
    BaseTypes_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=BaseType'
    UniqueMaps_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=UniqueMap'
    Maps_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Map'
    UniqueJewels_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=UniqueJewel'
    UniqueFlasks_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=UniqueFlask'
    UniqueWeapons_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=UniqueWeapon'
    UniqueArmours_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=UniqueArmour'
    UniqueAccessories_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=UniqueAccessory'
    Beasts_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Beast'
    Invitations_utl = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Invitation'
    DeliriumOrb_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=DeliriumOrb'
    Watchstone_url = f'https://poe.ninja/api/data/itemoverview?league=Standard&type=Watchstone'

    currencyUrl_list = [Currency_url, Fragment_url]

    itemsUrl_list = [
        Oils_url,
        Incubators_url,
        Scarabs_url,
        Fossils_url,
        Resonators_url,
        Essence_url,
        DivinationCards_url,
        Prophecies_url,
        SkillGems_url,
        UniqueMaps_url,
        Maps_url,
        UniqueJewels_url,
        UniqueFlasks_url,
        UniqueWeapons_url,
        UniqueArmours_url,
        UniqueAccessories_url,
        Beasts_url,
        Invitations_utl,
        DeliriumOrb_url,
        Watchstone_url
    ]


    poeNinjaData = []
    
    for idx, url in enumerate(currencyUrl_list):
        qs = urlparse(url)

        if parse_qs(qs.query)['type'][0] != 'Currency':
            ninjaType = amendSentence(parse_qs(qs.query)['type'][0])+'s'
        else:
            ninjaType = amendSentence(parse_qs(qs.query)['type'][0])

   
        r = requests.get(url)
        result = r.json()
        
        items = [{'baseType': item['currencyTypeName'], 'detailsId': item['detailsId'], 'ninjaType': ninjaType} for item in result['lines']]

        poeNinjaData.extend(items)


    for url in itemsUrl_list:
        qs = urlparse(url)
        ninjaType = amendSentence(parse_qs(qs.query)['type'][0])+'s'

        r = requests.get(url)
        result = r.json()

        items = []
        
        for item in result['lines']:
            name = ''
            if item['name'] != '':
                name = item['name']
            else:
                name = item['baseType']

            items.append({
                'baseType': name,
                'detailsId': item['detailsId'], 
                'ninjaType': ninjaType})
                
        poeNinjaData.extend(items)

    with open('data.json', 'w') as jsonfile:
        json.dump(poeNinjaData, jsonfile)
    
    

def charactersAndTabs(request):

    if request.method == 'GET':

        #getAllData(request)

        characters_url = 'https://www.pathofexile.com/character-window/get-characters?accountName=R33son'
        stashTabs_url = 'https://www.pathofexile.com/character-window/get-stash-items?league=Standard&realm=pc&accountName=R33son&tabs=1'

        r_characters = requests.get(characters_url, headers=headers, cookies=cookies)
        r_stashTabs = requests.get(stashTabs_url, headers=headers, cookies=cookies)

        results_characters = r_characters.json()
        results_stashTabs = r_stashTabs.json()
        
        characters = [{'name': character['name'], 'class': character['class'], 'level': character['level'], 'league': character['league']} for character in results_characters]

        stashTabs = [{'name': stashTab['n'], 'index': stashTab['i'], 'color': stashTab['colour']} for stashTab in results_stashTabs['tabs']]
        
        context = {
            'characters': characters,
            'stashTabs': stashTabs,
            'title': 'Select character',
        }

        return render(request, 'user/detail.html', context)

def characterDetail(request):
    if request.is_ajax and request.method == 'GET':

        if 'character_name' in request.GET:

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

def stashTab(request):

    poeNinjaCurrency_baseUrl = f'https://poe.ninja/'

    if request.is_ajax and request.method == 'GET':
        
        if 'stashtab_index' in request.GET:

            
            url = f'https://www.pathofexile.com/character-window/get-stash-items?league=Standard&realm=pc&accountName=R33son&tabs=0&tabIndex={request.GET["stashtab_index"]}'
            r = requests.get(url, headers=headers, cookies=cookies)
            results = r.json()

            c = Counter()

            stash_items = []

            for item in results['items']:
                stackSize = None
                if 'stackSize' not in item:
                    c[item['typeLine']] += 1
                    stackSize = c[item['typeLine']]
                else:
                    stackSize = item['stackSize']

                name = ''
                if item['name'] != '':
                    name = item['name']
                else:
                    name = item['baseType']

                stash_items.append({
                    'league': item['league'], 
                    'frameType': item['frameType'],
                    'quantity': stackSize, 
                    'typeLine': item['typeLine'], 
                    'baseType': name, 
                    'icon': item['icon'], 
                    'name': item['name']})

            
            
            with open('data.json') as jsonfile:
                ninjaData = json.load(jsonfile)

                for idx, item in enumerate(stash_items):
                    for ninjaItem in ninjaData:
                        if ninjaItem['baseType'] == item['baseType']:
                            stash_items[idx]['ninjaUrl'] = poeNinjaCurrency_baseUrl + item['league'].lower() + '/' + ninjaItem['ninjaType'] + '/' + ninjaItem['detailsId'] 
                

            return JsonResponse({'stash_items': stash_items}, status=200)
        else:
            return JsonResponse({'message': 'tab does not exists'}, status=400)

