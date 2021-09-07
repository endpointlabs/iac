#______________________________________________
#
# Fibre Channel WWNN Pool Variables
#______________________________________________

wwnn_pools = {
  "DEMO" = {
    id_blocks        = [
      {
        from = "20:00:00:25:B5:11:CC:00",
        to = "20:00:00:25:B5:11:CC:FF",
      },
    ]
    organization     = "UCS-DEMO2_FPV-FlexPod"
    pool_purpose     = "WWNN"
    tags = [
      {
        key = "easyucs_origin",
        value = "convert",
      },
      {
        key = "easyucs_version",
        value = "0.9.8",
      },
    ]
  }
}