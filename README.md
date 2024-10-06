Hello!

With this code you can download all the IP addresses of the country of your choice to ban unwanted partners in the torrent client.
The file you get when you run it is formatted as .dat. The output file looks quite strange, but this is the only one that works with qBittorent.

In my case, it works with 100% efficiency. The process of downloading addresses takes from 10 seconds to 5 minutes, depending of the population of the country.

Method of operation:
1. download the repo
2. select the country from txt file to ban and copy (two-letter ID)
3. paste it into a python file up to 62 line (there is instruction, you'll see) 
4. run with CMD -> python Change_here_country_code.py
5. find the file with the addresses
6. run the torrent client and find the options 'IP filtering' or something like that
7. load it and refresh. The torrent client should give you a feedback about the number of banned addresses

------------
I recommend qBittorent Enhanced Edition (banned Chinese weird leech clients by default) or regular qBittorent.
I don't know what other clients have this option and if the .dat file format will be correct. 
