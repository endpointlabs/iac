/*
API Information:
 - Class: "l3extInstP"
 - Distinguised Name: "/uni/tn-common/out-wakanda-prod/instP-prod"
GUI Location:
 - Tenants > common > Networking > L3Outs > wakanda-prod > External EPGs > prod
*/
resource "aci_external_network_instance_profile" "Tenant_common_L3Out_wakanda-prod_External_EPG_prod" {
    depends_on                                  = [
        aci_tenant.Tenant_common,
        aci_l3_outside.Tenant_common_L3Out_wakanda-prod
    ]
    l3_outside_dn                               = aci_l3_outside.Tenant_common_L3Out_wakanda-prod.id
    description                                 = "Wakanda Prod"
    flood_on_encap                              = "disabled"
    match_t                                     = "AtleastOne"
    name                                        = "prod"
    pref_gr_memb                                = "include"
    prio                                        = "unspecified"
    target_dscp                                 = "unspecified"
}

#------------------------------------------------
# Assign a Subnet to an External EPG
#------------------------------------------------

/*
API Information:
 - Class: "l3extSubnet"
 - Distinguised Name: "/uni/tn-common/out-wakanda-prod/instP-prod/extsubnet-[0.0.0.0/1]"
GUI Location:
 - Tenants > common > Networking > L3Outs > wakanda-prod > External EPGs > prod
*/
resource "aci_l3_ext_subnet" "Tenant_common_L3Out_wakanda-prod_External_EPG_prod_Subnet_0-0-0-0_1" {
    depends_on                              = [
        aci_tenant.Tenant_common,
        aci_l3_outside.Tenant_common_L3Out_wakanda-prod,
        aci_external_network_instance_profile.Tenant_common_L3Out_wakanda-prod_External_EPG_prod
    ]
    external_network_instance_profile_dn    = aci_external_network_instance_profile.Tenant_common_L3Out_wakanda-prod_External_EPG_prod.id
    description                             = "Wakanda Prod"
    ip                                      = "0.0.0.0/1"
    scope                                   = ["import-security"]
}

#------------------------------------------------
# Assign a Subnet to an External EPG
#------------------------------------------------

/*
API Information:
 - Class: "l3extSubnet"
 - Distinguised Name: "/uni/tn-common/out-wakanda-prod/instP-prod/extsubnet-[128.0.0.0/1]"
GUI Location:
 - Tenants > common > Networking > L3Outs > wakanda-prod > External EPGs > prod
*/
resource "aci_l3_ext_subnet" "Tenant_common_L3Out_wakanda-prod_External_EPG_prod_Subnet_128-0-0-0_1" {
    depends_on                              = [
        aci_tenant.Tenant_common,
        aci_l3_outside.Tenant_common_L3Out_wakanda-prod,
        aci_external_network_instance_profile.Tenant_common_L3Out_wakanda-prod_External_EPG_prod
    ]
    external_network_instance_profile_dn    = aci_external_network_instance_profile.Tenant_common_L3Out_wakanda-prod_External_EPG_prod.id
    description                             = "Wakanda Prod"
    ip                                      = "128.0.0.0/1"
    scope                                   = ["import-security"]
}

