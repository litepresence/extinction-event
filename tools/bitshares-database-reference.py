#Python3

' Bitshares Database Api Websocket Calls Pocket Reference'

# https://github.com/bitshares/bitshares-core/blob/master/libraries/app/database_api.cpp#L77

'litepresence 2018'

import websocket  #pip install websocket-client
websocket.enableTrace(False)

# EXAMPLE DATABASE REQUEST PARAMETERS
node = 'wss://api.bts.mobi/wss'#'wss://bts-seoul.clockwork.gr' # websocket address
asset = 'BTS' # symbol
currency = 'OPEN.BTC' #symbol
start = '2017-01-01T11:22:33' # iso date
stop = '2018-01-01T11:22:33' # iso date
account_name = 'litepresence1' # string
account_names = '["xeroc", "litepresence1"]' # list of string names
account_id = '1.2.743179' # a.b.c vector
block_num = 26444444 # int block number 
block_nums = [26444444, 26444445, 26444446] # list of block numbers
trx_in_block = 4 # int index of item
transaction_id = '1.7.66209049'
transaction_id_type = 'cancel'
skip_order_book = 'false' # bool - non pythonic 'true' or 'false'
limit = 5 # int depth of data called
object_id_type = '' # a.b.c vector
object_ids = []
asset_id = '1.3.0'
asset_id2 = '1.3.861'
subscribe = 'false' # bool - non pythonic 'true' or 'false'
public_key = "BTS7d4MpYzecprWMfso8f6o1Ln8fQyxuQGD5LM83PRTfQBkodk4Ck"
witness_id = '1.6.65'
trx = '{"expiration":"2018-04-27T14:16:35","extensions":[],"operation_results":[[1,"1.7.66407704"]],"operations":[[1,{"amount_to_sell":{"amount":71055254,"asset_id":"1.3.0"},"expiration":"2018-05-04T14:16:04","extensions":[],"fee":{"amount":578,"asset_id":"1.3.0"},"fill_or_kill":false,"min_to_receive":{"amount":1922091,"asset_id":"1.3.121"},"seller":"1.2.879926"}]],"ref_block_num":8413,"ref_block_prefix":4199813419}'

# '{"id":1,"method":"call","params":["database","get_ticker",["OPEN.BTC","BTS"]]}'
Z = '{"id":1,"method":"call","params":["database",'

'Objects'
get_objects                     = Z + ''

'Subscriptions'
set_subscribe_callback          = Z + ''
set_pending_transaction_callback = Z + ''
set_block_applied_callback      = Z + ''
cancel_all_subscriptions        = Z + ''

'Blocks and transactions'
get_block_header                = Z + '"get_block_header",["%s"]]}' % block_num
get_block_header_batch          = Z + '"get_block_header_batch",["%s"]]}' % (block_nums)
get_block                       = Z + '"get_block",["%s"]]}' % block_num
get_transaction                 = Z + '"get_transaction",["%s", "%s"]]}' % (block_num, trx_in_block)
get_recent_transaction_by_id    = Z + ''

'Globals' # DONE
get_chain_properties            = Z + '"get_chain_properties",[]]}'
get_global_properties           = Z + '"get_global_properties",[]]}'
get_config                      = Z + '"get_config",[]]}'
get_chain_id                    = Z + '"get_chain_id",[]]}'
get_dynamic_global_properties   = Z + '"dynamic_global_properties",[]]}'

'Keys' 
get_key_references              = Z + '"get_key_references",[["%s",]]]}' % public_key
is_public_key_registered        = Z + '"is_public_key_registered",["%s"]]}' % public_key

'Accounts'
get_accounts                    = Z + '"get_accounts",[["%s",]]]}' % account_id
get_full_accounts               = Z + '"get_full_accounts",[["%s",],%s]]}' % (account_name, subscribe)
get_account_by_name             = Z + '"get_account_by_name",["%s"]]}' % account_name
get_account_references          = Z + '"get_account_references",["%s",]]}' % account_id
lookup_account_names            = Z + '"lookup_account_names",[%s]]}' % account_names
lookup_accounts                 = Z + '"lookup_accounts",["%s", "%s"]]}' % (account_name, limit)
get_account_count               = Z + '"get_account_count",[]]}'

'Balances'
get_account_balances            = Z + '"get_account_balances",["%s", [] ]]}' % (account_id)
get_named_account_balances      = Z + '"get_named_account_balances",["%s", [] ]]}' % (account_name)
get_balance_objects             = Z + ''
get_vested_balances             = Z + ''
get_vesting_balances            = Z + '"get_vesting_balances",["%s"]]}' % account_id

'Assets'
get_assets                      = Z + '"get_assets",[["%s",]]]}' % asset_id
list_assets                     = Z + '"list_assets",["%s","%s"]]}' % (asset, limit)
lookup_asset_symbols            = Z + '"lookup_asset_symbols",[["%s",]]]}' % asset

'Markets / feeds'
get_order_book                  = Z + '"get_order_book",["%s","%s","%s"]]}' % (currency, asset, limit)
get_limit_orders                = Z + '"get_limit_orders",["%s","%s","%s"]]}' % (asset_id, asset_id2, limit)
get_call_orders                 = Z + '"get_call_orders",["%s","%s"]]}' % (asset_id, limit)
get_settle_orders               = Z + '"get_settle_orders",["%s","%s"]]}' % (asset_id, limit)
get_margin_positions            = Z + '"get_margin_positions",["%s"]]}' % account_id
get_collateral_bids             = Z + ''
subscribe_to_market             = Z + ''
unsubscribe_from_market         = Z + ''
get_ticker                      = Z + '"get_ticker",["%s","%s","%s"]]}' % (currency, asset, skip_order_book)
get_24_volume                   = Z + '"get_24_volume",["%s","%s"]]}' % (currency, asset)
get_top_markets                 = Z + '"get_top_markets",["%s"]]}' % limit
get_trade_history               = Z + '"get_trade_history",["%s","%s","%s","%s","%s"]]}' % (currency, asset, start, stop, limit)
get_trade_history_by_sequence   = Z + ''

