#______________________________________________
#
# Fibre Channel (vHBA) Network Policies
#______________________________________________

fibre_channel_network_policies = {
  "ESX_vfc0" = {
    description     = ""
    default_vlan_id = 1011
    vsan_id         = 11
    tags            = [
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
  "ESX_vfc1" = {
    description     = ""
    default_vlan_id = 1011
    vsan_id         = 11
    tags            = [
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
  "test-easyucs-conversion-sp_SCP_fc0" = {
    description     = ""
    default_vlan_id = 1011
    vsan_id         = 11
    tags            = [
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
  "test-easyucs-conversion-sp_SCP_fc1" = {
    description     = ""
    default_vlan_id = 1011
    vsan_id         = 11
    tags            = [
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
  "test-easyucs-conversion-sp_SCP_fc2" = {
    description     = ""
    default_vlan_id = 4048
    vsan_id         = 1
    tags            = [
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
  "test-easyucs-conversion-sp_SCP_fc3" = {
    description     = ""
    default_vlan_id = 4048
    vsan_id         = 1
    tags            = [
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
  "test-easyucs-static-wnnn_SCP_fc0" = {
    description     = ""
    default_vlan_id = 4048
    vsan_id         = 1
    tags            = [
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
  "test-easyucs-static-wnnn_SCP_fc1" = {
    description     = ""
    default_vlan_id = 4048
    vsan_id         = 1
    tags            = [
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