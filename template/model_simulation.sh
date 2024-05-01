
#! /bin/bash
mkdir /wspace
cp -r /model/* /wspace
#ls /wspace >>/model/mylog.txt
FN=$(amqp-consume --url="amqp://guest:guest@rabbitmq-service:5672" -q taskqueue -c 1 cat)

echo $FN >> /model/mylog20.txt

cp /wspace/parameter/$FN /wspace/model.in

cd /wspace
 
mono /wspace/Swat_Edit.exe

chmod 700 swat.out 

./swat.out 


cp /wspace/output.rch /model/output.rch.$FN

