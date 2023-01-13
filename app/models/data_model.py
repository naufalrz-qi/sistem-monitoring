from app.extensions import db
import sqlalchemy as sa
import sqlalchemy.orm as sql
from sqlalchemy.orm import backref
from app.models.master_model import *


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
