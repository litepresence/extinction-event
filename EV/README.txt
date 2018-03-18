5 NODE VERIFIED LAST PRICE

nodes.py and last.py should be run in seperate terminals

nodes.py creates file nodes.txt
last.py creates file last.txt and appends to file blacklist.txt

nodes.txt is the top 10 latency sorted nodes of about 50 known nodes; updated approx every 2 minutes

last.txt uses nodes.txt to get price from 5 nodes, then makes a list "prices"

then process that list of prices from 5 different nodes pseudocode:


if the spread of the prices is too wide:

    append to file blacklist.txt the list of prices and the list of nodes used to gather them


if all prices are same:
    
    last = latest price

elif latest price less than 2% different than mean(prices):
    
    last = latest price
  
else:
    try: last = mode(prices)
    except: last = median(prices)

return last


   
   
