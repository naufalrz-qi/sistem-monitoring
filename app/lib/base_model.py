from app.extensions import db

class BaseModel:
    def __init__(self, model) -> None:
        self.model = model
        
    def create(self):
        query = self.model
        db.session.add(query)
        db.session.commit()
        
    def get(self):
        query = self.model.query.all()
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
        db.delete(*args)
        db.session.commit()
    