#! /bin/bash
 
FN=$(amqp-consume --url="$BROKER_URL" -q foo -c 1)

cp /var/local/input/$FN /swat/model.in

cd /swat
 
mono /swat/swat_edit.exe

chmod 700 swat.out 

./swat.out 

awk -v RNO="$RNO" -v VNO="$VNO" -v FN="$FN" '/^REACH *'"$RNO"'/ {print $VNO}' output.rch > /var/local/output/$FN

