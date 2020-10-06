
from datetime import datetime

from app.init import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Date, DECIMAL, Time, Text, Enum
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect, url_for, request, render_template


class AdminView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.maloai == 1


class SanBay (db.Model):
    __table_args__ = {'extend_existing': True}
    masanbay = Column(Integer, primary_key=True, autoincrement=True)
    tensanbay = Column(String(50), nullable=False)
    diadiem = Column(String(50), nullable=False)
    sanbaycatcanh = relationship('LichChuyenBay', backref="sanbaycatcanh", lazy=True, foreign_keys='LichChuyenBay.masanbaycatcanh')
    sanbayhacanh = relationship('LichChuyenBay', backref="sanbayhacanh", lazy=True, foreign_keys='LichChuyenBay.masanbayhacanh')
    sanbaytrunggian = relationship('SanBayTrungGian', backref='sanbaytrunggian', lazy=True)

    def __str__(self):
        return self.tensanbay


class NguoiDung (db.Model):
    __table_args__ = {'extend_existing': True}
    manguoidung = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    cmnd = Column(Integer, nullable=False)
    sdt = Column(String(10), nullable=False)
    email = Column(String(50), nullable=True)
    diachi = Column(String(50), nullable=False)
    gioitinh = Column(Boolean, default=True)
    taikhoan = relationship('TaiKhoan', backref='nguoidung', lazy=True)
    quydinh = relationship('QuyDinh', backref='nguoidung', lazy=True)

    def __str__(self):
        return self.ten


class QuyDinh (db.Model):
    __table_args__ = {'extend_existing': True}
    maquydinh = Column(Integer, primary_key=True, autoincrement=True)
    tenquydinh = Column(String(50), nullable=False)
    noidung = Column(Text, nullable=False)
    manguoidung = Column(Integer, ForeignKey(NguoiDung.manguoidung), nullable=False)


class KhachHang (db.Model):
    __table_args__ = {'extend_existing': True}
    makhachhang = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    cmnd = Column(Integer, nullable=False)
    sdt = Column(String(10), nullable=False)
    email = Column(String(50), nullable=True)
    gioitinh = Column(String(3), nullable=False)
    vemaybay = relationship('VeMayBay', backref="khachhang", lazy=True)

    def __str__(self):
        return self.ten


class LichChuyenBay(db.Model):
    __table_args__ = {'extend_existing': True}
    machuyenbay = Column(Integer, primary_key=True, autoincrement=True)
    masanbaycatcanh = Column(Integer, ForeignKey(SanBay.masanbay), nullable=False)
    masanbayhacanh = Column(Integer, ForeignKey(SanBay.masanbay), nullable=False)
    ngaykhoihanh = Column(DateTime, nullable=False)
    thoigianbay = Column(Integer, default=30)
    soluongghehang1 = Column(Integer, nullable=False)
    soluongghehang2 = Column(Integer, nullable=False)
    sanbaytrunggian = relationship('SanBayTrungGian', backref='lichchuyenbay', lazy=True)
    giave = relationship('GiaVe', backref='lichchuyenbay', lazy=True)
    vemaybay = relationship('VeMayBay', backref='lichchuyenbay', lazy=True)

    def __str__(self):
        return self.sanbaycatcanh.diadiem + " - " + self.sanbayhacanh.diadiem


class SanBayTrungGian (db.Model):
    __table_args__ = {'extend_existing': True}
    masanbay = Column(Integer, ForeignKey(SanBay.masanbay), primary_key=True)
    machuyenbay = Column(Integer, ForeignKey(LichChuyenBay.machuyenbay), primary_key=True)
    thoigiandung = Column(Integer, default=10)


class LoaiVe (db.Model):
    __table_args__ = {'extend_existing': True}
    maloaive = Column(Integer, primary_key=True, autoincrement=True)
    tenloaive = Column(String(20), nullable=False)
    giave = relationship('GiaVe', backref='loaive', lazy=True)
    vemaybay = relationship('VeMayBay', backref='loaive', lazy=True)

    def __str__(self):
        return self.tenloaive


class GiaVe (db.Model):
    __table_args__ = {'extend_existing': True}
    machuyenbay = Column(Integer, ForeignKey(LichChuyenBay.machuyenbay), primary_key=True)
    maloaive = Column(Integer, ForeignKey(LoaiVe.maloaive), primary_key=True)
    giave = Column(DECIMAL(11, 2), nullable=False)
    soghetrong = Column(Integer, nullable=False)
    soghedat = Column(Integer, nullable=False)


class TrangThaiVe (db.Model):
    __table_args__ = {'extend_existing': True}
    matrangthai = Column(Integer, primary_key=True, autoincrement=True)
    tentrangthao = Column(String(20), nullable=False)
    vemaybay = relationship('VeMayBay', backref="trangthaive", lazy=True)


class VeMayBay (db.Model):
    __table_args__ = {'extend_existing': True}
    mave = Column(Integer, primary_key=True, autoincrement=True)
    ngaykhoitao = Column(DateTime, default=datetime.utcnow())
    trangthai = Column(Integer, ForeignKey(TrangThaiVe.matrangthai), nullable=False)
    gia = Column(DECIMAL(11, 2), nullable=False)
    giamgia = Column(Float, default=0)
    maloaive = Column(Integer, ForeignKey(LoaiVe.maloaive), nullable=False)
    machuyenbay = Column(Integer, ForeignKey(LichChuyenBay.machuyenbay), nullable=False)
    makhachhang = Column(Integer, ForeignKey(KhachHang.makhachhang), nullable=False)


class LoaiTaiKhoan(db.Model):
    __table_args__ = {'extend_existing': True}
    maloai = Column(Integer, primary_key=True, autoincrement=True)
    tenloai = Column(String(20), nullable=False)
    taikhoan = relationship('TaiKhoan', backref='loaitaikhoan', lazy=True)


class TaiKhoan (db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    tentaikhoan = Column(String(20), nullable=False)
    matkhau = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    maloai = Column(Integer, ForeignKey(LoaiTaiKhoan.maloai), default=2)
    manguoidung = Column(Integer, ForeignKey(NguoiDung.manguoidung), nullable=False)

    def __str__(self):
        return self.tentaikhoan




# class ThemLichBay(BaseView):
#     @expose("/")
#     def index(self):
#         sanbay = dao.san_bay_read_all()
#         maybay = dao.may_bay_read_all()
#         chuyenbay = dao.chuyen_bay_read_all()
#         return self.render("admin/quan-ly-lich-bay.html", sanbay=sanbay, maybay=maybay, chuyenbay=chuyenbay)
#
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.loaitaikhoan == LoaiTaiKhoan.ADMIN


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


@expose('/')
def index(self):
    if not current_user.is_authenticated:
        return render_template('admin/page-not-found.html')
    if current_user.maloai != 1:
        logout_user()
        return render_template('admin/page-not-found.html')
    return self.render('admin/index.html')


if __name__ == "__main__":
    db.create_all()