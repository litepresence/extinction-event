# Python3
#///////////////////////////////////////////////////////////////////////
'''
Bitshares Database Api Calls Pocket Reference

Samples calls without pybitshares, using requests or websocket-client
'''
#///////////////////////////////////////////////////////////////////////

# https://github.com/bitshares/bitshares-core/blob/master/libraries/app/include/graphene/app/database_api.hpp
# https://github.com/bitshares/bitshares-core/blob/master/libraries/app/database_api.cpp

'litepresence 2018'

# tidbits:
# be sure to use double quotes on your request parameters
# try switching order of dates
# set limits to <100
# make sure lists are not in quotes

# @brief, @param, @return as published in the graphene database_api.hpp
# keys are as returned by api call
# several calls have not yet been translated, PR appreciated
#///////////////////////////////////////////////////////////////////////

# MODULES REQUIRED
import websocket # pip3 install websocket-client
import requests # pip3 install requests

import time
from datetime import datetime
from ast import literal_eval as literal
websocket.enableTrace(False)

def iso_date(unix): #'2017-01-01T11:22:33'

    return datetime.utcfromtimestamp(int(unix)).isoformat()
'''
///////////////////////////////////////////////////////////////////////
//  EXAMPLE DATABASE REQUEST ARGUMENTS
///////////////////////////////////////////////////////////////////////
'''
# websocket addresses
#node = 'wss://bts-seoul.clockwork.gr' 
node = 'wss://api.bts.mobi/wss'
#node = 'wss://eu.openledger.info/wss'

now = iso_date(time.time()) 
then = iso_date(time.time()-86400)
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
coins = [asset_id, asset_id2]
subscribe = 'false' # bool - non pythonic 'true' or 'false'
public_key = "BTS7d4MpYzecprWMfso8f6o1Ln8fQyxuQGD5LM83PRTfQBkodk4Ck"
witness_id = '1.6.65'
trx = '{"expiration":"2018-04-27T14:16:35","extensions":[],"operation_results":[[1,"1.7.66407704"]],"operations":[[1,{"amount_to_sell":{"amount":71055254,"asset_id":"1.3.0"},"expiration":"2018-05-04T14:16:04","extensions":[],"fee":{"amount":578,"asset_id":"1.3.0"},"fill_or_kill":false,"min_to_receive":{"amount":1922091,"asset_id":"1.3.121"},"seller":"1.2.879926"}]],"ref_block_num":8413,"ref_block_prefix":4199813419}'

'''
///////////////////////////////////////////////////////////////////////
// TYPICAL API CALL FORMAT
// '{"id":1,"method":"call","params":["database","x",[y]]}'
// "id" will be returned to you unchanged in response header
// "x" is one of the calls below
// "y' is in the format of one of the example arguments above
///////////////////////////////////////////////////////////////////////
'''

# NOTE: Each sample database call will begin with this string
Z = '{"id":1,"method":"call","params":["database",'

'''
/////////////
// Objects //
/////////////
'''

get_objects = Z + 'FIXME' # (const vector<object_id_type>& ids)
# @brief Get the objects corresponding to the provided IDs
# @param ids IDs of the objects to retrieve
# @return The objects retrieved, in the order they are mentioned in ids
#
# If any of the provided IDs does not map to an object, a null variant is returned in its position.

'''
///////////////////
// Subscriptions //
///////////////////
'''

set_subscribe_callback = Z + 'FIXME' # ( std::function<void(const variant&)> cb, bool notify_remove_create )
#  @brief Register a callback handle which then can be used to subscribe to object database changes
#  @param cb The callback handle to register
#  @param nofity_remove_create Whether subscribe to universal object creation and removal events.
#        If this is set to true, the API server will notify all newly created objects and ID of all
#        newly removed objects to the client, no matter whether client subscribed to the objects.
#        By default, API servers don't allow subscribing to universal events, which can be changed
#        on server startup.

set_pending_transaction_callback = Z + 'FIXME' # ( std::function<void(const variant& signed_transaction_object)> cb )
#  @brief Register a callback handle which will get notified when a transaction is pushed to database
#  @param cb The callback handle to register
#  Note: a transaction can be pushed to database and be popped from database several times while
#  processing, before and after included in a block. Everytime when a push is done, the client will
#  be notified.

