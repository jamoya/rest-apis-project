import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        # raise NotImplementedError("Updating an store is not implemented yet" )

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.sesion.delete(store)
        db.session.commit()
        return {"message": "store deleted"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="la cagaste, Burt Lancaster. The storename already exits")
        except SQLAlchemyError:
            abort(500,message="la cagaste, Burt Lancaster. when creating the store")


        return store
