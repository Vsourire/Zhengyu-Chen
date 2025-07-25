import json
import pandas as pd

# load the JSON file
with open('DAO List.json', 'r', encoding='utf-8') as f:
    dao_data = json.load(f)

spaces = dao_data['data']['spaces']
# process the data source
result = []

for space in spaces:
    space_id = space['id']
    name = space['name']
    symbol = space.get('symbol')
    
    #count strategies
    strategies = space.get('strategies', [])
    strategy_names = [s['name'] for s in strategies]
    
    #count filters
    filters = space.get('filters', {})
    min_score = filters.get('minScore')
    only_members = filters.get('onlyMembers')
    
    result.append({
        'id': space_id,
        'name': name,
        'symbol': symbol,
        'strategy_names': strategy_names,
        'minScore': min_score,
        'onlyMembers': only_members
    })

# transfer to DataFrame
df = pd.DataFrame(result)

print(df)

# Symbol statistics
print("\n DAO Symbol：")
print(df[['id', 'symbol']])

# strategy statistics
print("\n DAO strategies：")
print(df[['id', 'strategy_names']])

# filter statistics
print("\n DAO filters：")
print(df[['id', 'minScore', 'onlyMembers']])