set_block_applied_callback = Z + 'FIXME' # ( std::function<void(const variant& block_id)> cb )
#  @brief Register a callback handle which will get notified when a block is pushed to database
#  @param cb The callback handle to register

cancel_all_subscriptions  = Z + '"cancel_all_subscriptions",[]]}'
#  @brief Stop receiving any notifications
#  This unsubscribes from all subscribed markets and objects.


'''
/////////////////////////////
// Blocks and transactions //
/////////////////////////////
'''

get_block_header = Z + '"get_block_header",["%s"]]}' % block_num
#  @brief Retrieve a block header
#  @param block_num Height of the block whose header should be returned
#  @return header of the referenced block, or null if no matching block was found
"(['previous', 'witness', 'extensions', 'timestamp', 'transaction_merkle_root'])"


get_block_header_batch = Z + '"get_block_header_batch",[%s]]}' % (block_nums)
#  @brief Retrieve multiple block header by block numbers
#  @param block_num vector containing heights of the block whose header should be returned
#  @return array of headers of the referenced blocks, or null if no matching block was found
"(['timestamp', 'extensions', 'witness', 'previous', 'transaction_merkle_root'])"

get_block = Z + '"get_block",["%s"]]}' % block_num
# @brief Retrieve a full, signed block
# @param block_num Height of the block to be returned
# @return the referenced block, or null if no matching block was found

get_transaction = Z + '"get_transaction",["%s", "%s"]]}' % (block_num, trx_in_block)
# @brief used to fetch an individual transaction.
"(['previous', 'witness', 'extensions', 'timestamp', 'transaction_merkle_root'])"

get_recent_transaction_by_id = Z + '' # ( const transaction_id_type& id )

# If the transaction has not expired, this method will return the transaction for the given ID or
# it will return NULL if it is not known.  Just because it is not known does not mean it wasn't
# included in the blockchain.

'''
/////////////
// Globals //
/////////////
'''

get_chain_properties  = Z + '"get_chain_properties",[]]}'
# @brief Retrieve the @ref chain_property_object associated with the chain
"(['chain_id', 'id', 'immutable_parameters'['min_committee_member_count', 'min_witness_count', 'num_special_accounts', 'num_special_assets']])"

get_global_properties = Z + '"get_global_properties",[]]}'
# @brief Retrieve the current @ref global_property_object
"(['chain_id', 'id', 'immutable_parameters'['min_committee_member_count', 'min_witness_count', 'num_special_accounts', 'num_special_assets']])"

get_config = Z + '"get_config",[]]}'
# @brief Retrieve compile-time constants
"([**large dictionary of GRAPHENE constants**])"

get_chain_id = Z + '"get_chain_id",[]]}'
# @brief Get the chain ID
# MAINNET Chain ID is:
'4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8' 

get_dynamic_global_properties   = Z + '"get_dynamic_global_properties",[]]}'
# @brief Retrieve the current @ref dynamic_global_property_object
'''(['accounts_registered_this_interval', 'next_maintenance_time',
'recent_slots_filled', 'witness_budget', 'dynamic_flags',
'last_irreversible_block_num', 'head_block_id', 'current_aslot',
'recently_missed_count', 'head_block_number', 'last_budget_time',
'id', 'time', 'current_witness'])'''


'''
//////////
// Keys //
//////////
'''

get_key_references = Z + '"get_key_references",[["%s",]]]}' % public_key
#
''

is_public_key_registered = Z + '"is_public_key_registered",["%s"]]}' % public_key
# Determine whether a textual representation of a public key
# (in Base-58 format) is #currently# linked
# to any #registered# (i.e. non-stealth) account on the blockchain
# @param public_key Public key
# @return Whether a public key is known
''

'''
//////////////
// Accounts //
//////////////
'''

get_accounts = Z + '"get_accounts",[["%s",]]]}' % account_id
# @brief Get a list of accounts by ID
# @param account_ids IDs of the accounts to retrieve
# @return The accounts corresponding to the provided IDs
# This function has semantics identical to @ref get_objects
'''(['membership_expiration_date', 'id', 'whitelisting_accounts',
'active_special_authority', 'lifetime_referrer', 'owner', 'statistics',
'options', 'blacklisted_accounts', 'referrer_rewards_percentage',
'top_n_control_flags', 'active', 'whitelisted_accounts',
'owner_special_authority', 'lifetime_referrer_fee_percentage',
'blacklisting_accounts', 'name', 'referrer', 'network_fee_percentage',
'registrar'])'''

