apiVersion: v1
kind: ConfigMap
metadata:
  name: ${app_name}-config
  namespace: ${namespace}
data:
  APP_NAME: "${app_name}"
  LOG_LEVEL: "INFO"
