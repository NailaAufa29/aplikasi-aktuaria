from flask import Flask, render_template, request

app = Flask(__name__)

# =========================
# HOME
# =========================
@app.route('/')
def home():
    return render_template('index.html')


# =========================
# BERJANGKA
# =========================
@app.route('/berjangka', methods=['GET', 'POST'])
def berjangka():
    hasil = None

    if request.method == 'POST':
        usia = int(request.form['usia'])
        bunga = float(request.form['bunga'])
        tenor = int(request.form['tenor'])
        manfaat = float(request.form['manfaat'])

        hasil = (manfaat * 0.01 * tenor) / (1 + bunga)
        hasil = round(hasil, 2)

    return render_template('berjangka.html', hasil=hasil)


# =========================
# SEUMUR HIDUP
# =========================
@app.route('/seumur_hidup', methods=['GET', 'POST'])
def seumur_hidup():
    hasil = None

    if request.method == 'POST':
        usia = int(request.form['usia'])
        bunga = float(request.form['bunga'])
        manfaat = float(request.form['manfaat'])

        # model sederhana
        hasil = (manfaat * 0.02 * (100 - usia)) / (1 + bunga)
        hasil = round(hasil, 2)

    return render_template('seumur_hidup.html', hasil=hasil)


# =========================
# DWIGUNA
# =========================
@app.route('/dwiguna', methods=['GET', 'POST'])
def dwiguna():
    hasil = None

    if request.method == 'POST':
        usia = int(request.form['usia'])
        bunga = float(request.form['bunga'])
        tenor = int(request.form['tenor'])
        manfaat = float(request.form['manfaat'])

        hasil = (manfaat * tenor * 0.015) / (1 + bunga)
        hasil = round(hasil, 2)

    return render_template('dwiguna.html', hasil=hasil)


# =========================
# HALAMAN LAIN (sementara)
# =========================
@app.route('/mortalitas')
def mortalitas():
    return render_template('mortalitas.html')




if __name__ == '__main__':
    app.run(debug=True)