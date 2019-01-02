from mongoengine import *
import os

connect('mongoengine-test', host=os.environ['RABBITMQ_SERVER'], port=27017)


class Animal(Document):
    genus = StringField()
    family = StringField()
    photo = FileField()


marmot = Animal(genus='Marmota', family='Sciuridae')
# save file to gridfs
marmot_photo = open('marmot.jpg', 'rb')
marmot.photo.put(marmot_photo, content_type = 'image/jpeg')
marmot.save()

# read file from gridfs
marmot = Animal.objects(genus='Marmota').first()
photo = marmot.photo.read()
content_type = marmot.photo.content_type
print(content_type)