class BaseModel:
    def __init__(self, model) -> None:
        self.model = model
        self.db = None
        
    def get(self):
        query = self.model.qouery.all()
        return query
    
    def get_one(self, id):
        query = self.model.query.filter_by(id=id).first()
        return query
    
    def edit(self):
        return self.db.session.commit()
    
    def delete(self, *args):
        self.db.delete(*args)
        self.db.session.commit()
    