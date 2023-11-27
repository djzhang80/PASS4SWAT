amqp-declare-queue --url=$BROKER_URL -q taskqueue -d the queue contains all the names of parameter files

DIRECTORY="/var/local/input"

for FILE in "$DIRECTORY"/*; do
    # Extract file name
    FILENAME=$(basename "$FILE")

    # Send file name to RabbitMQ exchange
    amqp-publish --url=$BROKER_URL -r taskqueue -b "$FILE"
    
    echo "Sent $FILENAME to RabbitMQ"
done