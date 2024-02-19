from flask import request, jsonify
from transformers import TinyBertTokenizer, TinyBertForSequenceClassification
import torch
import redis
import pika

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Load the tokenizer and model
tokenizer = TinyBertTokenizer.from_pretrained('prajjwal1/tf-tinybert')
model = TinyBertForSequenceClassification.from_pretrained('prajjwal1/tf-tinybert')

# Initialize Redis client
redis_client = redis.Redis(host=config['redis']['host'], port=config['redis']['port'])

# Initialize RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=config['rabbitmq']['host'], port=config['rabbitmq']['port']))
channel = connection.channel()
channel.queue_declare(queue='tasks', durable=True)

def process_message(ch, method, properties, body):
    try:
        # Decode and process the input text
        input_text = body.decode()
        input_ids = tokenizer.encode(input_text, add_special_tokens=True, return_tensors="pt")
        outputs = model(input_ids)
        predictions = outputs.logits.argmax(dim=-1).item()

        # Cache the result
        redis_client.set(input_text, predictions)
    except Exception as e:
        print(f"Error processing message: {e}")

def predict():
    try:
        # Get input text from request
        input_text = request.json.get('text')

        if not input_text:
            return jsonify({'error': 'Input text is required'}), 400

        # Check if input text exists in cache
        prediction = redis_client.get(input_text)
        if prediction:
            return jsonify({'predicted_class': int(prediction)})

        # Publish input text to RabbitMQ for processing
        channel.basic_publish(exchange='',
                              routing_key='tasks',
                              body=input_text,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))

        # Return response indicating processing
        return jsonify({'message': 'Processing input...'})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Set up RabbitMQ consumer
channel.basic_consume(queue='tasks', on_message_callback=process_message, auto_ack=True)
print('Waiting for messages...')
channel.start_consuming()
