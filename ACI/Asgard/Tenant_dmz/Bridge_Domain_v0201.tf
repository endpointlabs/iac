/*
API Information:
 - Class: "fvBD"
 - Distinguised Name: "/uni/tn-dmz/BD-v0201"
GUI Location:
 - Tenants > dmz > Networking > Bridge Domains > v0201
*/
resource "aci_bridge_domain" "Tenant_dmz_Bridge_Domain_v0201" {
    depends_on                                  = [
        aci_tenant.Tenant_dmz,
        data.aci_tenant.Tenant_common,
        data.aci_vrf.Tenant_common_VRF_dmz,
        data.aci_l3_outside.Tenant_common_L3Out_asgard-dmz,
    ]
    tenant_dn                                   = aci_tenant.Tenant_dmz.id
    description                                 = "Stretched Vlan201"
    name                                        = "v0201"
    arp_flood                                   = "no"
    bridge_domain_type                          = "regular"
    ep_clear                                    = "no"
    host_based_routing                          = "no"
    intersite_bum_traffic_allow                 = "yes"
    intersite_l2_stretch                        = "yes"
    ip_learning                                 = "yes"
    ipv6_mcast_allow                            = "no"
    limit_ip_learn_to_subnets                   = "yes"
    mcast_allow                                 = "no"
    multi_dst_pkt_act                           = "bd-flood"
    optimize_wan_bandwidth                      = "yes"
    unicast_route                               = "yes"
    unk_mac_ucast_act                           = "proxy"
    unk_mcast_act                               = "flood"
    relation_fv_rs_ctx                          = data.aci_vrf.Tenant_common_VRF_dmz.id
    relation_fv_rs_abd_pol_mon_pol              = "uni/tn-common/monepg-default"
    relation_fv_rs_bd_to_out                    = [data.aci_l3_outside.Tenant_common_L3Out_asgard-dmz.id]
    relation_fv_rs_bd_to_ep_ret                 = "uni/tn-common/epRPol-default"
    relation_fv_rs_mldsn                        = "uni/tn-common/mldsnoopPol-default"
    relation_fv_rs_bd_to_nd_p                   = "uni/tn-common/ndifpol-default"
    relation_fv_rs_bd_to_fhs                    = "uni/tn-common/bdpol-default"
    relation_fv_rs_igmpsn                       = "uni/tn-common/snPol-default"
}

/*
API Information:
 - Class: "fvSubnet"
 - Distinguished Name: "/uni/tn-dmz/BD-v0201/subnet-[10.89.1.1/24]"
GUI Location:
 - Tenants > dmz > Networking > Bridge Domains > v0201 > Subnets
*/
resource "aci_subnet" "Tenant_dmz_Bridge_Domain_v0201_Subnet_10-89-1-0_24" {
    depends_on                          = [
        aci_tenant.Tenant_dmz,
        aci_bridge_domain.Tenant_dmz_Bridge_Domain_v0201
    ]
    parent_dn                           = aci_bridge_domain.Tenant_dmz_Bridge_Domain_v0201.id
    ctrl                                = ["nd"]
    description                         = "Stretched Vlan201"
    ip                                  = "10.89.1.1/24"
    preferred                           = "no"
    scope                               = ["public"]
    virtual                             = "no"
}

