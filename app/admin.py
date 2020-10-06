from app.init import admin
from app.models import *

admin.add_view(AdminView(SanBay, db.session))
admin.add_view(AdminView(NguoiDung, db.session))
admin.add_view(AdminView(LichChuyenBay, db.session))
admin.add_view(AdminView(LoaiVe, db.session))
admin.add_view(AdminView(VeMayBay, db.session))
admin.add_view(AdminView(TrangThaiVe, db.session))
admin.add_view(AdminView(SanBayTrungGian, db.session))
admin.add_view(AdminView(GiaVe, db.session))
admin.add_view(AdminView(TaiKhoan, db.session))
admin.add_view(AdminView(LoaiTaiKhoan, db.session))
admin.add_view(AdminView(QuyDinh, db.session))
admin.add_view(AdminView(KhachHang, db.session))
admin.add_view(LogoutView(name="Log out"))