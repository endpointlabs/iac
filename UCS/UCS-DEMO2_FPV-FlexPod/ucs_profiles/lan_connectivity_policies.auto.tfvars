#______________________________________________
#
# LAN Connectivity Policies
#______________________________________________

lan_connectivity_policies = {
  "iSCSI-Boot" = {
    description                 = ""
    enable_azure_stack_host_qos = false
    iqn_allocation_type         = "None"
    iqn_pool                    = [""]
    iqn_static_identifier       = ""
    organization                = "UCS-DEMO2_FPV-FlexPod"
    vnic_placement_mode         = "auto"
    target_platform             = "FI-Attached"
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
    vnics = [
      {
        cdn_source                      = "vnic",
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMWare",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "iSCSI-Boot_00-Infra-A",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-A"],
        name                            = "00-Infra-A",
        pci_order                       = 6,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        cdn_source                      = "vnic",
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMWare",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "iSCSI-Boot_01-Infra-B",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-B"],
        name                            = "01-Infra-B",
        pci_order                       = 5,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        cdn_source                      = "vnic",
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMWare",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "iSCSI-Boot_02-iSCSI-A",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-A"],
        name                            = "02-iSCSI-A",
        pci_order                       = 4,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        cdn_source                      = "vnic",
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMWare",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "iSCSI-Boot_03-iSCSI-B",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-B"],
        name                            = "03-iSCSI-B",
        pci_order                       = 3,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        cdn_source                      = "vnic",
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMware-HighTrf",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "iSCSI-Boot_04-APIC-vDS-A",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-A"],
        name                            = "04-APIC-vDS-A",
        pci_order                       = 2,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        cdn_source                      = "vnic",
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMware-HighTrf",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "iSCSI-Boot_05-APIC-vDS-B",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-B"],
        name                            = "05-APIC-vDS-B",
        pci_order                       = 1,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
    ]
  }
  "TUTU_LCP" = {
    description                 = ""
    enable_azure_stack_host_qos = false
    iqn_allocation_type         = "None"
    iqn_pool                    = [""]
    iqn_static_identifier       = ""
    organization                = "UCS-DEMO2_FPV-FlexPod"
    vnic_placement_mode         = "auto"
    target_platform             = "FI-Attached"
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
    vnics = [
      {
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMWare",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "TUTU_LCP_00-Infra-A",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-A"],
        name                            = "00-Infra-A",
        pci_order                       = 61,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMWare",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "TUTU_LCP_01-Infra-B",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-B"],
        name                            = "01-Infra-B",
        pci_order                       = 60,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMWare",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "TUTU_LCP_02-iSCSI-A",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-A"],
        name                            = "02-iSCSI-A",
        pci_order                       = 59,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMWare",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "TUTU_LCP_03-iSCSI-B",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-B"],
        name                            = "03-iSCSI-B",
        pci_order                       = 58,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMware-HighTrf",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "TUTU_LCP_04-APIC-vDS-A",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-A"],
        name                            = "04-APIC-vDS-A",
        pci_order                       = 57,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = false,
        ethernet_adapter_policy         = "VMware-HighTrf",
        ethernet_network_control_policy = "Enable-CDP-LLDP",
        ethernet_network_group_policy   = "TUTU_LCP_05-APIC-vDS-B",
        ethernet_qos_policy             = "default_mtu9000",
        mac_address_allocation_type     = "pool",
        mac_address_pool                = ["MAC-Pool-B"],
        name                            = "05-APIC-vDS-B",
        pci_order                       = 56,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-001",
        pci_order                       = 2,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-002",
        pci_order                       = 3,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-003",
        pci_order                       = 4,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-004",
        pci_order                       = 5,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-005",
        pci_order                       = 6,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-006",
        pci_order                       = 7,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-007",
        pci_order                       = 8,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-008",
        pci_order                       = 9,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-009",
        pci_order                       = 10,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-010",
        pci_order                       = 11,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-011",
        pci_order                       = 12,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-012",
        pci_order                       = 13,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-013",
        pci_order                       = 14,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-014",
        pci_order                       = 15,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-015",
        pci_order                       = 16,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-016",
        pci_order                       = 17,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-017",
        pci_order                       = 18,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-018",
        pci_order                       = 19,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-019",
        pci_order                       = 20,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-020",
        pci_order                       = 21,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-021",
        pci_order                       = 22,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-022",
        pci_order                       = 23,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-023",
        pci_order                       = 24,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-024",
        pci_order                       = 25,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-025",
        pci_order                       = 26,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-026",
        pci_order                       = 27,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-027",
        pci_order                       = 28,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-028",
        pci_order                       = 29,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-029",
        pci_order                       = 30,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-030",
        pci_order                       = 31,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-031",
        pci_order                       = 32,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-032",
        pci_order                       = 33,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-033",
        pci_order                       = 34,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-034",
        pci_order                       = 35,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-035",
        pci_order                       = 36,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-036",
        pci_order                       = 37,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-037",
        pci_order                       = 38,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-038",
        pci_order                       = 39,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-039",
        pci_order                       = 40,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-040",
        pci_order                       = 41,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-041",
        pci_order                       = 42,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-042",
        pci_order                       = 43,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-043",
        pci_order                       = 44,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-044",
        pci_order                       = 45,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-045",
        pci_order                       = 46,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-046",
        pci_order                       = 47,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-047",
        pci_order                       = 48,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-048",
        pci_order                       = 49,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-049",
        pci_order                       = 50,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-050",
        pci_order                       = 51,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-051",
        pci_order                       = 52,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-052",
        pci_order                       = 53,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-053",
        pci_order                       = 54,
        slot_id                         = "MLOM",
        switch_id                       = "A",
      },
      {
        enable_failover                 = true,
        ethernet_adapter_policy         = "default",
        ethernet_network_control_policy = "default",
        ethernet_qos_policy             = "default",
        mac_address_allocation_type     = "static",
        mac_address_static              = "12:34:56:78:90:AB",
        name                            = "dynamic-prot-054",
        pci_order                       = 55,
        slot_id                         = "MLOM",
        switch_id                       = "B",
      },
    ]
  }
}