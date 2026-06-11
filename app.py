from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# ==================================================
# BACA TABEL MORTALITAS
# ==================================================

df = pd.read_csv("TMI_IV_2019.csv", sep=";")

# qx rata-rata laki-laki dan perempuan
df["qx"] = (
    df["laki_laki"].astype(float)
    + df["perempuan"].astype(float)
) / 2


# ==================================================
# MEMBENTUK px, lx, dx
# ==================================================

def buat_tabel(df):

    tabel = pd.DataFrame()

    tabel["usia"] = df["usia"]

    # qx asli dari CSV
    tabel["qx_laki_laki"] = df["laki_laki"]
    tabel["qx_perempuan"] = df["perempuan"]

    # qx rata-rata
    tabel["qx"] = df["qx"]

    # px = 1 - qx
    tabel["px"] = 1 - tabel["qx"]

    # radix
    l0 = 100000

    lx = [l0]

     # lx+1 = lx * px
    for i in range(len(tabel) - 1):

        lx.append(
            lx[i] *
            tabel.loc[i, "px"]
        )

    tabel["lx"] = lx

    # dx = lx - lx+1
    tabel["dx"] = (
        tabel["lx"]
        - tabel["lx"].shift(-1)
    )

    # usia terakhir
    tabel.loc[
        tabel.index[-1],
        "dx"
    ] = tabel.loc[
        tabel.index[-1],
        "lx"
    ]

    return tabel

tmi = buat_tabel(df)


# ==================================================
# PREMI BERJANGKA
# ==================================================

def premi_berjangka(
    usia,
    tenor,
    bunga,
    manfaat
):

    v = 1 / (1 + bunga)

    lx_awal = tmi.loc[
        tmi["usia"] == usia,
        "lx"
    ].iloc[0]

    Axn = 0

    for k in range(tenor):

        baris = tmi.loc[
            tmi["usia"] == usia + k
        ]

        if len(baris) == 0:
            break

        dx = baris["dx"].iloc[0]

        Axn += (
            (v ** (k + 1))
            * dx
            / lx_awal
        )

    premi = manfaat * Axn

    return {
        "Axn": round(Axn, 8),
        "premi": round(premi, 2)
    }

# ==================================================
# PREMI SEUMUR HIDUP
# ==================================================

def premi_seumur_hidup(
    usia,
    bunga,
    manfaat
):

    v = 1 / (1 + bunga)

    lx_awal = tmi.loc[
        tmi["usia"] == usia,
        "lx"
    ].values[0]

    Ax = 0

    usia_max = int(
        tmi["usia"].max()
    )

    for k in range(
        usia_max - usia + 1
    ):

        baris = tmi.loc[
            tmi["usia"] == usia + k
        ]

        if len(baris) == 0:
            break

        lx = baris["lx"].values[0]

        qx = baris["qx"].values[0]

        kpx = lx / lx_awal

        Ax += (
            (v ** (k + 1))
            * kpx
            * qx
        )

    return round(
        manfaat * Ax,
        2
    )


# ==================================================
# PREMI DWIGUNA
# ==================================================

# ==================================================
# PREMI DWIGUNA
# ==================================================

def premi_dwiguna(
    usia,
    tenor,
    bunga,
    manfaat
):

    v = 1 / (1 + bunga)

    data_awal = tmi.loc[
        tmi["usia"] == usia
    ]

    if data_awal.empty:
        return None

    lx_awal = data_awal["lx"].iloc[0]

    A_term = 0

    for k in range(tenor):

        baris = tmi.loc[
            tmi["usia"] == usia + k
        ]

        if baris.empty:
            break

        dx = baris["dx"].iloc[0]

        A_term += (
            (v ** (k + 1))
            * dx
            / lx_awal
        )

    baris_n = tmi.loc[
        tmi["usia"] == usia + tenor
    ]

    if not baris_n.empty:

        lx_n = baris_n["lx"].iloc[0]

        npx = lx_n / lx_awal

    else:

        npx = 0

    pure_endowment = (
        v ** tenor
    ) * npx

    A_endowment = (
        A_term
        + pure_endowment
    )

    premi = manfaat * A_endowment

    return round(
        premi,
        2
    )


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():
    return render_template("index.html")


# ==================================================
# BERJANGKA
# ==================================================

@app.route("/berjangka", methods=["GET", "POST"])
def berjangka():

    hasil = None

    if request.method == "POST":

        usia = int(
            request.form["usia"]
        )

        bunga = float(
            request.form["bunga"]
        ) / 100

        tenor = int(
            request.form["tenor"]
        )

        manfaat = float(
            request.form["manfaat"]
        )

        hasil = premi_berjangka(
            usia,
            tenor,
            bunga,
            manfaat
        )

    return render_template(
        "berjangka.html",
        hasil=hasil
    )


# ==================================================
# SEUMUR HIDUP
# ==================================================

@app.route("/seumur_hidup", methods=["GET", "POST"])
def seumur_hidup():

    hasil = None

    if request.method == "POST":

        usia = int(
            request.form["usia"]
        )

        bunga = float(
            request.form["bunga"]
        ) / 100

        manfaat = float(
            request.form["manfaat"]
        )

        hasil = premi_seumur_hidup(
            usia,
            bunga,
            manfaat
        )

    return render_template(
        "seumur_hidup.html",
        hasil=hasil
    )


# ==================================================
# DWIGUNA
# ==================================================

@app.route("/dwiguna", methods=["GET", "POST"])
def dwiguna():

    hasil = None

    if request.method == "POST":

        usia = int(
            request.form["usia"]
        )

        bunga = float(
            request.form["bunga"]
        ) / 100

        tenor = int(
            request.form["tenor"]
        )

        manfaat = float(
            request.form["manfaat"]
        )

        hasil = premi_dwiguna(
            usia,
            tenor,
            bunga,
            manfaat
        )

    return render_template(
        "dwiguna.html",
        hasil=hasil
    )


# ==================================================
# MORTALITAS
# ==================================================
@app.route("/mortalitas")
def mortalitas():

    data = tmi.to_dict(
        orient="records"
    )

    return render_template(
        "mortalitas.html",
        data=data
    )

# ==================================================
# RUN APP
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)