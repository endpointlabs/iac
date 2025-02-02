#------------------------------------------------
# Create L3Out
#------------------------------------------------

/*
API Information:
 - Class: "l3extOut"
 - Distinguished Name: "/uni/tn-common/out-wakanda-dmz"
GUI Location:
 - Tenants > common > Networking > L3Outs > wakanda-dmz
*/
resource "aci_l3_outside" "Tenant_common_L3Out_wakanda-dmz" {
    depends_on                                          = [
        data.aci_l3_domain_profile.L3_Domain_l3out,
        aci_tenant.Tenant_common,
        aci_vrf.Tenant_common_VRF_dmz
    ]
    tenant_dn                                           = aci_tenant.Tenant_common.id
    description                                         = "Wakanda DMZ L3Out"
    name                                                = "wakanda-dmz"
    enforce_rtctrl                                      = ["export"]
    target_dscp                                         = "unspecified"
    relation_l3ext_rs_ectx                              = aci_vrf.Tenant_common_VRF_dmz.id
    relation_l3ext_rs_l3_dom_att                        = data.aci_l3_domain_profile.L3_Domain_l3out.id
}

#------------------------------------------------
# Enable BGP on the L3Out
#------------------------------------------------

/*
API Information:
 - Class: "bgpExtP"
 - Distinguished Name: "uni/tn-common/out-wakanda-dmz/bgpExtP"
GUI Location:
 - Tenants > common > Networking > L3Outs > wakanda-dmz > Enable BGP (Checkbox)
*/
resource "aci_l3out_bgp_external_policy" "common_l3out_wakanda-dmz_bgpExtP" {
    depends_on  = [
        aci_tenant.Tenant_common,
        aci_l3_outside.Tenant_common_L3Out_wakanda-dmz,
    ]
    l3_outside_dn   = aci_l3_outside.Tenant_common_L3Out_wakanda-dmz.id
}

