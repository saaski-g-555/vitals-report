readings = [
    ("P001", 118, 76), ("P002", 152, 96), ("P003", None, None),
    ("P004", 126, 84), ("P005", 141, 92), ("P006", 132, 88),
]

def classify(systolic, diastolic):
    if systolic is None or diastolic is None:
        return "測定漏れ"
    if systolic >= 140 or diastolic >= 90:
        return "高血圧疑い"
    return "正常"

for pid, s, d in readings:
    print(pid, classify(s, d))