get_full_accounts = Z + '"get_full_accounts",[["%s",],%s]]}' % (account_name, subscribe)
# @brief Fetch all objects relevant to the specified accounts and subscribe to updates
# @param callback Function to call with updates
# @param names_or_ids Each item must be the name or ID of an account to retrieve
# @return Map of string from @ref names_or_ids to the corresponding account
# This function fetches all relevant objects for the given accounts, and subscribes to updates to the given
# accounts. If any of the strings in @ref names_or_ids cannot be tied to an account, that input will be
# ignored. All other accounts will be retrieved and subscribed.
'''(['proposals', 'settle_orders', 'registrar_name', 'vesting_balances',
'balances', 'statistics', 'account', 'lifetime_referrer_name',
'referrer_name', 'withdraws', 'call_orders', 'assets', 'votes',
'limit_orders'])'''

get_account_by_name = Z + '"get_account_by_name",["%s"]]}' % account_name
#
'''['membership_expiration_date', 'id', 'whitelisting_accounts',
'active_special_authority', 'lifetime_referrer', 'owner', 'statistics',
'options', 'blacklisted_accounts', 'referrer_rewards_percentage',
'top_n_control_flags', 'active', 'whitelisted_accounts',
'owner_special_authority', 'lifetime_referrer_fee_percentage',
'blacklisting_accounts', 'name', 'referrer', 'network_fee_percentage',
'registrar'])'''

get_account_references = Z + '"get_account_references",["%s",]]}' % account_id
#  @return all accounts that referr to the key or account id in their owner or active authorities.
''

lookup_account_names = Z + '"lookup_account_names",[%s]]}' % account_names
# @brief Get a list of accounts by name
# @param account_names Names of the accounts to retrieve
# @return The accounts holding the provided names
# This function has semantics identical to @ref get_objects
'''(['membership_expiration_date', 'id', 'whitelisting_accounts',
'active_special_authority', 'lifetime_referrer', 'owner', 'statistics',
'options', 'blacklisted_accounts', 'referrer_rewards_percentage',
'top_n_control_flags', 'active', 'whitelisted_accounts', 'cashback_vb',
'owner_special_authority', 'lifetime_referrer_fee_percentage',
'blacklisting_accounts', 'name', 'referrer', 'network_fee_percentage',
'registrar'])
'''

lookup_accounts = Z + '"lookup_accounts",["%s", "%s"]]}' % (account_name, limit)
# @brief Get names and IDs for registered accounts
# @param lower_bound_name Lower bound of the first name to return
# @param limit Maximum number of results to return -- must not exceed 1000
'[["account", "account_id"],[...],]'


get_account_count = Z + '"get_account_count",[]]}'
# @brief Get the total number of accounts registered with the blockchain
'integer'


'''
//////////////
// Balances //
//////////////
'''
get_account_balances = Z + '"get_account_balances",["%s", [] ]]}' % (account_id)
# @brief Get an account's balances in various assets
# @param id ID of the account to get balances for
# @param assets IDs of the assets to get balances of; if empty, get all assets account has a balance in
# @return Balances of the account
"(['amount', 'asset_id'])"

get_named_account_balances = Z + '"get_named_account_balances",["%s", [] ]]}' % (account_name)
# Semantically equivalent to @ref get_account_balances, but takes a name instead of an ID.
"(['amount', 'asset_id'])"

get_balance_objects = Z + 'FIXME' # ( const vector<address>& addrs )
# @return all unclaimed balance objects for a set of addresses #/
''

get_vested_balances = Z + 'FIXME' # ( const vector<balance_id_type>& objs )
#
''

get_vesting_balances = Z + '"get_vesting_balances",["%s"]]}' % account_id
#
''

'''
////////////
// Assets //
////////////
'''

