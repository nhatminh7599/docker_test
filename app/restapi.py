from app import dao
from app.init import myapp
from flask import jsonify, request


@myapp.route("/api/san-bay", methods=['get'])
def san_bay():
    data = dao.read_san_bay()
    return jsonify(
        message="success",
        data=data,
        status=200
    )


@myapp.route("/api/lich-chuyen-bay", methods=['get', 'post'])
def lich_chuyen_bay():
    diemdi = request.json['diemdi']
    diemden = request.json['diemden']
    ngaykhoihanh = request.json['ngaykhoihanh']
    loaive = request.json['loaive']
    data = dao.read_lich_chuyen_bay_form(diemdi, diemden, ngaykhoihanh, loaive)
    return jsonify(
        message="success",
        data=data,
        status=200
    )


@myapp.route("/api/them-lich-chuyen-bay", methods=['get', 'post'])
def them_lich_chuyen_bay():
    sanbaycatcanh = int(request.json['diaDiemKH'])
    sanbayhacanh = int(request.json['diaDiemDi'])
    ngaykhoihanh = request.json['ngaydi']
    thoigianbay = int(request.json['tgBay'])
    soluongghehang1 = int(request.json['slGheHang1'])
    soluongghehang2 = int(request.json['slGheHang2'])
    giavehang1 = int(request.json['giavehang1'])
    giavehang2 = int(request.json['giavehang2'])

    tgdung1 = int(request.json["tgDung1"]) if request.json["tgDung1"] else None
    tgdung2 = int(request.json["tgDung2"]) if request.json["tgDung2"] else None
    # import pdb
    # pdb.set_trace()
    if tgdung1:
        sbtrunggian1 = request.json["diemDung1"]
        if tgdung2:
            sbtrunggian2 = request.json["diemDung2"]
            data = dao.them_lich_chuyen_bay(sanbaycatcanh, sanbayhacanh, ngaykhoihanh, thoigianbay, soluongghehang1,
                                            soluongghehang2, giavehang1, giavehang2, sbtrunggian1, tgdung1,
                                            sbtrunggian2, tgdung2)
            return jsonify(
                message="success",
                data=data,
                status=200
            )
        else:
            data = dao.them_lich_chuyen_bay(sanbaycatcanh, sanbayhacanh, ngaykhoihanh, thoigianbay, soluongghehang1,
                                            soluongghehang2, giavehang1, giavehang2, sbtrunggian1, tgdung1)
            return jsonify(
                message="success",
                data=data,
                status=200
            )
    else:
        data = dao.them_lich_chuyen_bay(sanbaycatcanh, sanbayhacanh, ngaykhoihanh, thoigianbay, soluongghehang1,
                                        soluongghehang2, giavehang1, giavehang2)

        return jsonify(
            message="success",
            data=data,
            status=200
        )


@myapp.route("/api/read-lich-chuyen-bay-theo-ma-chuyen-ma-loai-ve", methods=['get', 'post'])
def read_lich_chuyen_bay_theo_ma_chuyen_ma_loai_ve():
    machuyenbay = request.json["machuyenbay"]
    maloaive = request.json["maloaive"]
    data = dao.read_lich_chuyen_bay_theo_ma_chuyen_ma_loai_ve(machuyenbay, maloaive)
    return jsonify(
        message="success",
        data=data,
        status=200
    )


@myapp.route("/api/lich-chuyen-bay-id", methods=['get', 'post'])
def lich_chuyen_bay_id():
    machuyen = request.json['machuyenbay']
    data = dao.read_lich_chuyen_bay_id(machuyen)
    return jsonify(
        message="success",
        data=data,
        status=200
    )


@myapp.route("/api/loai-ve")
def gia_ve():
    data = dao.read_loai_ve()
    return jsonify(
        message="success",
        data=data,
        status=200
    )


@myapp.route("/api/loai-ve/<int:ma_chuyen>")
def gia_ve_theo_chuyen(ma_chuyen):
    data = dao.read_loai_ve_theo_chuyen(ma_chuyen)
    return jsonify(
        message="success",
        data=data,
        status=200
    )


