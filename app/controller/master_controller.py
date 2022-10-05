from flask import Blueprint, jsonify, request
from app.models.master_model import *
from app.lib.base_model import BaseModel
from app.lib.status_code import *

master = Blueprint('master', __name__, url_prefix='/api/v2/master')

class Kelas:
    @master.route('/kelas/create', methods=['POST','GET'])
    def create():
        kelas = request.json.get('kelas')
        
        base = BaseModel(KelasModel(kelas=kelas))
        kelas_check = base.get_one_or_none(kelas=kelas)
        if kelas_check:
            return jsonify(msg='Data Class has been already exists.'), HTTP_409_CONFLICT
        else:
            base.create()        
            return jsonify(kelas=base.model.kelas), HTTP_201_CREATED
        
    @master.route('/kelas/get-all', methods=['GET'])
    def get_all():
        base = BaseModel(KelasModel)
        model = base.get()
        
        data = []
        for kelas in model:
            data.append({
                'id' : kelas.id,
                'kelas' : kelas.kelas,
                'laki' : kelas.jml_laki,
                'perempuan' : kelas.jml_perempuan
            })
            
        return jsonify({
            'data' : data
        }), HTTP_200_OK
        
    @master.route('/kelas/get-one/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def get_one(id):
        base = BaseModel(KelasModel)
        model = base.get_one_or_none(id=id)
        
        if request.method == 'GET':
            if model is not None:
                return jsonify(id=model.id, kelas= model.kelas,
                               laki = model.jml_laki,
                               perempuan = model.jml_perempuan
                               )
            else:
                return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
        
        elif request.method == 'PUT':
            kelas = request.json.get('kelas')
            
            class_check = base.get_one_or_none(kelas=kelas)
            if class_check:
                return jsonify(msg=f'Data dengan {kelas} sudah ada.')      
            else:
                model.kelas = kelas
                base.edit()            
                return jsonify(id=model.id, kelas=model.kelas), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
class Mapel(object):
    # @master.add_url_rule('/mapel/create', methods=['POST','GET'])       
    @master.route('/mapel/create', endpoint='mapel', methods=['POST','GET'])
    def create():
        mapel = request.json.get('mapel')
        
        base = BaseModel(MapelModel(mapel=mapel))
        mapel_check = base.get_one_or_none(mapel=mapel)
        if mapel_check:
            return jsonify(msg='Data Class has been already exists.'), HTTP_409_CONFLICT
        else:
            base.create()        
            return jsonify(mapel=base.model.mapel), HTTP_201_CREATED
        
    @master.route('/mapel/get-all', endpoint='mapel-all', methods=['GET'])
    def get_all():
        base = BaseModel(MapelModel)
        model = base.get()
        
        data = []
        for mapel in model:
            data.append({
                'id' : mapel.id,
                'mapel' : mapel.mapel
            })
            
        return jsonify({
            'data' : data
        }), HTTP_200_OK
        
    @master.route('/mapel/get-one/<int:id>', endpoint='mapel-single', methods=['GET', 'PUT', 'DELETE'])
    def get_one(id):
        base = BaseModel(MapelModel)
        model = base.get_one_or_none(id=id)
        
        if request.method == 'GET':
            if model is not None:
                return jsonify(id=model.id, mapel= model.mapel)
            else:
                return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
                
        elif request.method == 'PUT':
            mapel = request.json.get('mapel')
            
            class_check = base.get_one_or_none(mapel=mapel)
            if class_check:
                return jsonify(msg=f'Data dengan {mapel} sudah ada.')      
            else:
                model.mapel = mapel
                base.edit()            
                return jsonify(id=model.id, mapel=model.mapel), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
class Hari(object):
    @master.route('/hari/create', endpoint='hari', methods=['POST','GET'])
    def create():
        hari = request.json.get('hari')
        
        base = BaseModel(HariModel(hari=hari))
        hari_check = base.get_one_or_none(hari=hari)
        if hari_check:
            return jsonify(msg='Data Class has been already exists.'), HTTP_409_CONFLICT
        else:
            base.create()        
            return jsonify(hari=base.model.hari), HTTP_201_CREATED
        
    @master.route('/hari/get-all', endpoint='hari-all', methods=['GET'])
    def get_all():
        base = BaseModel(HariModel)
        model = base.get()
        
        data = []
        for hari in model:
            data.append({
                'id' : hari.id,
                'hari' : hari.hari
            })
            
        return jsonify({
            'data' : data
        }), HTTP_200_OK
        
    @master.route('/hari/get-one/<int:id>', endpoint='hari-single', methods=['GET', 'PUT', 'DELETE'])
    def get_one(id):
        base = BaseModel(HariModel)
        model = base.get_one_or_none(id=id)
        
        if request.method == 'GET':
            if model is not None:
                return jsonify(id=model.id, hari= model.hari)
            else:
                return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
                
        elif request.method == 'PUT':
            hari = request.json.get('hari')
            
            class_check = base.get_one_or_none(hari=hari)
            if class_check:
                return jsonify(msg=f'Data dengan {hari} sudah ada.')      
            else:
                model.hari = hari
                base.edit()            
                return jsonify(id=model.id, hari=model.hari), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
class TahunAjaran(object):
    @master.route('/ajaran/create', endpoint='ajaran', methods=['POST','GET'])
    def create():
        ajaran = request.json.get('ajaran')
        
        base = BaseModel(TahunAjaranModel(ajaran=ajaran))
        ajaran_check = base.get_one_or_none(th_ajaran=ajaran)
        if ajaran_check:
            return jsonify(msg='Data Class has been already exists.'), HTTP_409_CONFLICT
        else:
            base.create()        
            return jsonify(ajaran=base.model.th_ajaran), HTTP_201_CREATED
        
    @master.route('/ajaran/get-all', endpoint='ajaran-all', methods=['GET'])
    def get_all():
        base = BaseModel(TahunAjaranModel)
        model = base.get()
        
        data = []
        for ajaran in model:
            data.append({
                'id' : ajaran.id,
                'th_ajaran' : ajaran.th_ajaran,
                'active' : True  if ajaran.is_active == "0" else False 
            })
            
        return jsonify({
            'data' : data
        }), HTTP_200_OK
        
    @master.route('/ajaran/get-one/<int:id>', endpoint='ajaran-single', methods=['GET', 'PUT', 'DELETE'])
    def get_one(id):
        base = BaseModel(TahunAjaranModel)
        model = base.get_one_or_none(id=id)
        
        if request.method == 'GET':
            if model is not None:
                return jsonify(id=model.id, 
                               ajaran= model.th_ajaran,
                               active= True if model.is_active == "0" else False)
            else:
                return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
                
        elif request.method == 'PUT':
            ajaran = request.json.get('ajaran')
            
            class_check = base.get_one_or_none(th_ajaran=ajaran)
            if class_check:
                return jsonify(msg=f'Data dengan {ajaran} sudah ada.')      
            else:
                model.th_ajaran = ajaran
                base.edit()            
                return jsonify(id=model.id, ajaran=model.th_ajaran), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
class Semester(object):
    @master.route('/semester/create', endpoint='semester', methods=['POST','GET'])
    def create():
        semester = request.json.get('semester')
        active = request.json.get('active')
        
        base = BaseModel(SemesterModel(semester, active))
        sms_check = base.get_one_or_none(semester=semester)
        if sms_check:
            return jsonify(msg='Data Class has been already exists.'), HTTP_409_CONFLICT
        else:
            base.create()        
            return jsonify(ajaran=base.model.semester), HTTP_201_CREATED
        
    @master.route('/semester/get-all', endpoint='semester-all', methods=['GET'])
    def get_all():
        base = BaseModel(SemesterModel)
        model = base.get()
        
        data = []
        for sms in model:
            data.append({
                'id' : sms.id,
                'semester' : sms.semester,
                'active' : True  if sms.is_active == "0" else False 
            })
            
        return jsonify({
            'data' : data
        }), HTTP_200_OK
        
    @master.route('/semester/get-one/<int:id>', endpoint='semester-single', methods=['GET', 'PUT', 'DELETE'])
    def get_one(id):
        base = BaseModel(SemesterModel)
        model = base.get_one_or_none(id=id)
        
        if request.method == 'GET':
            if model is not None:
                return jsonify(id=model.id, 
                               semester= model.semester,
                               active= True if model.is_active == "0" else False)
            else:
                return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
                
        elif request.method == 'PUT':
            semester = request.json.get('semester')
            active = request.json.get('active')
            
            class_check = base.get_one_or_none(semester=semester)
            if class_check:
                return jsonify(msg=f'Data dengan {semester} sudah ada.')      
            else:
                model.semester = semester
                model.is_active = active
                base.edit()            
                return jsonify(id=model.id, semester=semester), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
