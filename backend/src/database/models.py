import json
import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

db = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_uri = "sqlite:///{}".format(os.path.join(project_dir, db))

engine = create_engine(database_uri)
Base = declarative_base()


class Drink(Base):
    __tablename__ = 'drinks'
    id = Column(Integer(), primary_key=True)
    title = Column(String(80), unique=True)
    recipe = Column(String(180), nullable=False)

    def short(self):
        recipe = json.loads(self.recipe)
        short_recipe = {'color': recipe["color"], 'parts': recipe["parts"]}
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def __repr__(self):
        return json.dumps(self.short())


# Create the table in the database
Base.metadata.create_all(engine)
