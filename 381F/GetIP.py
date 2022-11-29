from ncclient import manager
import xml.dom.minidom as p
import xmltodict

m = manager.connect(
    host="192.168.56.105",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
    )

netconf_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet2</name>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                
                                                <netmask>255.255.255.0</netmask>
                                        </address>
                                </ipv4>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
    </interface>
  </interfaces>
</filter>
"""

def sendIP():
  netconf_reply = m.get(netconf_filter)
  intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
  intf_config = intf_details["interfaces"]["interface"]
  CSVIP = intf_config["ipv4"]["address"]["ip"]
  return CSVIP