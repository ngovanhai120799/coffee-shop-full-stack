import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from auth.auth import requires_auth
from database.models import Drink, engine
from exceptions.bad_request_exception import BadRequestException
from exceptions.not_found_exception import NotFoundException

Session = sessionmaker(bind=engine)
session = Session()


class DrinkService:
    @requires_auth(permission='get:drinks')
    def get_drinks(self):
        try:
            drinks = []
            query = session.query(Drink).all()
            for drink in query:
                drinks.append(drink.short())
            return {"drinks": drinks}
        except SQLAlchemyError as err:
            raise BadRequestException(422, {
                "message": f"Get error while processing sqlAlchemy: {str(err)}",
                "error": "resource_unprocessable"
            })
        except Exception as err:
            raise BadRequestException(400, {
                "message": f"Bad Request: {str(err)}",
                "error": "resource bad request"
            })

    @requires_auth(permission='get:drinks')
    def get_drinks_detail(self):
        try:
            drinks = []
            query = session.query(Drink).all()
            for drink in query:
                drinks.append(drink.long())
            return {"drinks": drinks}
        except SQLAlchemyError as err:
            raise BadRequestException(422, {
                "message": f"Get error while processing sqlAlchemy: {str(err)}",
                "error": "resource_unprocessable"
            })
        except Exception as err:
            raise BadRequestException(400, {
                "message": f"Bad Request: {str(err)}",
                "error": "resource bad request"
            })

    @requires_auth(permission='post:drinks')
    def post_drink(self, request_body):
        try:
            title = request_body.get("title")
            recipe = request_body.get("recipe")
            new_drink = Drink(title=title, recipe=json.dumps(recipe))
            session.add(new_drink)
            session.commit()

            return {"drinks": new_drink.long()}

        except SQLAlchemyError as err:
            session.rollback()
            raise BadRequestException(422, {
                "message": f"Get error while processing sqlAlchemy: {str(err)}",
                "error": "resource_unprocessable"
            })
        except Exception as err:
            raise BadRequestException(400, {
                "message": f"Bad Request: {str(err)}",
                "error": "resource bad request"
            })

    @requires_auth(permission='patch:drinks')
    def patch_drinks(self, _id, request_body):
        try:
            title = request_body.get("title", None)
            recipe = request_body.get("recipe", None)
            drink = session.query(Drink).where(Drink.id == _id).one_or_none()
            if not drink:
                raise NotFoundException(404, {
                    "message": f"No row was found when one was required",
                    "error": "no resource found"
                })
            if title:
                drink.title = title
            if recipe:
                drink.recipe = json.dumps(recipe)

            session.commit()
            return {"drinks": drink.long()}
        except SQLAlchemyError as err:
            session.rollback()
            raise BadRequestException(422, {
                "message": f"Get error while processing sqlAlchemy: {str(err)}",
                "error": "resource_unprocessable"
            })
        except Exception as err:
            raise BadRequestException(400, {
                "message": f"Bad Request: {str(err)}",
                "error": "resource bad request"
            })

    @requires_auth(permission='delete:drinks')
    def delete_drinks(self, _id):
        try:
            drink = session.query(Drink).where(Drink.id == _id).one_or_none()
            if not drink:
                raise NotFoundException(404, {
                    "message": f"No row was found when one was required",
                    "error": "no resource found"
                })
            session.delete(drink)
            session.commit()

        except SQLAlchemyError as err:
            session.rollback()
            raise BadRequestException(422, {
                "message": f"Get error while processing sqlAlchemy: {str(err)}",
                "error": "resource_unprocessable"
            })
        except Exception as err:
            raise BadRequestException(400, {
                "message": f"Bad Request: {str(err)}",
                "error": "resource bad request"
            })

    def drop_and_create(self):
        try:
            session.query(Drink).delete()
            drink = Drink(
                title='water',
                recipe='[{"name": "water", "color": "blue", "parts": 1}]')
            session.add(drink)
            session.commit()
            import json
            return json.dumps(drink.short())
        except Exception as e:
            raise e