get_assets = Z + '"get_assets",[["%s",]]]}' % asset_id
# @brief Get a list of assets by ID
# @param asset_ids IDs of the assets to retrieve
# @return The assets corresponding to the provided IDs
# This function has semantics identical to @ref get_objects
list_assets = Z + '"list_assets",["%s","%s"]]}' % (asset, limit)
# @brief Get assets alphabetically by symbol name
# @param lower_bound_symbol Lower bound of symbol names to retrieve
# @param limit Maximum number of assets to fetch (must not exceed 100)
# @return The assets found
lookup_asset_symbols= Z + '"lookup_asset_symbols",[%s]]}' % coins
# @brief Get a list of assets by symbol
# @param asset_symbols Symbols or stringified IDs of the assets to retrieve
# @return The assets corresponding to the provided symbols or IDs
# This function has semantics identical to @ref get_objects

'''
/////////////////////
// Markets / feeds //
/////////////////////
'''

get_order_book = Z + '"get_order_book",["%s","%s","%s"]]}' % (currency, asset, limit)
# @brief Get limit orders in a given market
# @param a ID of asset being sold
# @param b ID of asset being purchased
# @param limit Maximum number of orders to retrieve
# @return The limit orders, ordered from least price to greatest
"(['bids', 'quote', 'base', 'asks'])"

get_limit_orders = Z + '"get_limit_orders",["%s","%s","%s"]]}' % (asset_id, asset_id2, limit)
# @brief Get limit orders in a given market
# @param a ID of asset being sold
# @param b ID of asset being purchased
# @param limit Maximum number of orders to retrieve
# @return The limit orders, ordered from least price to greatest
"(['expiration', 'for_sale', 'seller', 'sell_price', 'id', 'deferred_fee'])"

get_call_orders = Z + '"get_call_orders",["%s","%s"]]}' % (asset_id, limit)
# @brief Get call orders in a given asset
# @param a ID of asset being called
# @param limit Maximum number of orders to retrieve
# @return The call orders, ordered from earliest to be called to latest
# Returns list of dictionaries

get_settle_orders = Z + '"get_settle_orders",["%s","%s"]]}' % (asset_id, limit)
# @brief Get forced settlement orders in a given asset
# @param a ID of asset being settled
# @param limit Maximum number of orders to retrieve
# @return The settle orders, ordered from earliest settlement date to latest
# Returns list of dictionaries

get_margin_positions = Z + '"get_margin_positions",["%s"]]}' % account_id
# @return all open margin positions for a given account id.
# Returns list of dictionaries

get_collateral_bids = Z + 'FIXME' # (const asset_id_type asset, uint32_t limit, uint32_t start)
# @brief Get collateral_bid_objects for a given asset
# @param a ID of asset
# @param limit Maximum number of objects to retrieve
# @param start skip that many results
# @return The settle orders, ordered from earliest settlement date to latest

subscribe_to_market = Z + 'FIXME' # (std::function<void(const variant&)> callback, asset_id_type a, asset_id_type b)
# @brief Request notification when the active orders in the market between two assets changes
# @param callback Callback method which is called when the market changes
# @param a First asset ID
# @param b Second asset ID
# Callback will be passed a variant containing a vector<pair<operation, operation_result>>. The vector will
# contain, in order, the operations which changed the market, and their results.

unsubscribe_from_market = Z + 'FIXME' # unsubscribe_from_market( asset_id_type a, asset_id_type b )
# @brief Unsubscribe from updates to a given market
# @param a First asset ID
# @param b Second asset ID

get_ticker = Z + '"get_ticker",["%s","%s","%s"]]}' % (currency, asset, skip_order_book)
# @brief Returns the ticker for the market assetA:assetB
# @param a String name of the first asset
# @param b String name of the second asset
# @return The market ticker for the past 24 hours.
"(['base', 'lowest_ask', 'highest_bid', 'time', 'percent_change', 'latest', 'quote', 'quote_volume', 'base_volume'])"

get_24_volume = Z + '"get_24_volume",["%s","%s"]]}' % (currency, asset)
# @brief Returns the ticker for the market assetA:assetB
# @param a String name of the first asset
# @param b String name of the second asset
# @return The market ticker for the past 24 hours.
"(['base_volume', 'base', 'quote', 'time', 'quote_volume'])"

