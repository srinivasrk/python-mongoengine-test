from mongoengine import *
import os

connect('mongoengine-test', host=os.environ['RABBITMQ_SERVER'], port=27017)


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)  # this is similar to foreign key in traditional ORM
    tags = ListField(StringField(max_length=30))  # means a list of string can be stored
    comments = ListField(EmbeddedDocumentField(Comment))
    meta = {'allow_inheritance': True}  # need to set this to true to use Inheritance on class model


class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()


# Working with ORM

ross = User(email='ross@example.com', first_name='Ross', last_name='Lawley').save()
john = User(email='john@example.com', first_name='John', last_name='Doe').save()

post1 = TextPost(title='Fun with MongoEngine', author=john)
post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
post1.tags = ['mongodb', 'mongoengine']
post1.save()

post2 = LinkPost(title='MongoEngine Documentation', author=ross)
post2.link_url = 'http://docs.mongoengine.com/'
post2.tags = ['mongoengine']
post2.save()


for post in Post.objects:
    print(post)
    print(post.title)

