import websocket  #pip install websocket-client
websocket.enableTrace(False)
from ast import literal_eval as literal

def database_call(node, call):

    while 1:
        try:
            call = call.replace("'",'"') # never use single quotes
            ws = websocket.create_connection(node)
            print('')
            print((call.split(',"params":')[1]).rstrip('}'))
            print('-----------------------------------------------------------')
            ws.send(call)
            # 'result' key of literally evaluated
            # string representation of dictionary from websocket
            ret = literal(ws.recv())['result']
            print (ret)
            ws.close()
            return ret
        except Exception as e:
            print (e.args)
            pass

def account_balances(node, account_name):

    Z = '{"id":1,"method":"call","params":["database",'
    # make call for raw account balances as returned by api
    get_named_account_balances = Z + '"get_named_account_balances",["%s", [] ]]}' % (account_name)
    raw_balances = database_call(node, get_named_account_balances)
    # make list of asset_id's in raw account balances
    asset_ids = []
    for i in range(len(raw_balances)):
        asset_ids.append(raw_balances[i]['asset_id'])
    # make a second api request for additional data about each asset
    get_assets = Z + '"get_assets",[%s]]}' % asset_ids
    raw_assets = database_call(node, get_assets)
    # create a common key "asset_id" for both list of dicts
    # also extract the symbol and precision 
    id_sym_prec = []
    for i in range(len(raw_assets)):
        id_sym_prec.append({'asset_id':raw_assets[i]['id'],
                            'symbol':raw_assets[i]['symbol'],
                            'precision':raw_assets[i]['precision'], })
    # merge the two list of dicts with common key "asset_id"
    data = {}
    lists = [raw_balances, id_sym_prec]
    for each_list in lists:
       for each_dict in each_list:
           data.setdefault(each_dict['asset_id'], {}).update(each_dict)
    # convert back to list
    data = list(data.values())
    # create a new dictionary containing only the symbol and quantity
    ret = {}
    for i in range(len(data)):
        qty = float(data[i]['amount'])/10**float(data[i]['precision'])
        ret[data[i]['symbol']] = qty
    return raw_balances, ret

#node = 'wss://bts-seoul.clockwork.gr' # websocket address
node = 'wss://api.bts.mobi/wss'
account_name = 'abc123' # string
raw_balances, balances = account_balances(node, account_name)


print('')
print('balances')
print(balances)



