parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {


    state parse_start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet)
        transition select(hdr.ethernet.ethertype) {
            ETHERTYPE_IPV4: parse_ipv4;
            ETHERTYPE_IPV6: parse_ipv6;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4)
        transition select(hdr.ipv4.protocol) {
            PROTOCOL_TCP: parse_tcp;
            PROTOCOL_UDP: parse_udp;
            PROTOCOL_ICMP: parse_icmp;
            default: accept;
        }
    }

    state parse_ipv6 {
        packet.extract(hdr.ipv6)
        transition select(hdr.ipv6.nextHeader) {
            NEXTHEADER_ICMP: parse_icmp;
            NEXTHEADER_UDP: parse_udp;
            NEXTHEADER_TCP: parse_tcp;
            default: accept;
        }
    }

    state parse_tcp {
        packet.extract(hdr.tcp)
        transition accept;
    }

    state parse_icmp {
        packet.extract(hdr.icmp)
        transition accept;
    }

    state parse_udp {
        packet.extract(hdr.udp)
        transition accept;
    }

}

