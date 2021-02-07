
import scapy.all as scapy
import optparse

parse = optparse.OptionParser()

def get_input():

    parse.add_option("-i","--ip", dest="ip",help="login ip range")

    parse.add_option("-m", "--mac",dest="mac_address",help="login mac address")

    (user_inputs,arguments) = parse.parse_args()

    if not user_inputs.ip and user_inputs.mac_address:
        print("Error please enter ip and mac address")

    return user_inputs



def send_packet(user_ip, user_mac):

    arp_request_packet = scapy.ARP(pdst=user_ip)

    broadcast_packet = scapy.Ether(dst=user_mac)

    combined_packet = broadcast_packet / arp_request_packet

    (answered_list, unanswered_list) = scapy.srp(combined_packet, timeout=1)

    return answered_list.summary()

print("net scanner start!!!")
user_inputs = get_input()
print(send_packet(user_inputs.ip, user_inputs.mac_address))
