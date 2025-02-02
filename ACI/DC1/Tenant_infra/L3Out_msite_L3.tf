#------------------------------------------------
# Create L3Out
#------------------------------------------------

/*
API Information:
 - Class: "l3extOut"
 - Distinguished Name: "/uni/tn-infra/out-msite_L3"
GUI Location:
 - Tenants > infra > Networking > L3Outs > msite_L3
*/
resource "aci_l3_outside" "Tenant_infra_L3Out_msite_L3" {
    depends_on                                          = [
        data.aci_l3_domain_profile.L3_Domain_l3out,
        aci_tenant.Tenant_infra,
        aci_vrf.Tenant_infra_VRF_overlay-1
    ]
    tenant_dn                                           = aci_tenant.Tenant_infra.id
    description                                         = "Multi-Site L3Out"
    name                                                = "msite_L3"
    enforce_rtctrl                                      = "export"
    target_dscp                                         = "unspecified"
    relation_l3ext_rs_ectx                              = aci_vrf.Tenant_infra_VRF_overlay-1.id
    relation_l3ext_rs_l3_dom_att                        = data.aci_l3_domain_profile.L3_Domain_l3out.id
}

#------------------------------------------------
# Enable BGP on the L3Out
#------------------------------------------------

/*
API Information:
 - Class: "bgpExtP"
 - Distinguished Name: "uni/tn-infra/out-msite_L3/bgpExtP"
GUI Location:
 - Tenants > infra > Networking > L3Outs > msite_L3 > Enable BGP (Checkbox)
*/
resource "aci_rest" "infra_l3out_msite_L3_bgpExtP" {
    depends_on  = [
        aci_tenant.Tenant_infra,
        aci_l3_outside.Tenant_infra_L3Out_msite_L3,
    ]
    path        = "/api/node/mo/uni/tn-infra/out-msite_L3/bgpExtP.json"
    class_name  = "bgpExtP"
    payload     = <<EOF
{
	"bgpExtP": {
		"attributes": {
			"dn": "uni/tn-infra/out-msite_L3/bgpExtP",
			"status": "created"
		},
		"children": []
	}
}
    EOF
}

#------------------------------------------------
# Assign a OSPF Routing Policy to the L3Out
#------------------------------------------------

/*
API Information:
 - Class: "ospfExtP"
 - Distinguished Name: "/uni/tn-infra/out-msite_L3/ospfExtP"
GUI Location:
 - Tenants > infra > Networking > L3Outs > msite_L3: OSPF
*/
resource "aci_l3out_ospf_external_policy" "Tenant_infra_L3Out_msite_L3_OSPF_Policy" {
    depends_on      = [
        aci_tenant.Tenant_infra,
        aci_l3_outside.Tenant_infra_L3Out_msite_L3
    ]
    l3_outside_dn   = aci_l3_outside.Tenant_infra_L3Out_msite_L3.id
    area_cost  = "1"
    area_ctrl = "redistribute,summary"
    area_id  = "0.0.0.0"
    area_type = "regular"
    # multipod_internal = "no"
}

