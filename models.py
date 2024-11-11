from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty

class User(StructuredNode):
    uid= IntegerProperty(UniqueIdProperty=True, Required=True, db_property="id")
    screen_name = StringProperty()
    name = StringProperty()
    sex = IntegerProperty()
    home_town = StringProperty()
    follows = RelationshipTo('User', 'Follow')
    subscribes_to = RelationshipTo('Group', 'Subscribe')

class Group(StructuredNode):
    uid= IntegerProperty(UniqueIdProperty=True, Required=True, db_property="id")
    name = StringProperty()
    screen_name = StringProperty()
    subscribers = RelationshipFrom('User', 'Subscribe')