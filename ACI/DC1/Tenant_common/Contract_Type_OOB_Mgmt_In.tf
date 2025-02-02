#------------------------------------------
# Create a Out-Of-Band Contract
#------------------------------------------

/*
API Information:
 - Class: "vzOOBBrCP"
 - Distinguished Name: "uni/tn-common/oobbrc-Mgmt_In"
GUI Location:
 - Tenants > common > Contracts > Out-Of-Band Contracts: Mgmt_In
*/
resource "aci_rest" "Tenant_common_Contract_Type_OOB_Mgmt_In" {
    path        = "/api/node/mo/uni/tn-common/oobbrc-Mgmt_In.json"
    class_name  = "vzOOBBrCP"
    payload     = <<EOF
{
    "vzOOBBrCP": {
        "attributes": {
            "descr": "Out-of-Band Inbound Traffic",
            "dn": "uni/tn-common/oobbrc-Mgmt_In",
            "name": "Mgmt_In",
            "prio": "unspecified",
            "scope": "global",
            "targetDscp": "unspecified"
        },
        "children": [ ]
    }
}
    EOF
}