get_top_markets = Z + '"get_top_markets",["%s"]]}' % 100
# @brief Returns vector of 24 hour volume markets sorted by reverse base_volume
# Note: this API is experimental and subject to change in next releases
# @param limit Max number of results
# @return Desc Sorted volume vector
"(['base', 'quote_volume', 'quote', 'base_volume', 'time'])"

get_trade_history = Z + '"get_trade_history",["%s","%s","%s","%s","%s"]]}' % (currency, asset, now, then, 100)
# @brief Returns recent trades for the market assetA:assetB, ordered by time, most recent first. The range is [stop, start)
# Note: Currently, timezone offsets are not supported. The time must be UTC.
# @param a String name of the first asset
# @param b String name of the second asset
# @param stop Stop time as a UNIX timestamp, the earliest trade to retrieve
# @param limit Number of trasactions to retrieve, capped at 100
# @param start Start time as a UNIX timestamp, the latest trade to retrieve
# @return Recent transactions in the market
"(['date', 'side2_account_id', 'sequence', 'value', 'side1_account_id', 'amount', 'price'])"


get_trade_history_by_sequence = Z + '' # ( const string& base, const string& quote, int64_t start, fc::time_point_sec stop, unsigned limit = 100 )
# @brief Returns trades for the market assetA:assetB, ordered by time, most recent first. The range is [stop, start)
# Note: Currently, timezone offsets are not supported. The time must be UTC.
# @param a String name of the first asset
# @param b String name of the second asset
# @param stop Stop time as a UNIX timestamp, the earliest trade to retrieve
# @param limit Number of trasactions to retrieve, capped at 100
# @param start Start sequence as an Integer, the latest trade to retrieve
# @return Transactions in the market

'''
///////////////
// Witnesses //
///////////////
'''

get_witnesses = Z + 'FIXME' # (const vector<witness_id_type>& witness_ids)
# @brief Get a list of witnesses by ID
# @param witness_ids IDs of the witnesses to retrieve
# @return The witnesses corresponding to the provided IDs
# This function has semantics identical to @ref get_objects

get_witness_by_account = Z + '"get_witness_by_account",["%s"]]}' % witness_id
# @brief Get the witness owned by a given account
# @param account The ID of the account whose witness should be retrieved
# @return The witness object, or null if the account does not have a witness

lookup_witness_accounts = Z + '"lookup_witness_accounts",["%s","%s"]]}' % (witness_id, limit)
# @brief Get names and IDs for registered witnesses
# @param lower_bound_name Lower bound of the first name to return
# @param limit Maximum number of results to return -- must not exceed 1000
# @return Map of witness names to corresponding IDs
"[['account', 'account_id'],[...],]"

get_witness_count = Z + '"get_witness_count",[]]}'
# @brief Get the total number of witnesses registered with the blockchain
'integer'

'''
///////////////////////
// Committee members //
///////////////////////
'''

get_committee_members = Z + 'FIXME' # (const vector<committee_member_id_type>& committee_member_ids)
# @brief Get a list of committee_members by ID
# @param committee_member_ids IDs of the committee_members to retrieve
# @return The committee_members corresponding to the provided IDs
#
# This function has semantics identical to @ref get_objects
''

get_committee_member_by_account = Z + 'FIXME' # (account_id_type account)
# @brief Get the committee_member owned by a given account
# @param account The ID of the account whose committee_member should be retrieved
# @return The committee_member object, or null if the account does not have a committee_member
''

lookup_committee_member_accounts = Z + 'FIXME' # (const string& lower_bound_name, uint32_t limit)
# @brief Get names and IDs for registered committee_members
# @param lower_bound_name Lower bound of the first name to return
# @param limit Maximum number of results to return -- must not exceed 1000
# @return Map of committee_member names to corresponding IDs
''

get_committee_count = Z + '"get_committee_count",[]]}'
# @brief Get the total number of committee registered with the blockchain
'integer'

'''
///////////////////////
// Worker proposals  //
///////////////////////
'''

get_all_workers = Z + '"get_all_workers",[]]}'
# @brief Get all workers
# @return All the workers
'''(['work_begin_date', 'total_votes_for', 'worker', 'worker_account',
'name', 'url', 'work_end_date', 'id', 'vote_for', 'daily_pay',
'vote_against', 'total_votes_against'])'''

