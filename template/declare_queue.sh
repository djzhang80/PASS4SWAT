#export $BROKER_URL=amqp://guest:guest@rabbitmq-service:5672
echo "start initialize queue"
amqp-declare-queue -d --url=amqp://guest:guest@rabbitmq-service:5672 -q taskqueue>>/model/cq10.log
rm -rf /model/*.log
DIRECTORY="/model/parameter"

for FILE in "$DIRECTORY"/*; do
    # Extract file name
    FILENAME=$(basename "$FILE")

    # Send file name to RabbitMQ exchange
    amqp-publish --url=amqp://guest:guest@rabbitmq-service:5672 -r taskqueue -b "$FILENAME"
    #FN=$(amqp-consume --url="amqp://guest:guest@rabbitmq-service:5672" -q taskqueue -c 1 cat)

    #echo a$FN >> /model/mylog110.log
    
    echo "Sent $FILENAME to RabbitMQ">>/model/enqueue110.log
    #amqp-publish --url=amqp://guest:guest@rabbitmq-service:5672 -r taskqueue -b "$FILENAME"
done


