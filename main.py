# encoding=utf8
# For Python 2.6.6+ and Debian 2.6.32+

import subprocess
import sys

# main class for arps
class varp():
    host = ''
    mac = ''
    eth = ''
    vendor = ''
    color = '\033[0m'                                       # now it is default but may be changed
    color_EOL = '\033[0m'                                   # default color of end of line

    def __init__(self, host, mac, eth):                     # set attributes of arp - host, mac, interface and vendor!
        self.host = host[1:-1]                              # set host
        self.mac = mac                                      # set MAC
        self.eth = eth                                      # set name of interface
        if not mac.startswith('--'):                        # if arp is not incompleted 
            check_last = check_db(mac[:8], oui_last)        # check in list of last found ouis 
            if check_last:                                  # if we find - so we've got vendor
                self.vendor = check_last
            else:                                           # if not - let's check in once found list
                check_once = check_db(mac[:8], oui_once)
                if check_once:
                    self.vendor = check_once
                else:
                    check_all = check_db(mac[:8], oui_all)  # and the last chance - check in all ouis list
                    if check_all:
                        self.vendor = check_all
                                                            # now we can paint different vendors by color
                                                            # you can change it and add new
            if self.vendor == '' or self.vendor == 'Unknown':
                self.vendor = 'Unknown'                     # if we haven't found vendor, so make it Unknown and we will
                global vmacs_last                           # never try to find it in all oui list
                self.color = paint.BOLD
                vmacs_last.append([mac[:8], self.vendor])
            elif self.vendor.startswith('Cisco'):
                self.color = paint.WARNING
            elif self.vendor.startswith('DOMS') or self.vendor.startswith('Current En'):
                self.color = paint.GREEN                     
            elif self.vendor.startswith('Wincor'):
                self.color = paint.MAGENTA                  # Wincor would be magenta
        else:                                               # if arp is incompleted, change color to red
            self.vendor = ''
            self.color = paint.FAIL


    # for some reason maybe we want to change it from outside 
    def vend(self, vend):
        self.vendor = vend

    # just for debugging usage
    def __str__(self):
        if self.vendor == '':
            return self.color + self.host + ' ' + self.mac + ' ' + self.eth + self.color_EOL
        else:
            return self.color + self.host + ' ' + self.mac + ' ' + self.vendor + ' ' + self.eth + self.color_EOL

    # just for debugging usage
    def __repr__(self):
        if self.vendor == '':
            return self.host + ' ' + self.mac + ' ' + self.eth
        else:
            return self.host + ' ' + self.mac + ' ' + self.vendor + ' ' + self.eth
 
# from stackoverflow python color theme, thank folks!
class paint:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    EOL = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# checking MAC in file
def check_db(mac, file):
    global vmacs_last
    file.seek(0)
    for line in file.readlines():
        if line.startswith(mac[:8]):            
            vmacs_last.append(vmac_split(line))
            return vmac_split(line)[1]

# split '00:00:00    VENDOR OF NIC' to ['00:00:00', 'VENDOR OF NIC'] and shortened vendor to 20 characters
def vmac_split(s):
    return [s[:8], s[8:].strip()[:20]]

# adding spaces after a string to create columns 
def spacer(s, width=23):
    return s+(' '*(width-len(s)))

# representing table with columns by adding right amount of spaces
def liner(v):
    return ' ' + v.color + spacer(v.host, 17) + spacer(v.mac, 19) + spacer(v.vendor) + v.color_EOL

# here we will find out incompleted arps and create new object for every line in arp table, 
# sort them by interface and return to printing
def list_clear(l):
    temp_list = []
    global mac_in_int
    for line in l:
        if len(line.strip()) > 0:
            h, m, i = line.split()
            if i in mac_in_int:                         # count arps by interface we will use it to print nice borders
                mac_in_int[i] += 1
            else:
                mac_in_int[i] = 1
            if m.startswith('<inc'):                    # ARP is incompleted
                m = '-- Incomplete  --'
            temp_list.append(varp(h, m, i))             # new object of class varp
    temp_list.sort(key=lambda v: (v.eth, v.host))       # sort lines by interfaces and IPs
    return temp_list

# get middle of column
def middle(x):
    return x//2+1

