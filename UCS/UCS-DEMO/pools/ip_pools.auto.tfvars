#______________________________________________
#
# IP Pools Policies
#______________________________________________

ip_pools = {
  "ext-mgmt" = {
    ipv4_block         = [
      {
        from = "10.60.0.111",
        to   = "10.60.0.130"
      },
    ]
    ipv4_config        = [
      {
        gateway       = "",
        netmask       = ""
        primary_dns   = ""
        secondary_dns = ""
      },
      {
        gateway       = "",
        netmask       = ""
        primary_dns   = ""
        secondary_dns = ""
      },
      {
        gateway       = "",
        netmask       = ""
        primary_dns   = ""
        secondary_dns = ""
      },
    ]
    ipv6_block         = []
    ipv4_config        = []
    organization      = "UCS-DEMO"
    tags              = [
      {
        key   = "easyucs_origin",
        value = "convert"
      },
      {
        key   = "easyucs_version",
        value = "0.9.8"
      },
    ]
  }
  "iscsi-initiator-pool" = {
    ipv4_block         = [
      {
        from = "10.60.0.111",
        to   = "10.60.0.130"
      },
    ]
    ipv4_config        = [
      {
        gateway       = "",
        netmask       = ""
        primary_dns   = ""
        secondary_dns = ""
      },
      {
        gateway       = "",
        netmask       = ""
        primary_dns   = ""
        secondary_dns = ""
      },
      {
        gateway       = "",
        netmask       = ""
        primary_dns   = ""
        secondary_dns = ""
      },
    ]
    ipv6_block         = []
    ipv4_config        = []
    organization      = "UCS-DEMO"
    tags              = [
      {
        key   = "easyucs_origin",
        value = "convert"
      },
      {
        key   = "easyucs_version",
        value = "0.9.8"
      },
    ]
  }
}