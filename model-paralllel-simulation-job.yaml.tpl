apiVersion: batch/v1
kind: Job
metadata:
  name: job-swat
spec:
  completions: scount
  parallelism: pcount
  template:
    metadata:
      name: job-pod
    spec:
      containers:
        - name: swat
          image: execution_image
          command: ["/bin/bash", "execution_script"]
          volumeMounts:
            - mountPath: mount_path_in_container
              name: model
      volumes:
        - name: model
          hostPath:
            path: path_to_your_project
            type: Directory
      restartPolicy: OnFailure
