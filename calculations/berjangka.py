import pandas as pd

mortality = pd.read_csv(
    'database/mortality.csv'
)

def asuransi_berjangka(age, n, i):

    v = 1 / (1+i)

    lx = mortality.loc[
        mortality['age'] == age,
        'lx'
    ].values[0]

    total = 0

    for k in range(n):

        dx = mortality.loc[
            mortality['age'] == age+k,
            'dx'
        ].values[0]

        total += (
            (v**(k+1))
            *
            (dx/lx)
        )

    return total