import time

import pika
from bson import ObjectId
from mongoengine import connect

from mod02 import Contact

connect(
    db='homework2', host="mongodb+srv://Impelle:Mh200601@cluster0.z0mvkzp.mongodb.net/?retryWrites=true&w=majority"
)

credentials = pika.PlainCredentials('tkpfvxtf', 'vqWLXMuz-T9_HfyVlBdMiBy_lnTi-r5p')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='cow-01.rmq2.cloudamqp.com', port=5672,
                                                               credentials=credentials, virtual_host="tkpfvxtf"))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='email_queue')


def send_email(contact_id):
    contact = Contact.objects.get(id=ObjectId(contact_id))
    print(f" [x] Sending email to {contact.full_name} ({contact.email})...")
    # Тут можна додати реальну логіку надсилання email
    time.sleep(2)  # Імітація часу, потрібного для відправлення email
    print(f" [x] Email sent to {contact.full_name} ({contact.email})")
    contact.message_sent = True
    contact.save()


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    print(f" [x] Received message for contact_id: {contact_id}")
    send_email(contact_id)
    print(" [x] Done")


# Підписка на чергу та очікування повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
