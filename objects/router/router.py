"""Test components specific to Commotion Routers"""
import objects.exceptions as exceptions
import bunch
import netifaces as ni
import re

# To do:
# 1. (This doesn't actually need to be a class)
# 2. separate get_net_info into component methods


#class CommotionNetworkComponent(object):
    #"""Create object-like dict for netinfo
        #Client needs interfaces, node_ip, and client_ip.
        #Node needs only node_ip"""
    #netinfo = None;

    #def __init__:
        #netinfo = create_net_info()

    #def create_net_info():
        #get_interfaces()
        #get_commotion_client_ip()
        #get_commotion_node_ip()

        #return netinfo

    #setattr(object, netinfo)

    #return object

def get_net_info():
    """Create object-like dict for netinfo"""
    netobject = bunch.Bunch()
    #commotion_client_ip = None
    #commotion_node_ip = None

    interfaces, commotion_client_ip = get_commotion_client_ip()

    print("Commotion Client IP is", commotion_client_ip)

    try:
        commotion_client_ip is not None
    except exceptions.CommotionIPError as args:
        print(args)
    else:
        commotion_node_ip = get_commotion_node_ip(commotion_client_ip)
    finally:
        netobject.update(interfaces)
        netobject.update({'commotion_client_ip': commotion_client_ip})
        netobject.update({'commotion_node_ip': commotion_node_ip})

    return netobject


def get_commotion_client_ip():
    """Check interfaces for a valid commotion client IP address"""
    # Will interface impact commotion tests
    commotion_interfaces = {}
    commotion_client_ip = None
    # Raw list of interfaces
    # Could be rewritten as for __, iface in enumerate(ni.interfaces())
    interfaces = ni.interfaces()
    for iface in interfaces:
        try:
            if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
                print(iface + " has a valid Commotion IP address: " \
                    + ni.ifaddresses(iface)[2][0]['addr'])
                commotion_client_ip = ni.ifaddresses(iface)[2][0]['addr']
            else:
                commotion_interfaces[iface] = False
                print(iface + " not valid")
        except KeyError:
            commotion_interfaces[iface] = True
            print(iface + " has been disconnected")
            continue

    try:
        commotion_client_ip
    except (exceptions.CommotionIPError, KeyError) as args:
        print(args)

    # This should only return one thing. Move interfaces somewhere else!
    return commotion_interfaces, commotion_client_ip


def get_commotion_node_ip(commotion_client_ip):
    """Use commotion_client_ip to generate guess commotion node IP"""
    commotion_node_ip = None
    print("Generating node ip from", commotion_client_ip)
    commotion_node_ip = re.sub(r"(\d+)$", '1', commotion_client_ip)
    print("node_ip function is returning", commotion_node_ip)
    return commotion_node_ip