get_workers_by_account = Z + 'FIXME' # (account_id_type account)
# @brief Get the workers owned by a given account
# @param account The ID of the account whose worker should be retrieved
# @return The worker object, or null if the account does not have a worker
''

get_worker_count = Z + '"get_worker_count",[]]}'
# @brief Get the total number of workers registered with the blockchain
'integer'

'''
///////////
// Votes //
///////////
'''

lookup_vote_ids = Z + ''
# @brief Given a set of votes, return the objects they are voting for.
# This will be a mixture of committee_member_object, witness_objects, and worker_objects
# The results will be in the same order as the votes.  Null will be returned for
# any vote ids that are not found.
''

'''
////////////////////////////
// Authority / validation //
////////////////////////////
'''

get_transaction_hex = Z + '"get_transaction_hex",[%s]]}' % trx
# @brief Get a hexdump of the serialized binary form of a transaction
'dd202b1154fac330e35a0101420200000000000000b6da3596373c0400000000002b541d000000000079246bec5a00000000'

get_required_signatures = Z + 'FIXME'
# @brief This API will take a partially signed transaction and a set of public keys that the owner has the ability to sign for
# and return the minimal subset of public keys that should add signatures to the transaction.

get_potential_signatures = Z + '"get_potential_signatures",[%s]]}' % trx
# @brief This method will return the set of all public keys that could possibly sign for a given transaction.  This call can
# be used by wallets to filter their set of public keys to just the relevant subset prior to calling @ref get_required_signatures
# to get the minimum subset.
"['BTS7QfjZvG5FPaKAy1FBKwixcrVW17cygGEqsDzXWgRf5UbQGxMZN', 'BTS62p99FbzbE6XuxE3cvMLH9b85NZrxuD58eB5yWm2qUMGLDuPr3']"

get_potential_address_signatures = Z + '"get_potential_address_signatures",[%s]]}' % trx
#  @brief This method will return the set of all public keys that could possibly sign for a given transaction.  This call can
# be used by wallets to filter their set of public keys to just the relevant subset prior to calling @ref get_required_signatures
# to get the minimum subset.
''

verify_authority = Z + '"verify_authority",[%s]]}' % trx
# @return true of the @ref trx has all of the required signatures, otherwise throws an exception
''

verify_account_authority = Z + 'FIXME'
# @return true if the signers have enough authority to authorize an account
''

validate_transaction = Z + '"validate_transaction",[%s]]}' % trx
# @brief Validates a transaction against the current state without broadcasting it on the network.
''

get_required_fees = Z + 'FIXME'
# @brief For each operation calculate the required fee in the specified asset type.  If the asset type does
# not have a valid core_exchange_rate
''

'''
///////////////////////////
// Proposed transactions //
///////////////////////////
'''

get_proposed_transactions = Z + '"get_proposed_transactions",["%s"]]}' % account_id
# @return the set of proposed transactions relevant to the specified account id.

'''
//////////////////////
// Blinded balances //
//////////////////////
'''

get_blinded_balances = Z + 'FIXME'
# @return the set of blinded balance objects by commitment ID

'''
/////////////////
// Withdrawals //
/////////////////
'''

get_withdraw_permissions_by_giver = Z + 'FIXME'
# @brief Get non expired withdraw permission objects for a giver(ex:recurring customer)
# @param account Account to get objects from
# @param start Withdraw permission objects(1.12.X) before this ID will be skipped in results. Pagination purposes.
# @param limit Maximum number of objects to retrieve
# @return Withdraw permission objects for the account
get_withdraw_permissions_by_recipient = Z + 'FIXME'
# @brief Get non expired withdraw permission objects for a recipient(ex:service provider)
# @param account Account to get objects from
# @param start Withdraw permission objects(1.12.X) before this ID will be skipped in results. Pagination purposes.
# @param limit Maximum number of objects to retrieve
# @return Withdraw permission objects for the account

