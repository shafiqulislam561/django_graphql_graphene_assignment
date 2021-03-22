import graphene
from graphene_django import DjangoObjectType

from events.myevent.models import Event, Location, EventMember

class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ("name", "description", "location")

class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = ("lattitude", "altitude")

class EventMemberType(DjangoObjectType):
    class Meta:
        model = EventMember
        fields = ("user_id", "event")

class Query(graphene.ObjectType):
    all_events = graphene.List(EventType)
    event_by_eventmember = graphene.Field(EventType, user_id=graphene.Int())
    location = graphene.Field(LocationType)

    def resolve_all_events(root, info):
        return Event.objects.select_related("location").all()

    def resolve_event_by_eventmember(root, info, user_id):
        try:
            return EventMember.objects.get(user_id=user_id).event
        except EventMember.DoesNotExist:
            return None


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        lattitude = graphene.Float()
        altitude = graphene.Float()
        id = graphene.ID()

    event = graphene.Field(EventType)
    ok = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, name, description, lattitude, altitude):
        location = Location(lattitude=lattitude,altitude=altitude)
        event = Event(name=name,description=description,location=location)
        ok = True
        return CreateEvent(event=event, ok=ok)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, id):
        Event = Event.objects.get(pk=id)
        Event.delete()
        ok = True
        return DeleteEvent(ok=ok)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        description = graphene.String()

    event = graphene.Field(EventType)
    ok = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, id, name, description):
        event = Event.objects.get(pk=id)
        event.name = name
        event.description = description
        event.save()
        ok = True
        return DeleteEvent(event=event, ok=ok)


class MyMutations(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations)

mutation_string ='''
    mutation myFirstMutation {
        createEvent (name:"Django",description:"abc",lattitude:1.0,altitude=2.0){
            event{
                name
                description
                location {
                    lattitude
                    altitude
                }
            }
        }
    }
'''
# result = schema.execute(mutation_string)
# assert result.data["createEvent"]
