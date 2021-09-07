#______________________________________________
#
# IP Pool Variables
#______________________________________________

ip_pools = {
  "iSCSI-IP-Pool-A" = {
    ipv4_block       = [
      {
        from = "192.168.10.101",
        to = "192.168.10.116",
      },
    ]
    ipv4_config      = {
      config = {
        netmask = "255.255.255.0",
      }
    }
    ipv6_block       = [
      {
        from = "44::",
        size = "9",
      },
    ]
    ipv6_config      = {
      config = {
        gateway = "44::12",
        prefix = "64",
        primary_dns = "::",
        secondary_dns = "::",
      }
    }
    organization     = "UCS-DEMO2_FPV-FlexPod"
    tags = [
      {
        key = "easyucs_origin",
        value = "convert",
      },
      {
        key = "easyucs_version",
        value = "0.9.8",
      },
    ]
  }
  "iSCSI-IP-Pool-B" = {
    ipv4_block       = [
      {
        from = "192.168.20.101",
        to = "192.168.20.116",
      },
    ]
    ipv4_config      = {
      config = {
        netmask = "255.255.255.0",
      }
    }
    ipv6_block       = [
      {
        from = "44::",
        size = "9",
      },
    ]
    ipv6_config      = {
      config = {
        gateway = "44::12",
        prefix = "64",
        primary_dns = "::",
        secondary_dns = "::",
      }
    }
    organization     = "UCS-DEMO2_FPV-FlexPod"
    tags = [
      {
        key = "easyucs_origin",
        value = "convert",
      },
      {
        key = "easyucs_version",
        value = "0.9.8",
      },
    ]
  }
}