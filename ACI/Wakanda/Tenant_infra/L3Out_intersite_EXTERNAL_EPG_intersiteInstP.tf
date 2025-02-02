/*
API Information:
 - Class: "l3extInstP"
 - Distinguised Name: "/uni/tn-infra/out-intersite/instP-intersiteInstP"
GUI Location:
 - Tenants > infra > Networking > L3Outs > intersite > External EPGs > intersiteInstP
*/
resource "aci_external_network_instance_profile" "Tenant_infra_L3Out_intersite_External_EPG_intersiteInstP" {
    depends_on                                  = [
        aci_tenant.Tenant_infra,
        aci_l3_outside.Tenant_infra_L3Out_intersite
    ]
    l3_outside_dn                               = aci_l3_outside.Tenant_infra_L3Out_intersite.id
    description                                 = "Multi-Site"
    flood_on_encap                              = "disabled"
    match_t                                     = "AtleastOne"
    name                                        = "intersiteInstP"
    pref_gr_memb                                = "exclude"
    prio                                        = "unspecified"
    target_dscp                                 = "unspecified"
}

#------------------------------------------------
# Assign a Subnet to an External EPG
#------------------------------------------------

/*
API Information:
 - Class: "l3extSubnet"
 - Distinguised Name: "/uni/tn-infra/out-intersite/instP-intersiteInstP/extsubnet-[0.0.0.0/1]"
GUI Location:
 - Tenants > infra > Networking > L3Outs > intersite > External EPGs > intersiteInstP
*/
resource "aci_l3_ext_subnet" "Tenant_infra_L3Out_intersite_External_EPG_intersiteInstP_Subnet_0-0-0-0_1" {
    depends_on                              = [
        aci_tenant.Tenant_infra,
        aci_l3_outside.Tenant_infra_L3Out_intersite,
        aci_external_network_instance_profile.Tenant_infra_L3Out_intersite_External_EPG_intersiteInstP
    ]
    external_network_instance_profile_dn    = aci_external_network_instance_profile.Tenant_infra_L3Out_intersite_External_EPG_intersiteInstP.id
    description                             = "Multi-Site"
    ip                                      = "0.0.0.0/1"
    scope                                   = ["import-security"]
}

#------------------------------------------------
# Assign a Subnet to an External EPG
#------------------------------------------------

/*
API Information:
 - Class: "l3extSubnet"
 - Distinguised Name: "/uni/tn-infra/out-intersite/instP-intersiteInstP/extsubnet-[128.0.0.0/1]"
GUI Location:
 - Tenants > infra > Networking > L3Outs > intersite > External EPGs > intersiteInstP
*/
resource "aci_l3_ext_subnet" "Tenant_infra_L3Out_intersite_External_EPG_intersiteInstP_Subnet_128-0-0-0_1" {
    depends_on                              = [
        aci_tenant.Tenant_infra,
        aci_l3_outside.Tenant_infra_L3Out_intersite,
        aci_external_network_instance_profile.Tenant_infra_L3Out_intersite_External_EPG_intersiteInstP
    ]
    external_network_instance_profile_dn    = aci_external_network_instance_profile.Tenant_infra_L3Out_intersite_External_EPG_intersiteInstP.id
    description                             = "Multi-Site"
    ip                                      = "128.0.0.0/1"
    scope                                   = ["import-security"]
}

