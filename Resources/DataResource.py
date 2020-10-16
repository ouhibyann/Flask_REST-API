from flask_restful import Resource

from models.db import db
from models.data import Data, DataSchema
from sqlalchemy.sql import func

Datas_schema = DataSchema(many=True)
DataSchema = DataSchema()


class DataResource(Resource):
    @classmethod
    def get(cls):
        fields = ['Name', 'Value', 'Created_date']
        req = Data.query.options(db.load_only(*fields))
        # The response will contain the id as it is defined as PRIMARY KEY
        arr = Datas_schema.dump(req)

        created_date = []
        name = []
        value = []
        for x in arr:
            created_date.append(x['Created_date'])
            name.append(x['Name'])
            value.append(x['Value'])
        # An array has been asked in the subject, so here it is
        arr = [['name', name], ['value', value]]

        # SELECT AVG(Value) FROM Data ORDER BY Name, Created_date
        qry = db.session.query(func.avg(Data.Value), Data.Name, Data.Created_date)
        req2 = qry.group_by(Data.Name, Data.Created_date).all()
        avg = []
        for res in req2:
            print(res)
            avg.append(str(res))
        print(avg)

        arr = [['name', name], ['value', value], ['AVG_name_date', avg]]
        return arr, 200
