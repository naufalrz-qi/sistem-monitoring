from app.backend.extensions import db
from flask import jsonify

class BaseModel:
    def __init__(self, model=None) -> None:
        self.model = model
        
    def create(self):
        query = self.model
        db.session.add(query)
        db.session.commit()
        
    def get_all(self):
        query = self.model.query.all()
        return query
    
    def get_all_filter(self, **kwargs):
        query =self.model.query.filter_by(**kwargs).all()
        return query
    
    def get_one(self, **kwargs):
        query = self.model.query.filter_by(**kwargs).first()
        return query
    
    def get_one_or_none(self, **kwargs):
        query = self.model.query.filter_by(**kwargs).one_or_none()
        return query
    
    def edit(self):
        return db.session.commit()
    
    def delete(self, *args):        
        db.session.delete(*args)
        db.session.commit()
    
        
class BaseModel2:
    def __init__(self, model):
        self.model = model 
        
    def get_all(self):
        items = self.model.query.all()
        return items
    
    def _get_item(self, id):
        return self.model.query.get_or_404(id)
    
    def get_one(self, id):
        return self._get_item(id)
        
    