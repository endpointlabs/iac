/*
API Information:
 - Class: "fvAEPg"
 - Distinguished Name: /uni/tn-prod/ap-sap_intg/epg-sap_sds
GUI Location:
Tenants > prod > Application Profiles > sap_intg > Application EPGs > sap_sds
*/
resource "aci_application_epg" "Tenant_prod_App_Profile_sap_intg_EPG_sap_sds" {
    depends_on                      = [
        aci_tenant.Tenant_prod,
        aci_application_profile.Tenant_prod_App_Profile_sap_intg,
        aci_bridge_domain.Tenant_prod_Bridge_Domain_sap_itg,
    ]
    application_profile_dn          = aci_application_profile.Tenant_prod_App_Profile_sap_intg.id
    name                            = "sap_sds"
    flood_on_encap                  = "disabled"
    has_mcast_source                = "no"
    is_attr_based_epg               = "no"
    match_t                         = "AtleastOne"
    pc_enf_pref                     = "unenforced"
    pref_gr_memb                    = "include"
    prio                            = "unspecified"
    shutdown                        = "no"
    relation_fv_rs_bd               = aci_bridge_domain.Tenant_prod_Bridge_Domain_sap_itg.id
    relation_fv_rs_aepg_mon_pol     = "uni/tn-common/monepg-default"
}

