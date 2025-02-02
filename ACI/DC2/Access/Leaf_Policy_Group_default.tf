#------------------------------------------
# Create Leaf Policy Group
#------------------------------------------

/*
API Information:
 - Class: "infraAccNodePGrp"
 - Distinguished Name: "uni/infra/funcprof/accnodepgrp-default"
GUI Location:
 - Fabric > Access Policies > Switches > Leaf Switches > Policy Groups: default

802.1x Node Authentication Policy
 - Class: "l2NodeAuthPol"
 - Distinguished Name: "uni/infra/nodeauthpol-default"
BFD IPv4 Policy
 - Class: "bfdIpv4InstPol"
 - Distinguished Name: "uni/infra/bfdIpv4Inst-default"
BFD IPv6 Policy
 - Class: "bfdIpv6InstPol"
 - Distinguished Name: "uni/infra/bfdIpv6Inst-default"
CDP Policy
 - Class: "cdpIfPol"
 - Distinguished Name: "uni/infra/cdpIfP-"
CoPP Leaf Policy
 - Class: "coppLeafProfile"
 - Distinguished Name: "uni/infra/coppleafp-default"
CoPP Pre-Filter
 - Class: "iaclLeafProfile"
 - Distinguished Name: "uni/infra/iaclleafp-default"
Equipment Flash Config
 - Class: "equipmentFlashConfigPol"
 - Distinguished Name: "uni/infra/flashconfigpol-default"
Fast Link Failover Policy
 - Class: "topoctrlFastLinkFailoverInstPol"
 - Distinguished Name: "uni/infra/fastlinkfailoverinstpol-default"
Fibre Channel SAN Policy
 - Class: "fcFabricPol"
 - Distinguished Name: "uni/infra/fcfabricpol-default"
Fibre Channel Node Policy
 - Class: "fcInstPol"
 - Distinguished Name: "uni/infra/fcinstpol-default"
Forward Scale Profile Policy
 - Class: "topoctrlFwdScaleProfilePol"
 - Distinguished Name: "uni/infra/fwdscalepol-default"
LLDP Policy
 - Class: "lldpIfPol"
 - Distinguished Name: "uni/infra/lldpIfP-lldpEnabled"
Monitoring Policy
 - Class: "monInfraPol"
 - Distinguished Name: "uni/infra/moninfra-default"
Netflow Node Policy
 - Class: "netflowNodePol"
 - Distinguished Name: "uni/infra/nodepol-default"
PoE Node Policy
 - Class: "poeInstPol"
 - Distinguished Name: "uni/infra/poeInstP-default"
Spanning Tree Policy (MSTP)
 - Class: "stpInstPol"
 - Distinguished Name: "uni/infra/mstpInstPol-default"
*/
resource "aci_rest" "Leaf_Policy_Group_default" {
  path       = "/api/node/mo/uni/infra/funcprof/accnodepgrp-default.json"
  class_name = "infraAccNodePGrp"
  payload    = <<EOF
{
    "infraAccNodePGrp": {
        "attributes": {
        "dn": "uni/infra/funcprof/accnodepgrp-default",
        "descr": "Default Leaf Policy Group",
        "name": "default"
        },
        "children": [
            {
                "infraRsMstInstPol": {
                    "attributes": {
                        "tnStpInstPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsBfdIpv4InstPol": {
                    "attributes": {
                        "tnBfdIpv4InstPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsBfdIpv6InstPol": {
                    "attributes": {
                        "tnBfdIpv6InstPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsEquipmentFlashConfigPol": {
                    "attributes": {
                        "tnEquipmentFlashConfigPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsFcFabricPol": {
                    "attributes": {
                        "tnFcFabricPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsFcInstPol": {
                    "attributes": {
                        "tnFcInstPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsMonNodeInfraPol": {
                    "attributes": {
                        "tnMonInfraPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsPoeInstPol": {
                    "attributes": {
                        "tnPoeInstPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsNetflowNodePol": {
                    "attributes": {
                        "tnNetflowNodePolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsLeafCoppProfile": {
                    "attributes": {
                        "tnCoppLeafProfileName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsTopoctrlFwdScaleProfPol": {
                    "attributes": {
                        "tnTopoctrlFwdScaleProfilePolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsTopoctrlFastLinkFailoverInstPol": {
                    "attributes": {
                        "tnTopoctrlFastLinkFailoverInstPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsL2NodeAuthPol": {
                    "attributes": {
                        "tnL2NodeAuthPolName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsIaclLeafProfile": {
                    "attributes": {
                        "tnIaclLeafProfileName": "default"
                    },
                    "children": []
                }
            },
            {
                "infraRsLeafPGrpToCdpIfPol": {
                    "attributes": {
                        "tnCdpIfPolName": "cdpEnabled"
                    },
                    "children": []
                }
            },
            {
                "infraRsLeafPGrpToLldpIfPol": {
                    "attributes": {
                        "tnLldpIfPolName": "lldpEnabled"
                    },
                    "children": []
                }
            },
        ]
    }
}
  EOF
}

