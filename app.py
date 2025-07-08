from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model database
class Obat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    waktu = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, default=False)

# ✅ 1. Halaman Beranda
@app.route('/')
def index():
    daftar_obat = Obat.query.all()
    return render_template('index.html', daftar_obat=daftar_obat)

# ✅ 2. Halaman Tambah Obat
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        waktu = request.form['waktu']
        obat_baru = Obat(nama=nama, waktu=waktu)
        db.session.add(obat_baru)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('tambah.html')

# ✅ 3. Halaman Riwayat (yang sudah diminum)
@app.route('/riwayat')
def riwayat():
    daftar_obat = Obat.query.filter_by(status=True).all()
    return render_template('riwayat.html', daftar_obat=daftar_obat)

# ✅ 4. Halaman Tentang
@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

# ✅ 5. Halaman Kontak
@app.route('/kontak')
def kontak():
    return render_template('kontak.html')

# ✅ Update status minum
@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    obat = Obat.query.get(id)
    if obat:
        obat.status = not obat.status
        db.session.commit()
        return jsonify({'status': obat.status})
    return jsonify({'error': 'Obat tidak ditemukan'}), 404

# ✅ Hapus obat
@app.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    obat = Obat.query.get(id)
    if obat:
        db.session.delete(obat)
        db.session.commit()
    return redirect(url_for('index'))

# ✅ Jalankan Flask
if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