@myapp.route("/api/khach-hang", methods=['get', 'post'])
def khach_hang():
    keyword = request.json["kw"] if request.json["kw"] else None

    data = dao.tim_khach_hang(keyword=keyword)
    return jsonify(
        message="success",
        data=data,
        status=200
    )


@myapp.route("/api/them-ve", methods=['post', 'get'])
def them_ve():
    try:
        trang_thai = int(request.json['trang_thai'])
        gia = int(request.json['gia'])
        giam_gia = 0
        ma_loai_ve = int(request.json['ma_loai_ve'])
        ma_chuyen_bay = int(request.json['ma_chuyen_bay'])
        ten_khach_hang = request.json['ten_khach_hang']
        cmnd = int(request.json['cmnd'])
        sdt = request.json['sdt']
        email = request.json['email']
        gioi_tinh = request.json['gioi_tinh']

        ma_khach_hang = dao.them_khach_hang(ten_khach_hang=ten_khach_hang, cmnd=cmnd, sdt=sdt, email=email, gioi_tinh=gioi_tinh)
        if dao.them_ve(trang_thai=int(trang_thai), gia=gia, giam_gia=0, ma_loai_ve=ma_loai_ve,
                       ma_chuyen_bay=ma_chuyen_bay, ma_khach_hang=ma_khach_hang):
            return jsonify(
                message="success",
                status=200
            )
        return jsonify(
            message="Them ve that bai",
            status=400
        )
    except Exception:
        return jsonify(
            message="fail",
            status=400
        )


@myapp.route("/api/del-ve", methods=['delete'])
def xoa_ve():
    ma_ve = request.json["mave"]
    ma_khach_hang = request.json["makhachhang"]
    if dao.xoa_ve(ma_ve, ma_khach_hang):
        return jsonify(
            message="success",
            status=200
        )
    return jsonify(
        message="fail",
        status=400
    )


@myapp.route("/api/sua-trang-thai-ve", methods=['post', 'get'])
def sua_trang_thai_ve():
    ma_ve = request.json['mave']
    if dao.sua_trang_thai_ve(ma_ve):
        return jsonify(
            message="success",
            status=200
        )
    return jsonify(
        message="fail",
        status=400
    )


@myapp.route("/api/sua-khach-hang", methods=['post', 'get'])
def sua_khach_hang():
    ma_khach_hang = request.json['makhachhang']
    ten_khach_hang = request.json['tenkhachhang']
    cmnd = request.json['cmnd']
    sdt = request.json['sdt']
    email = request.json['email']
    if dao.sua_khach_hang(ma_khach_hang, ten_khach_hang, cmnd, sdt, email):
        return jsonify(
            message="success",
            status=200
        )
    return jsonify(
        message="fail",
        status=400
    )


@myapp.route("/api/chi-tiet-ve", methods=['post', 'get'])
def chi_tiet_ve():
    ma_khach_hang = request.json['makhachhang']
    ma_ve = request.json['mave']
    if dao.tim_khach_hang_id(ma_khach_hang, ma_ve):
        return jsonify(
            message="success",
            data=dao.tim_khach_hang_id(ma_khach_hang, ma_ve),
            status=200
        )
    return jsonify(
        message="fail",
        status=400
    )


@myapp.route("/api/doanh-thu-theo-thang", methods=['post', 'get'])
def doanh_thu_theo_thang():
    date = request.json['date']
    if dao.doanh_thu_theo_thang(date):
        return jsonify(
            message="success",
            data=dao.doanh_thu_theo_thang(date),
            status=200
        )
    return jsonify(
        message="fail",
        status=400
    )


@myapp.route("/api/doanh-thu-theo-nam", methods=['post', 'get'])
def doanh_thu_theo_nam():
    date = request.args['date']
    if dao.doanh_thu_theo_nam(date):
        return jsonify(
            message="success",
            data=dao.doanh_thu_theo_nam(date),
            status=200
        )
    return jsonify(
        message="fail",
        status=400
    )

