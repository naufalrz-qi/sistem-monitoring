from flask import Blueprint, jsonify, request
from ..models.master_model import *
from ..lib.base_model import BaseModel
from ..lib.status_code import *
from sqlalchemy import func

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
        
    @master.route('/kelas/get-all', endpoint='kelas_all', methods=['GET'])
    def get_all():
        base = BaseModel(KelasModel)
        model = base.get_all()
        
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
            return jsonify(msg=f'Data mata pelajaran {base.model.mapel} telah di tambahkan.'), HTTP_201_CREATED
        
    @master.route('/mapel/get-all', endpoint='mapel-all', methods=['GET'])
    def get_all():
        base = BaseModel(MapelModel)
        model = base.get_all()
        
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
            
            mapel_check = base.get_one_or_none(mapel=mapel)
            if mapel_check:
                return jsonify(msg=f'Data dengan {mapel} sudah ada.')      
            else:
                model.mapel = mapel
                base.edit()            
                return jsonify(msg=f'Data mapel {model.mapel}, telah di perbaharui.'), HTTP_200_OK
        
        elif request.method == 'DELETE':
            if not model:
                return jsonify(msg='Data Mata Pelajaran tidak ada di database.'), HTTP_404_NOT_FOUND
            else:
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
        model = base.get_all()
        
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
        status = request.json.get('status')
        
        base = BaseModel(TahunAjaranModel(ajaran=ajaran, status=status))
        ajaran_check = base.get_one_or_none(th_ajaran=ajaran)
        if ajaran_check:
            return jsonify(msg='Data Class has been already exists.'), HTTP_409_CONFLICT
        else:
            base.create()        
            return jsonify(msg=f'Data tahun ajaran {base.model.th_ajaran} telah ditambahkan.'), HTTP_201_CREATED
        
    @master.route('/ajaran/get-all', endpoint='ajaran-all', methods=['GET'])
    def get_all():
        base = BaseModel(TahunAjaranModel)
        model = base.get_all()
        
        data = []
        for ajaran in model:
            data.append({
                'id' : ajaran.id,
                'th_ajaran' : ajaran.th_ajaran,
                'status' : True if ajaran.is_active == "1" else False 
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
                               status= True if model.is_active == "1" else False)
            else:
                return jsonify(msg='Data tahun ajaran not found.'), HTTP_404_NOT_FOUND
                
        elif request.method == 'PUT':
            ajaran = request.json.get('ajaran')
            status = request.json.get('status')
            
            # class_check = base.get_one_or_none(th_ajaran=ajaran)
            # if class_check:
            #     return jsonify(msg=f'Data dengan {ajaran} sudah ada.')      
            # else:
            model.th_ajaran = ajaran
            model.is_active = status
            base.edit()            
            return jsonify(msg=f'Data tahun ajaran {model.th_ajaran} telah diperbaharui'), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
class Semester(object):
    @master.route('/semester/create', endpoint='semester', methods=['POST','GET'])
    def create():
        semester = request.json.get('semester')
        active = request.json.get('status')
        
        base = BaseModel(SemesterModel(semester, active))
        sms_check = base.get_one_or_none(semester=semester)
        if sms_check:
            return jsonify(msg='Data Class has been already exists.'), HTTP_409_CONFLICT
        else:
            base.create()        
            return jsonify(msg=f'Data Semester {base.model.semester} telah di tambahkan.' ), HTTP_201_CREATED
        
    @master.route('/semester/get-all', endpoint='semester-all', methods=['GET'])
    def get_all():
        base = BaseModel(SemesterModel)
        model = base.get_all()
        
        data = []
        for sms in model:
            data.append({
                'id' : sms.id,
                'semester' : sms.semester,
                'status' : True  if sms.is_active == "1" else False 
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
                               status=  True  if model.is_active == "1" else False )
            else:
                return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
                
        elif request.method == 'PUT':
            # semester = request.json.get('semester')
            active = request.json.get('status')
            
            # class_check = base.get_one_or_none(semester=semester)
            if not model:
                return jsonify(msg=f'Data dengan semester tidak ditemukan.'), HTTP_404_NOT_FOUND      
            else:
                # model.semester = semester
                model.is_active = active
                base.edit()            
                return jsonify(msg=f'Data Semester {model.semester} telah diperbaharui'), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
class Jam(object):
    @master.route('/jam/create', endpoint='jam', methods=['POST','GET'])
    def create():
        jam = request.json.get('jam')
        
        base = BaseModel(JamMengajarModel(jam=jam))
        jam_check = base.get_one_or_none(jam=jam)
        if jam_check:
            return jsonify(msg='Data has been already exists.'), HTTP_409_CONFLICT
        else:
            base.create()        
            return jsonify(jam=base.model.jam), HTTP_201_CREATED
        
    @master.route('/jam/get-all', endpoint='jam-all', methods=['GET'])
    def get_all():
        base = BaseModel(JamMengajarModel)
        model = base.get_all()
        
        data = []
        for jam in model:
            data.append({
                'id' : jam.id,
                'jam' : jam.jam
            })
            
        return jsonify({
            'data' : data
        }), HTTP_200_OK
        
    @master.route('/jam/get-one/<int:id>', endpoint='jam-single', methods=['GET', 'PUT', 'DELETE'])
    def get_one(id):
        base = BaseModel(JamMengajarModel)
        model = base.get_one_or_none(id=id)
        
        if request.method == 'GET':
            if model is not None:
                return jsonify(id=model.id, jam= model.jam)
            else:
                return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
                
        elif request.method == 'PUT':
            jam = request.json.get('jam')
            
            jam_check = base.get_one_or_none(jam=jam)
            if jam_check:
                return jsonify(msg=f'Data dengan {jam} sudah ada.')      
            else:
                model.jam = jam
                base.edit()            
                return jsonify(id=model.id, jam=model.jam), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
class WaliKelas(object):
    @master.route('/wali-kelas/create', endpoint='wali-kelas', methods=['POST','GET'])
    def create():
        guru_id = request.json.get('guru_id')
        kelas_id = request.json.get('kelas_id')
        
        base = BaseModel(WaliKelasModel(guru_id=guru_id, kelas_id=kelas_id))
        guru_check = base.get_one_or_none(guru_id=guru_id)
        kelas_check = base.get_one_or_none(kelas_id=kelas_id)
        
        if guru_check:
            return jsonify(msg='Data has been already exists.'), HTTP_409_CONFLICT
        
        elif guru_check and kelas_check:
            return jsonify(msg='Data has been already exists.'), HTTP_409_CONFLICT
        
        elif guru_check or kelas_check:
            return jsonify(msg='Data has been already exists.'), HTTP_409_CONFLICT
        
        else:
            base.create()        
            return jsonify(
                id=base.model.id,
                wali_kelas=base.model.guru.users.first_name,
                kelas = base.model.kelas.kelas
                           
                           ), HTTP_201_CREATED
        
    @master.route('/wali-kelas/get-all', endpoint='wali-kelas-all', methods=['GET'])
    def get_all():
        base = BaseModel(WaliKelasModel)
        model = base.get_all()
        
        data = []
        for wali in model:
            data.append({
                'id' : wali.id,
                'first_name' : wali.guru.users.first_name,
                'last_name' : wali.guru.users.last_name,
                'kelas' : wali.kelas.kelas
            })
            
        return jsonify(data=data), HTTP_200_OK
        
    @master.route('/wali-kelas/get-one/<int:id>', endpoint='wali-kelas-single', methods=['GET', 'PUT', 'DELETE'])
    def get_one(id):
        base = BaseModel(WaliKelasModel)
        model = base.get_one_or_none(id=id)
        
        if request.method == 'GET':
            if model is not None:
                return jsonify(id=model.id,
                               first_name=model.guru.users.first_name,
                               last_name=model.guru.users.last_name,
                               kelas=model.kelas.kelas
                               ), HTTP_200_OK
            else:
                return jsonify(msg='Data not found.'), HTTP_404_NOT_FOUND
                
        elif request.method == 'PUT':
            kelas_id = request.json.get('kelas_id')
            
            kelas_check = base.get_one_or_none(kelas_id=kelas_id)            
            if kelas_check:
                return jsonify(msg='Data has been already exists.'), HTTP_409_CONFLICT   
            else:
                model.kelas_id = kelas_id
                base.edit()            
                return jsonify(id=model.id,
                               jam=model.guru.users.first_name +' '+ model.guru.users.last_name,
                               kelas=model.kelas.kelas), HTTP_200_OK
        
        elif request.method == 'DELETE':
            base.delete(model)            
            return jsonify(msg='Data has been deleted.'), HTTP_204_NO_CONTENT
        
