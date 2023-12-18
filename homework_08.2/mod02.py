from mongoengine import connect, Document, StringField, BooleanField, EmailField

connect(
    db = 'homework2', host="mongodb+srv://Impelle:Mh200601@cluster0.z0mvkzp.mongodb.net/?retryWrites=true&w=majority"
)

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