'''
///////////////////////////////////////////////////////////////////////
MAKE SEVERAL TESTS CALLS BY TYPE
///////////////////////////////////////////////////////////////////////
'''
all_calls = [get_objects,set_subscribe_callback,
    set_pending_transaction_callback,set_block_applied_callback,
    cancel_all_subscriptions,get_block_header,get_block_header_batch,
    get_block,get_transaction,get_recent_transaction_by_id,
    get_chain_properties,get_global_properties,get_config,get_chain_id,
    get_dynamic_global_properties,get_key_references,is_public_key_registered,
    get_accounts,get_full_accounts,get_account_by_name,get_account_references,
    lookup_account_names,lookup_accounts,get_account_count,get_account_balances,
    get_named_account_balances,get_balance_objects,get_vested_balances,
    get_vesting_balances,get_assets,list_assets,lookup_asset_symbols,
    get_order_book,get_limit_orders,get_call_orders,get_settle_orders,
    get_margin_positions,get_collateral_bids,subscribe_to_market,
    unsubscribe_from_market,get_ticker,get_24_volume,get_top_markets,
    get_trade_history,get_trade_history_by_sequence,get_witnesses,
    get_witness_by_account,lookup_witness_accounts,get_witness_count,
    get_committee_members,get_committee_member_by_account,
    lookup_committee_member_accounts,get_committee_count,get_all_workers,
    get_workers_by_account,get_worker_count,lookup_vote_ids,
    get_transaction_hex,get_required_signatures,get_potential_signatures,
    get_potential_address_signatures,verify_authority,
    verify_account_authority,validate_transaction,get_required_fees,
    get_proposed_transactions,get_blinded_balances,
    get_withdraw_permissions_by_giver,get_withdraw_permissions_by_recipient,]

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

worker_calls =     [get_all_workers,get_worker_count]

vote_calls = []

authority_calls =  [get_transaction_hex,
                    get_potential_signatures,
                    get_potential_address_signatures,
                    verify_authority,
                    validate_transaction]

proposed_calls = []
blinded_calls = []
withdrawal_calls = []

'''
///////////////////////////////////////////////////////////////////////
 BEGIN TEST SCRIPT
///////////////////////////////////////////////////////////////////////
'''
print('')
print('which method would you like to test?')
print('')

print(' 1 : wss')
print(' 2 : https')
print('')
CHOICE = 0
while CHOICE not in [1,2]:
    CHOICE = int(input('choice 1 or 2 ? '))
print('')
print('which set of calls would you like to test?')
print('')
print('0 : all_calls')
print('1 : object_calls')
print('2 : subscription_calls')
print('3 : block_calls')
print('4 : global_calls')
print('5 : key_calls')
print('6 : account_calls')
print('7 : asset_calls')
print('8 : balance_calls')
print('9 : market_calls')
print('10 : witness_calls')
print('11 : committe_calls')
print('12 : worker_calls')
print('13 : vote_calls')
print('14 : authority_calls')
print('15 : proposed_calls')
print('16 : blinded_calls')
print('17 : withdrawal_calls')
print('')
CALLS = ''
while CALLS not in range(18):
    CALLS = int(input('call 0 to 17 ? '))
print('')

call_types = [all_calls, object_calls, subscription_calls, block_calls,
    global_calls,key_calls,account_calls,asset_calls,balance_calls,market_calls,
    witness_calls,committe_calls,worker_calls,vote_calls,authority_calls,
    proposed_calls,blinded_calls,withdrawal_calls]

CALLS = call_types[CALLS]

print(CALLS)

for call in CALLS:

    call = call.replace("'",'"') # double quotes ONLY

    # print call parameters
    print('')
    print((call.split(',"params":')[1]).rstrip('}'))
    print('-----------------------------------------------------------')


    if CHOICE == 1: 

        print("connecting via wss using websocket-client module to", node)
        try:
            ws = websocket.create_connection(node)
            ws.send(call)
            ret = literal(ws.recv())
            ws.close()
        except Exception as e:
            print (e.args)
            pass


    if CHOICE == 2: # connect via https using requests module

        node = node.replace('wss://','https://')
        print("connecting via https using requests module to", node)
        try:
            ret = literal(requests.post(node, data=call).text)
        except Exception as e:
            print (e.args)
            pass

    # Print keys and full response
    try:
        keys = ret['result'].keys()
        print('#', keys)
    except:
        try:
            keys = ret['result'][0].keys()
            print('#', keys)
        except:
            try:
                keys = ret['result'][0][1].keys()
                print('#', keys)
            except:
                print('# Returns string')
    try:
        print (ret)
    except:
        print('failed')
