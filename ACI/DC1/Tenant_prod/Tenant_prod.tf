/*
API Information:
 - Class: "fvTenant"
 - Distinguished Name: "uni/tn-prod"
GUI Location:
 - Tenants > Create Tenant > prod
*/
resource "aci_tenant" "Tenant_prod" {
    description                     = "Updated Tenant Description"
    name                            = "prod"
    relation_fv_rs_tenant_mon_pol   = ""
}

