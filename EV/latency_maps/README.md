This folder is used to store historical latency maps as produced by latencyTEST.py

Your most recent latency test always overwrites:

    map.png

Your historical maps will be in map + unix timestamp format like this:

    map_1556209155

To store your map history, set `USER CONTROLS` toggle to:

    HISTORY = True
    
    
**SAMPLE LATENCY MAP**

<p align="center"> 
<img src="https://raw.githubusercontent.com/litepresence/extinction-event/master/EV/latency_maps/map.png">
</p>

**LEGEND**

    small red dot is a seed node
    yellow dot is a public rpc node
    larger magenta circle means faster response time 
