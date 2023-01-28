from app.extensions import db
import sqlalchemy as sa
import sqlalchemy.orm as sql
from sqlalchemy.orm import backref
from app.models.master_model import *
from datetime import datetime


class AbsensiModel(db.Model):
    __tablename__ = "data_absensi"
    id = sa.Column(sa.Integer, primary_key=True)
    mengajar_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            "master_jadwal_mengajar.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    mengajar = sql.relationship(
        "MengajarModel", backref=backref("mengajar_guru", cascade="all, delete-orphan")
    )
    siswa_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("detail_siswa.user_id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    siswa = sql.relationship("SiswaModel", backref="data_siswa")
    tgl_absen = sa.Column(sa.Date)
    ket = sa.Column(sa.String(16), nullable=True)
    # pertemuan_ke = sa.Column(sa.String(2), nullable=True)

    def __init__(self, mengajar_id=None, siswa_id=None, tgl_absen=None, ket=None):
        self.mengajar_id = mengajar_id
        self.siswa_id = siswa_id
        self.tgl_absen = tgl_absen
        self.ket = ket
        # self.pertemuan_ke = pertemuan

    def __repr__(self):
        return "{}".format(self.ket)


class PelanggaranModel(db.Model):
    __tablename__ = "data_pelanggaran"
    id = sa.Column(sa.Integer, primary_key=True)
    siswa_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("detail_siswa.user_id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    siswa = sql.relationship("SiswaModel", backref="siswa_melanggar")
    jenis_pelanggaran_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            "master_jenis_pelanggaran.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    jenis_pelanggaran = sql.relationship(
        "JenisPelanggaranModel", backref="jenis_pelanggaran"
    )
    pelapor = sa.Column(sa.String(128), nullable=False)
    note = sa.Column(sa.Text(), nullable=True)
    tgl_report = sa.Column(sa.Date, nullable=False)

    def __init__(self, siswaId: int, jenisPelanggaranId: int, pelapor: str, note: str):
        self.siswa_id = siswaId
        self.jenis_pelanggaran_id = jenisPelanggaranId
        self.pelapor = pelapor
        self.note = note
        self.tgl_report = datetime.date(datetime.today())

    def __repr__(self):
        return self.pelapor