'Witnesses'
get_witnesses                   = Z + ''
get_witness_by_account          = Z + '"get_witness_by_account",["%s"]]}' % witness_id
lookup_witness_accounts         = Z + '"lookup_witness_accounts",["%s","%s"]]}' % (witness_id, limit)
get_witness_count               = Z + '"get_witness_count",[]]}'

'Committee members'
get_committee_members           = Z + ''
get_committee_member_by_account = Z + ''
lookup_committee_member_accounts = Z + ''
get_committee_count             = Z + '"get_committee_count",[]]}'

'Workers'
get_all_workers                 = Z + ''
get_workers_by_account          = Z + ''
get_worker_count                = Z + '"get_worker_count",[]]}'

'Votes'
lookup_vote_ids = Z + ''

'Authority / validation'
get_transaction_hex             = Z + '"get_transaction_hex",[%s]]}' % trx
get_required_signatures         = Z + ''
get_potential_signatures        = Z + '"get_potential_signatures",[%s]]}' % trx
get_potential_address_signatures  = Z + '"get_potential_address_signatures",[%s]]}' % trx
verify_authority                = Z + '"verify_authority",[%s]]}' % trx
verify_account_authority        = Z + ''
validate_transaction            = Z + '"validate_transaction",[%s]]}' % trx
get_required_fees               = Z + ''

'Proposed transactions'
get_proposed_transactions = Z + '"get_proposed_transactions",["%s"]]}' % account_id

'Blinded balances'
get_blinded_balances = Z + ''

'Withdrawals'
get_withdraw_permissions_by_giver = Z + ''
get_withdraw_permissions_by_recipient = Z + ''


all_calls = [get_objects,set_subscribe_callback,set_pending_transaction_callback,set_block_applied_callback,cancel_all_subscriptions,get_block_header,get_block_header_batch,get_block,get_transaction,get_recent_transaction_by_id,get_chain_properties,get_global_properties,get_config,get_chain_id,get_dynamic_global_properties,get_key_references,is_public_key_registered,get_accounts,get_full_accounts,get_account_by_name,get_account_references,lookup_account_names,lookup_accounts,get_account_count,get_account_balances,get_named_account_balances,get_balance_objects,get_vested_balances,get_vesting_balances,get_assets,list_assets,lookup_asset_symbols,get_order_book,get_limit_orders,get_call_orders,get_settle_orders,get_margin_positions,get_collateral_bids,subscribe_to_market,unsubscribe_from_market,get_ticker,get_24_volume,get_top_markets,get_trade_history,get_trade_history_by_sequence,get_witnesses,get_witness_by_account,lookup_witness_accounts,get_witness_count,get_committee_members,get_committee_member_by_account,lookup_committee_member_accounts,get_committee_count,get_all_workers,get_workers_by_account,get_worker_count,lookup_vote_ids,get_transaction_hex,get_required_signatures,get_potential_signatures,get_potential_address_signatures,verify_authority,verify_account_authority,validate_transaction,get_required_fees,get_proposed_transactions,get_blinded_balances,get_withdraw_permissions_by_giver,get_withdraw_permissions_by_recipient,]


object_calls = []

subscription_calls = []

block_calls =      [get_block,
                    get_block_header,
                    get_block_header_batch,
                    get_transaction]

global_calls =     [get_chain_properties,
                    get_global_properties,
                    get_config,
                    get_chain_id,
                    get_dynamic_global_properties]

key_calls =        [get_key_references,
                    is_public_key_registered]

account_calls =    [get_accounts,
                    get_full_accounts,
                    get_account_by_name,
                    get_account_references,
                    lookup_account_names,
                    lookup_accounts,
                    get_account_count]

asset_calls =      [get_assets,
                    list_assets,
                    lookup_asset_symbols]

balance_calls =    [get_account_balances,
                    get_named_account_balances,
                    get_vesting_balances]

market_calls =     [get_order_book,
                    get_ticker,
                    get_trade_history,
                    get_limit_orders,
                    get_call_orders,
                    get_settle_orders,
                    get_margin_positions,
                    get_24_volume,
                    get_top_markets, ]

witness_calls =    [get_witness_by_account,
                    lookup_witness_accounts,
                    get_witness_count]

committe_calls =   [get_committee_count]

worker_calls =     [get_worker_count]

vote_calls = []

authority_calls =  [get_transaction_hex,
                    get_potential_signatures,
                    get_potential_address_signatures,
                    verify_authority,
                    validate_transaction]

proposed_calls = []
blindied_calls = []
withdrawal_calls = []


for call in asset_calls:

    try:
        ws = websocket.create_connection(node)
        print('')
        print((call.split(',"params":')[1]).rstrip('}'))
        print('-----------------------------------------------------------')
        ws.send(call)
        ret = ws.recv()
        print (ret)
        ws.close()
    except Exception as e:
        print (e.args)
        pass

# you can also make https requests in this manner
'''
import requests
data = '{"id":1,"method":"call","params":["database","get_ticker",["CNY","USD"]]}'
response = requests.post('https://api.bts.mobi/wss;echo', data=data)
'''


