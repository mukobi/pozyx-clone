from pythonosc.osc_message_builder import  OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
from definitions import definitions

class ReplayOscMessageSending:
    @staticmethod
    def send_message(data_type, header_list, data_list, osc_udp_client):
        if data_type == definitions.DATA_TYPE_POSITIONING:
            ReplayOscMessageSending.send_single_position(header_list, data_list, osc_udp_client)

    @staticmethod
    def send_single_position(header_list, data_list, osc_udp_client):
        network_id = 0x6000
        if network_id is None:
            network_id = 0
        i_posx = header_list.index("Position-X")
        i_posy = header_list.index("Position-Y")
        i_posz = header_list.index("Position-Z")
        posx = data_list[i_posx]
        posy = data_list[i_posy]
        posz = data_list[i_posz]
        if osc_udp_client is not None:
            osc_udp_client.send_message(
                "/position", [network_id, int(posx), int(posy), int(posz)])
