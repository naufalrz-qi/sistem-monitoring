import sqlalchemy as sa
from ..extensions import db
import sqlalchemy.orm as rs
from sqlalchemy.orm import backref
from .user_details_model import *


class KelasModel(db.Model):
    __tablename__ = "master_kelas"
    id = sa.Column(sa.Integer, primary_key=True)
    kelas = sa.Column(sa.String(16), nullable=False)
    jml_laki = sa.Column(sa.Integer, nullable=True)
    jml_perempuan = sa.Column(sa.Integer, nullable=True)
    jml_seluruh = sa.Column(sa.Integer, nullable=True)

    def __init__(self, kelas) -> None:
        self.kelas = kelas
        self.jml_laki = 0
        self.jml_perempuan = 0
        self.jml_seluruh = 0

    def __repr__(self) -> str:
        return self.kelas


class MapelModel(db.Model):
    __tablename__ = "master_mapel"
    id = sa.Column(sa.Integer, primary_key=True)
    mapel = sa.Column(sa.String(32), nullable=False)

    def __repr__(self) -> str:
        return self.mapel


class HariModel(db.Model):
    __tablename__ = "master_hari"
    id = sa.Column(sa.Integer, primary_key=True)
    hari = sa.Column(sa.String(32), nullable=False)

    def __init__(self, hari):
        self.hari = hari

    def __repr__(self) -> str:
        return self.hari


class TahunAjaranModel(db.Model):
    __tablename__ = "master_tahun_ajaran"
    id = sa.Column(sa.Integer, primary_key=True)
    th_ajaran = sa.Column(sa.String(32), nullable=False)
    is_active = sa.Column(sa.String(1), nullable=False)

    def __init__(self, ajaran, status=None):
        self.th_ajaran = ajaran
        self.is_active = status

    def __repr__(self) -> str:
        return self.th_ajaran


class SemesterModel(db.Model):
    __tablename__ = "master_semester"
    id = sa.Column(sa.Integer, primary_key=True)
    semester = sa.Column(sa.String(32), nullable=False)
    is_active = sa.Column(sa.String(1), nullable=False)

    def __init__(self, semester=None, active=None) -> None:
        self.semester = semester
        self.is_active = active

    def __repr__(self) -> str:
        return self.semester


class WaliKelasModel(db.Model):
    __tablename__ = "master_wali_kelas"
    id = sa.Column(sa.Integer, primary_key=True)
    guru_id = sa.Column(sa.Integer, sa.ForeignKey("detail_guru.user_id"))
    guru = rs.relationship("GuruModel", backref="wali_kelas")
    kelas_id = sa.Column(sa.Integer, sa.ForeignKey("master_kelas.id"))
    kelas = rs.relationship("KelasModel", backref="kelas_didik")

    def __repr__(self) -> str:
        return "{}".format(self.kelas)


class JamMengajarModel(db.Model):
    __tablename__ = "master_jam_mengajar"
    id = sa.Column(sa.Integer, primary_key=True)
    jam = sa.Column(sa.String(32), nullable=False)

    def __init__(self, jam=None) -> None:
        self.jam = jam

    def __repr__(self) -> str:
        return "jam : {}".format(self.jam)


class MengajarModel(db.Model):
    __tablename__ = "master_jadwal_mengajar"
    id = sa.Column(sa.Integer, primary_key=True)
    kode_mengajar = sa.Column(sa.String(32), nullable=False)
    guru_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("detail_guru.user_id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    guru = rs.relationship("GuruModel",backref=backref("guru_mapels", cascade="all, delete-orphan"))
    mapel_id = sa.Column(sa.Integer, sa.ForeignKey('master_mapel.id', ondelete='CASCADE', onupdate='CASCADE'))
    mapel = rs.relationship('MapelModel', backref=backref('mengajar_mapel', cascade='all, delete-orphan'))
    jam_ke = sa.Column(sa.String(6), nullable=True)
    hari_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("master_hari.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    hari = rs.relationship('HariModel', backref=backref('hari_mengajar'))
    
    jam_mulai = sa.Column(sa.String(12))
    jam_selesai = sa.Column(sa.String(12))
    kelas_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("master_kelas.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    kelas = rs.relationship('KelasModel', backref=backref('kelas_mengajar'))
    semester_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("master_semester.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    semester = rs.relationship('SemesterModel', backref=backref('semester_aktif'))
    tahun_ajaran_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("master_tahun_ajaran.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    tahun_ajaran = rs.relationship('TahunAjaranModel', backref=backref('tahun_ajaran_aktif'))

    def __init__(
        self,
        kodeMengajar=None,
        guruId=None,
        hariId=None,
        jamMulai=None,
        jamSelesai=None,
        kelasId=None,
        semesterId=None,
        tahunAjaranId=None
        
    ) -> None:
        self.kode_mengajar = kodeMengajar
        self.guru_id = guruId
        self.hari_id = hariId
        self.jam_mulai = jamMulai
        self.jam_selesai = jamSelesai
        self.kelas_id = kelasId
        self.semester_id = semesterId
        self.tahun_ajaran_id = tahunAjaranId

    def __repr__(self) -> str:
        return 'Kode Mengajar : {}, Nama Guru : {}, Mapel : {}'.format(self.kode_mengajar, self.guru.first_name, self)


class KepsekModel(db.Model):
    __tablename__ = "master_kepsek"
    id = sa.Column(sa.Integer, primary_key=True)
    guru_id = sa.Column(
        sa.Integer, sa.ForeignKey("detail_guru.user_id", onupdate="CASCADE")
    )
    guru = rs.relationship("GuruModel", backref="kepsek")
    status = sa.Column(sa.String(2))

    def __init__(self, guruId=None):
        self.guru_id = guruId
        self.status = 0

    def __repr__(self) -> str:
        return f"Kepsek : {self.guru.first_name}"


class GuruBKModel(db.Model):
    __tablename__ = "master_guru_bk"
    id = sa.Column(sa.Integer, primary_key=True)
    guru_id = sa.Column(
        sa.Integer, sa.ForeignKey("detail_guru.user_id", onupdate="CASCADE")
    )
    guru = rs.relationship("GuruModel", backref="guru_bk")

    def __init__(self, guruId=None):
        self.guru_id = guruId

    def __repr__(self) -> str:
        return "Nama Guru : {}".format(self.guru.first_name)
