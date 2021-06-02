/*
API Information:
 - Class: "infraSpAccPortP"
 - Distinguished Name: "uni/infra/spaccportprof-asgard-spine102"
GUI Location:
 - Fabric > Access Policies > Interfaces > Spine Interfaces > Profiles > asgard-spine102
*/
resource "aci_spine_interface_profile" "Interface_Profile_asgard-spine102" {
    name        = "asgard-spine102"
}

#------------------------------------------
# Create Spine Interface Selector
#  - Attach Port Block
#  - Attach Spine Interface Policy Group
#------------------------------------------

/*
API Information:
 - Class: "infraSHPortS"
 - Distinguished Name: "uni/infra/spaccportprof-asgard-spine102/shports-Eth1-29-typ-range"
GUI Location:
 - Fabric > Access Policies > Interfaces > Spine Interfaces > Profiles > asgard-spine102:Eth1-29
*/
resource "aci_rest" "Spine_Interface_Profile_asgard-spine102_Selector_Eth1-29" {
    depends_on  = [
        aci_spine_interface_profile.Interface_Profile_asgard-spine102
    ]
    path        = "/api/node/mo/uni/infra/spaccportprof-asgard-spine102/shports-Eth1-29-typ-range.json"
    class_name  = "infraSHPortS"
    payload     = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "descr": "143b-core-E1/24",
            "dn": "uni/infra/spaccportprof-asgard-spine102/shports-Eth1-29-typ-range",
            "name": "Eth1-29",
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "descr": "",
                        "dn": "uni/infra/spaccportprof-asgard-spine102/shports-Eth1-29-typ-range/portblk-Eth1-29",
                        "fromCard": "1",
                        "fromPort": "29",
                        "toCard": "1",
                        "toPort": "29",
                        "name": "Eth1-29",
                    }
                }
            },
            {
                "infraRsSpAccGrp": {
                    "attributes": {
                        "tDn": "uni/infra/funcprof/spaccportgrp-default"
                    }
                }
            }
        ]
    }
}
    EOF
}

#------------------------------------------
# Create Spine Interface Selector
#  - Attach Port Block
#  - Attach Spine Interface Policy Group
#------------------------------------------

/*
API Information:
 - Class: "infraSHPortS"
 - Distinguished Name: "uni/infra/spaccportprof-asgard-spine102/shports-Eth1-30-typ-range"
GUI Location:
 - Fabric > Access Policies > Interfaces > Spine Interfaces > Profiles > asgard-spine102:Eth1-30
*/
resource "aci_rest" "Spine_Interface_Profile_asgard-spine102_Selector_Eth1-30" {
    depends_on  = [
        aci_spine_interface_profile.Interface_Profile_asgard-spine102
    ]
    path        = "/api/node/mo/uni/infra/spaccportprof-asgard-spine102/shports-Eth1-30-typ-range.json"
    class_name  = "infraSHPortS"
    payload     = <<EOF
{
    "infraSHPortS": {
        "attributes": {
            "descr": "143c-core-E1/24",
            "dn": "uni/infra/spaccportprof-asgard-spine102/shports-Eth1-30-typ-range",
            "name": "Eth1-30",
        },
        "children": [
            {
                "infraPortBlk": {
                    "attributes": {
                        "descr": "",
                        "dn": "uni/infra/spaccportprof-asgard-spine102/shports-Eth1-30-typ-range/portblk-Eth1-30",
                        "fromCard": "1",
                        "fromPort": "30",
                        "toCard": "1",
                        "toPort": "30",
                        "name": "Eth1-30",
                    }
                }
            },
            {
                "infraRsSpAccGrp": {
                    "attributes": {
                        "tDn": "uni/infra/funcprof/spaccportgrp-default"
                    }
                }
            }
        ]
    }
}
    EOF
}

