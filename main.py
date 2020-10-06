from app import dao, restapi, decorator
from app.init import myapp, login
from app.admin import *
from flask import render_template, redirect, request, session, jsonify
from flask_login import login_user
import hashlib


@myapp.route("/")
@decorator.login_required_user
def index():
    sanbay = dao.read_san_bay()
    loaive = dao.read_loai_ve()
    return render_template("nhanvien/index.html", sanbay=sanbay, loaive=loaive)


@login.user_loader
def user_loader(user_id):
    return TaiKhoan.query.get(user_id)


@myapp.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        tentaikhoan = request.form.get("tentaikhoan")
        matkhau = request.form.get("matkhau")
        matkhau = str(hashlib.md5(matkhau.strip().encode("utf-8")).hexdigest())
        taikhoan = TaiKhoan.query.filter(TaiKhoan.tentaikhoan == tentaikhoan.strip(),
                                         TaiKhoan.matkhau == matkhau, TaiKhoan.maloai == 1).first()
        if taikhoan:
            login_user(user=taikhoan)
            session['err-login'] = ''
        else:
            err = "Truy cập thất bại"
            session['err-login'] = err
        return redirect('/admin')


@myapp.route("/ticket-list", methods=['get', 'post'])
@decorator.login_required_user
def ticket_list():
    diemdi = request.form.get("diemdi")
    diemden = request.form.get("diemden")
    madiemdi = request.form.get("madiemdi")
    madiemden = request.form.get("madiemden")
    ngaykhoihanh = request.form.get("ngaykhoihanh")
    maloaive = request.form.get("maloaive")
    # ngaykhoihanh = datetime.strptime(ngaykhoihanh, '%Y-%m-%d')
    # ngaykhoihanh.replace(day=15)
    return render_template("nhanvien/ticket-list.html", diemdi=diemdi, diemden=diemden, madiemdi=madiemdi,
                           madiemden=madiemden, ngaykhoihanh=ngaykhoihanh, maloaive=maloaive)


@myapp.route("/ticket-detail", methods=['get', 'post'])
@decorator.login_required_user
def ticket_detail():
    machuyenbay = request.args.get("machuyenbay")
    maloaive = request.args.get("maloaive")
    giave = request.args.get("giave")
    data = dao.read_lich_chuyen_bay_theo_ma_chuyen_ma_loai_ve(machuyenbay, maloaive)
    return render_template("nhanvien/ticket-detail.html", data=data, giave=giave)


@myapp.route("/ticket-fill-form", methods=['get', 'post'])
@decorator.login_required_user
def ticket_fill_form():
    machuyenbay = request.args.get("machuyenbay")
    maloaive = request.args.get("maloaive")
    giave = request.args.get("giave")
    data = dao.read_lich_chuyen_bay_theo_ma_chuyen_ma_loai_ve(machuyenbay, maloaive)
    return render_template("nhanvien/ticket-fill-form.html", data=data, giave=giave)

@myapp.route("/ticket-info", methods=['get', 'post'])
@decorator.login_required_user
def ticket_info():
    giave = request.form.get("giave")
    data = jsonify(request.form)
    data = data.json
    ve = dao.read_lich_chuyen_bay_theo_ma_chuyen_ma_loai_ve(data['machuyenbay'], data['maloaive'])
    return render_template("nhanvien/ticket-info.html", data=data, ve=ve, giave=giave)

@myapp.route("/ticket-manager", methods=['get', 'post'])
@decorator.login_required_user
def ticket_manager():
    kw = ''
    page_num = 1
    if request.method == 'POST':
        kw = request.form["kw"] if request.form.get("kw") else ''
        page_num = int(request.form["page_num"]) if request.form.get("page_num") else 1
    if request.method == 'GET':
        kw = request.args["kw"] if request.args.get("kw") else ''
        page_num = int(request.args["page_num"]) if request.args.get("page_num") else 1

    if kw != '':
        ve = dao.tim_khach_hang(keyword=kw, page=page_num)
    else:
        ve = ''
    return render_template("nhanvien/ticket-manager.html", ve=ve, kw=kw, page_num=page_num)

@myapp.route("/flight-manager", methods=['get', 'post'])
@decorator.login_required_user
def flight_manager():
    sanbay = dao.read_san_bay()
    qd = dao.doc_quy_dinh_thoi_gian_bay()
    if request.method == 'POST':
        diemdi = request.form["diemDi"] if request.form.get("diemDi") else None
        diemden = request.form["diemDen"] if request.form.get("diemDen") else None
        if diemdi != None and diemden != None:
            lich = dao.read_lich_chuyen_bay_san_bay(diemdi, diemden)
        else:
            lich = dao.read_lich_chuyen_bay()
    else:
        lich = dao.read_lich_chuyen_bay()
    return render_template("nhanvien/flight-manager.html", sanbay=sanbay, lich=lich, qd=qd)

@myapp.route("/login", methods=['get', 'post'])
def login():
    err = False
    if request.method == 'POST':
        tentaikhoan = request.form.get("tentaikhoan")
        matkhau = request.form.get("matkhau")
        matkhau = str(hashlib.md5(matkhau.strip().encode("utf-8")).hexdigest())
        taikhoan = TaiKhoan.query.filter(TaiKhoan.tentaikhoan == tentaikhoan.strip(), TaiKhoan.matkhau == matkhau).first()
        if taikhoan:
            login_user(user=taikhoan)
            return redirect('/')
        err = True
    return render_template("nhanvien/login.html", err=err)


@myapp.route("/logout")
def logout():
    logout_user()
    return redirect('/login')


@myapp.route("/report", methods=['get', 'post'])
def report():
    doanhthutheonam = []
    doanhthutheothang = []
    if request.method == 'POST':
        date = request.form.get('date')
        date += ' 00:00:00'
        doanhthutheonam = dao.doanh_thu_theo_nam(date)
        doanhthutheothang = dao.doanh_thu_theo_thang(date)
    return render_template("nhanvien/report.html", doanhthutheonam=doanhthutheonam, doanhthutheothang=doanhthutheothang)


if __name__ == "__main__":
    myapp.run(debug=True)