# print out arp table
def print_varp(arp):                                    # different borders:
    tl = u'\u250c'.encode('utf-8')                      # top left corner
    tr = u'\u2510'.encode('utf-8')                      # top right
    br = u'\u2518'.encode('utf-8')                      # bottom right
    bl = u'\u2514'.encode('utf-8')                      # bottom left
    hli = u'\u2500'.encode('utf-8')                     # horizontal line
    vli = u'\u2502'.encode('utf-8')                     # vertical one
    title = u'\u251c'.encode('utf-8')                   # vertical lines to right
    toptitle = u'\u252c'.encode('utf-8')                # horizontal to bottom
    int_counter = {'int': '', 'alone': False, 'middle': 1, 'top': 1} # helps us to print borders in right way
    print tl, 'IP address   ', tr+tl, 'MAC-address    ', tr+tl, 'NIC vendor         ', tr+tl, '  Int  ', tr   # top line with table's title 
    for line in arp:                                    # loop by arps
        if int_counter['int'] != line.eth:              # if it's arp from new interface 
            print ''                                    # miss one line to separate interfaces
            int_counter['int'] = line.eth               # change interface
            if mac_in_int[line.eth] == 1:               # if this interface has only one arp - tag it
                int_counter['alone'] = True
            else:
                int_counter['alone'] = False            # if it has more than one - get middle and top line
                int_counter['middle'] = middle(mac_in_int[line.eth])
                int_counter['top'] = mac_in_int[line.eth]

        if int_counter['alone'] is True:                            # if we have only one arp in interface 
            print liner(line) + hli + ' ' + line.eth
        else:
            if int_counter['top'] == mac_in_int[line.eth] == 2:     # we have two arps in interface
                print liner(line) + toptitle + ' ' + line.eth
            elif mac_in_int[line.eth] == int_counter['top']:        # and more than two arps, it will be top line
                print liner(line) + tr
            elif mac_in_int[line.eth] == int_counter['middle']:     # middle line with name of interface
                print liner(line) + title + ' ' + line.eth
            elif mac_in_int[line.eth] == 1:                         # bottom line
                print liner(line) + br
            else:
                print liner(line) + vli                             # all others lines - with top border between top/middle and middle/bottom
        mac_in_int[line.eth] -= 1

# We going to ask OS "arp -na | awk '...', dismember, try to find vendor and print it
def call_arp():
    arp = subprocess.Popen(['arp', '-an'], stdout=subprocess.PIPE)
    awk = subprocess.Popen(['awk', '$4~/<incomplete>/ {print $2, $4, $6}; $5~/[ether]/ {print $2, $4, $7}'], stdin=arp.stdout, stdout=subprocess.PIPE)
    arp_result =  awk.communicate()[0]
    arp_clear = arp_result.split('\n')              # spliting it by words
    print_varp(list_clear(arp_clear))               # processing and print it out

 
# Main body of script
current_folder = sys.path[0]                        # folder of script
oui_all_link = current_folder+'/oui_all.txt'        # all OUI vendors list
oui_once_link = current_folder+'/oui_once.txt'      # OUI list wich we was found at least once
oui_last_link = current_folder+'/oui_last.txt'      # last found ouis - it is usefull for statically connected devices
vmacs_last = []                                     # here was a list of OUI wich we find this time to write in oui_last.txt
mac_in_int = {}                                     # arps by interfaces counter

# open a list of last found ouis, if it absent - create new and open
try:
    oui_last = open(oui_last_link, 'r+')
except IOError:
    oui_last = open(oui_last_link, 'a').close()
    oui_last = open(oui_last_link, 'r+')

# the same for once found OUI list
try:
    oui_once = open(oui_once_link, 'r')
except IOError:
    oui_once = open(oui_once_link, 'a').close()
    oui_once = open(oui_once_link, 'r+')

# try to open all oui list, if we don't have one, use once list instead, for example, if you need your own oui list
try:
    oui_all = open(oui_all_link, 'r')
except IOError:
    oui_all = oui_once

# Go on!
call_arp()


# Section of updating oui_last and oui_once
# Now I think it was useless idea of three-stage finding 

# rewrite last found ouis file to our new oui vendor list!
oui_last.seek(0)
for elem in vmacs_last:
    if elem[1] != 'Unknown':
        oui_last.write('{0}    {1}\n'.format(elem[0], elem[1]))
oui_last.truncate()
oui_last.close()

# check once found list and if we find a new one in last finded - add it to new list
oui_once_to_add = []
for oui_now in vmacs_last:
    if oui_now[1] != 'Unknown':
        oui_once.seek(0)
        check = False
        for elem in oui_once.readlines():
            if elem.startswith(oui_now[0]):
                check = True
                break
        if check is False:
            oui_once_to_add.append(oui_now)

# closing oui_once
oui_once.close()
# and if we find a new one oui in full list - open oui_once and add em
if len(oui_once_to_add) > 0:
    oui_once = open(oui_once_link, 'a')
    for elem in oui_once_to_add:
        oui_once.write('{0}    {1}\n'.format(elem[0], elem[1]))
    oui_once.close()

oui_all.close()
