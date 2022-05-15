from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config,EmailProperty, UniqueIdProperty, IntegerProperty , StructuredRel
from neomodel import db
config.DATABASE_URL = 'bolt://neo4j:yazlab@localhost:7687'
class User(StructuredNode):
    email = EmailProperty(unique_index=True)
    password = StringProperty()


class Researcher(StructuredNode):
    researcher_id = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    surname = StringProperty(unique_index=True)
    article = RelationshipTo('Article', 'AUTHOR')


class Article(StructuredNode):
    article_id = UniqueIdProperty()
    name = StringProperty(unique_index=False)
    year = IntegerProperty(unique_index=True)
    type = RelationshipTo('Type', 'TYPE')
    researcher = RelationshipFrom("Researcher","AUTHOR")
    #publication_place = StringProperty()

class Type(StructuredNode):
    type_id = UniqueIdProperty()
    name = StringProperty(unique_index=False)
    publication_place = StringProperty(unique_index=True)

# asd = 'test'
# asdd = 'test'

# query = "MATCH (article:Article {name: '"+asd+"'})<-[:AUTHOR]-(researcher:Researcher {name: '"+asdd+"'}) RETURN researcher.name,researcher.researcher_id,article.name"
# print(query)
# results, meta = db.cypher_query(query)
# print(results)

# name = "test"
# article_name = "test"
# year = "2011"
# article = Article.nodes.first(name=article_name,year=year)
# researcher = Researcher.nodes.first(name=name)
# for article in researcher.article.match(name=article_name):
#     print(article)


# article = Type.nodes.first()
# article.delete()

