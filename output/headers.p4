header ethernet_t{
    bit<48>  dstAddr;
    bit<48>  srcAddr;
    bit<16>  etherType;
}

header ipv6_t{
    bit<4>    version;
    bit<8>    trafficClass;
    bit<20>   flowLabel;
    bit<16>   len;
    bit<8>    nextHeader;
    bit<8>    hopLimit;
    bit<128>  srcAddr;
    bit<128>  dstAddr;
}

header ipv4_t{
    bit<4>   version;
    bit<4>   ihl;
    bit<6>   dscp;
    bit<2>   ecn;
    bit<16>  totalLength;
    bit<16>  identification;
    bit<3>   flags;
    bit<13>  fragOffset;
    bit<8>   ttl;
    bit<8>   protocol;
    bit<16>  hdrChecksum;
    bit<32>  srcAddr;
    bit<32>  dstAddr;
}

header icmp_t{
    bit<8>   tp;
    bit<8>   code;
    bit<16>  checksum;
    bit<16>  id;
    bit<16>  seqNo;
}

header tcp_t{
    bit<16>  srcPort;
    bit<16>  dstPort;
    bit<32>  seqNo;
    bit<32>  ackNo;
    bit<4>   dataOffset;
    bit<3>   res;
    bit<3>   ecn;
    bit<6>   crtl;
    bit<16>  window;
    bit<16>  checksum;
    bit<16>  urgentPtr;
}

header udp_t{
    bit<16>  srcPort;
    bit<16>  dstPort;
    bit<16>  len;
    bit<16>  checksum;
}

struct headers {
    ethernet_t  ethernet;
    ipv6_t      ipv6;
    ipv4_t      ipv4;
    icmp_t      icmp;
    tcp_t       tcp;
    udp_t       udp;
}
