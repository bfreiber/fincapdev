import json

def json_connections(friend_list):
    children = []
    for friend in friend_list:
        children.append({'name': friend[0] + ' ' + friend[1], 'pic': friend[2]})
    res = {"name": "Me", "children": children}
    return json.dumps(res)
