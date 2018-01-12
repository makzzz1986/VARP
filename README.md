# ARP table with NIC vendors
Sometimes it is important to know about MAC vendors right here and now.
You always can use online OUI checkers but much quicker to do it on Linux directly.
 
* OUI base from 07.01.18
* three-stage searching for slow machines: last time catching, catching at least once and at last resort - search in full OUI list
* colorizing vendors (in future - in separated configuration file)
* nice borders for arps from one interface
* written for old Python 2.6.6 and Debian 2.6.32+
* requires only arp and awk on host, no sudo privilage, installation or dependencies. Add alias to .bashrc to use it quick!

### No more boring grey ARP tables! 

![arp - sucks!](https://img-fotki.yandex.ru/get/373867/51752532.d/0_ff071_574ceee1_orig.png) 

### Brand new toxic Vendor ARP!

![varp - rulez!](https://img-fotki.yandex.ru/get/480528/51752532.d/0_ff072_3b4f650_orig.png)
