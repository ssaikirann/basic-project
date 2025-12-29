apiVersion: v1
kind: Service
metadata:
  name: ${app_name}-service
  namespace: ${namespace}
  labels:
    app: ${app_name}
spec:
  type: LoadBalancer
  ports:
  - port: ${port}
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: ${app_name}
