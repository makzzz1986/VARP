# ARP table with NIC vendors
Sometimes it is important to know about MAC vendors right here and now.
You always can use online OUI checkers but much quicker to do it on Linux directly.
 
* OUI base from 07.01.18
* three-stage searching for slow machines: last time catching, catching at least once and at last resort - search in full OUI list
* colorizing vendors (in future - in separated configuration file)
* nice borders for arps from one interface
* written for old Python 2.6.6 and Debian 2.6.32+
* requires only arp and awk on host, no sudo privilage or installation. Add alias to .bashrc to use it quick!

### No more boring grey ARP tables! Brand new toxic Vendor ARP!

###![arp - sucks!](https://www.dropbox.com/s/9uim8z4inzrsrje/arpna.png?dl=0) -> ![varp - rulez!](https://www.dropbox.com/s/b5n3aa64kkti550/varp.png?dl=0)
