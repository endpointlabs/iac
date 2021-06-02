#------------------------------------------
# Create a Static Node Mgmt Address
#------------------------------------------

/*
API Information:
 - Class: "mgmtRsOoBStNode"
 - Distinguished Name: "uni/tn-mgmt/mgmtp-default/oob-default/rsooBStNode-[topology/pod-1/node-201]"
GUI Location:
 - Tenants > mgmt > Node Management Addresses > Static Node Management Addresses
*/
resource "aci_static_node_mgmt_address" "Pod_1_Node_201_Mgmt_EPG_out_of_band_EPG_default_Static_Address" {
    depends_on          = [
        aci_node_mgmt_epg.Mgmt_EPG_out_of_band_EPG_default
    ]
    management_epg_dn   = aci_node_mgmt_epg.Mgmt_EPG_out_of_band_EPG_default.id
    t_dn                = "topology/pod-1/node-201"
    type                = "out_of_band"
    addr                = "198.18.1.201/24"
    gw                  = "198.18.1.1"
    v6_addr             = "::"
    v6_gw               = "::"
}

