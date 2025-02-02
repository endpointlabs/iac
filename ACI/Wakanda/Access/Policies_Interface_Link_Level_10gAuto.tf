#------------------------------------------
# Create Interface Link Level Policies
#------------------------------------------

/*
API Information:
 - Class: "fabricHIfPol"
 - Distinguished Name: "uni/infra/hintfpol-10gAuto"
GUI Location:
 - Fabric > Access Policies > Policies > Interface > Link Level : 10gAuto
*/
resource "aci_fabric_if_pol" "Link_Level_10gAuto" {
    auto_neg        =  "on"
    fec_mode        =  "inherit"
    link_debounce   =  "100"
    name            =  "10gAuto"
    name_alias      =  "None"
    speed           =  "10G"
}

