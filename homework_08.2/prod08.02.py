import pika
from faker import Faker
from mongoengine import connect

from mod02 import Contact

# З'єднання з MongoDB
connect(
    db='homework2', host="mongodb+srv://Impelle:Mh200601@cluster0.z0mvkzp.mongodb.net/?retryWrites=true&w=majority"
)

credentials = pika.PlainCredentials('tkpfvxtf', 'vqWLXMuz-T9_HfyVlBdMiBy_lnTi-r5p')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='cow-01.rmq2.cloudamqp.com',
    port=5672,
    credentials=credentials,
    virtual_host="tkpfvxtf"
))
channel = connection.channel()
channel.queue_declare(queue='email_queue')


def generate_and_send_contacts(num_contacts):
    fake = Faker()
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=str(contact.id))
        print(f" [x] Sent {full_name} ({email}) to the email_queue")


generate_and_send_contacts(5)

connection.close()
