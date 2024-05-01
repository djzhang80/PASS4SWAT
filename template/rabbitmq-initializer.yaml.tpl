apiVersion: v1
kind: Pod
metadata:
  name: queue-initializer
spec:
  containers:
    - name: swat-container
      image: jannyarj/base:1.0
      command: ["/bin/bash", "/model/declare_queue.sh"]
      #keep containner alive
      #command: ["tail"]
      #args: ["-f", "/dev/null"]
      volumeMounts:
        - name: model
          mountPath: /model/
  volumes:
      - name: model
        hostPath:
          path: path_to_your_project
          type: Directory
  restartPolicy: OnFailure
