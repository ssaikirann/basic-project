apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${app_name}
  namespace: ${namespace}
  labels:
    app: ${app_name}
spec:
  replicas: ${replicas}
  selector:
    matchLabels:
      app: ${app_name}
  template:
    metadata:
      labels:
        app: ${app_name}
    spec:
      containers:
      - name: ${app_name}
        image: ${docker_image}
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          name: http
        resources:
          requests:
            memory: "${memory_request}"
            cpu: "${cpu_request}"
          limits:
            memory: "${memory_limit}"
            cpu: "${cpu_limit}"
        envFrom:
        - configMapRef:
            name: ${app_name}-config
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import finance_tracker; print('OK')"
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          exec:
            command:
            - python
            - -c
            - "import finance_tracker; print('OK')"
          initialDelaySeconds: 5
          periodSeconds: 10
