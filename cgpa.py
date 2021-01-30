import sys
import pandas as pd


def get_mark(x):
    return (float(x.replace(',', '.').split()[1][1:-1])
            if any(s.isdigit() for s in x) else 0.0)


def us_mark(number):
    if 9 <= number <= 10:
        return 'A'
    elif 7 <= number < 9:
        return 'B+'
    elif 5 <= number < 7:
        return 'B-'
    else:
        return 'F'


def map_us_mark(mark):
    return {
        'A': 4.0,
        'B+': 3.3,
        'B-': 2.7,
        'F': 0.0
    }[mark]


if len(sys.argv) <= 1:
    raise AttributeError("CSV filename must be provided")

fn = sys.argv[1]
df = pd.read_csv(fn)
df['Calificación'] = df['Calificación'].apply(lambda x: float(
    x.replace(',', '.').split()[1][1:-1]) if any(s.isdigit() for s in x) else 0.0)
print(df)
print(df['Calificación'])
