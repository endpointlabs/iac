#______________________________________________
#
# Ethernet (vNIC) Network (VLAN) Group Policies
#______________________________________________

ethernet_network_group_policies = {
  "ESX_vmdata1-gold" = {
    allowed_vlans = "100,101,102,103"
    description   = ""
    native_vlan   = 2
    tags          = [
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
  "ESX_vmdata2-gold" = {
    allowed_vlans = "100,101,102,103"
    description   = ""
    native_vlan   = 2
    tags          = [
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
  "ESX_vmdata3-bronze" = {
    allowed_vlans = "109,110"
    description   = ""
    native_vlan   = 2
    tags          = [
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
  "ESX_vmdata4-bronze" = {
    allowed_vlans = "109,110"
    description   = ""
    native_vlan   = 2
    tags          = [
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
  "ESX_Vmotion" = {
    allowed_vlans = "2"
    description   = ""
    native_vlan   = 2
    tags          = [
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
  "ADMIN" = {
    allowed_vlans = "100"
    description   = ""
    native_vlan   = 2
    tags          = [
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
  "test-easyucs-conversion_LCP_eth1" = {
    allowed_vlans = "99,1101,1102,32"
    description   = ""
    native_vlan   = 2
    tags          = [
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
  "test-easyucs-conversion_LCP_eth3" = {
    allowed_vlans = "100,99,1102,1101"
    description   = ""
    native_vlan   = 1101
    tags          = [
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
  "test-easyucs-conversion_LCP_eth4" = {
    allowed_vlans = "1101,1103,1104,1102"
    description   = ""
    native_vlan   = 1102
    tags          = [
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
  "test-easyucs-conversion_LCP_eth5" = {
    allowed_vlans = "1101,1102,1103"
    description   = ""
    native_vlan   = 1102
    tags          = [
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
  "test-easyucs-conversion_LCP_eth6" = {
    allowed_vlans = "1101"
    description   = ""
    native_vlan   = 1101
    tags          = [
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
  "test-easyucs-conversion-sp_LCP_eth0" = {
    allowed_vlans = "1101,1102"
    description   = ""
    native_vlan   = 1101
    tags          = [
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
  "test-easyucs-conversion-sp_LCP_eth2" = {
    allowed_vlans = "99,1101,1102,1107,1108"
    description   = ""
    native_vlan   = 1101
    tags          = [
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
  "test-easyucs-conversion-sp_LCP_eth3" = {
    allowed_vlans = "1101"
    description   = ""
    native_vlan   = 1101
    tags          = [
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