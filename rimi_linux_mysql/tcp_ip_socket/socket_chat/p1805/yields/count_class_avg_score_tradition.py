data = {
    'A班': [90, 89, 60, 68],
    'B班': [90, 13, 43, 13, 53],
    'C班': [12, 86, 43, 34, 89, 98, 89]
}
#输入每个每个人的成绩,输出他们的平均成绩
# res = {
#     'A班': 70,
#     'B班': 98,
#     'C班': 20
# }

# yield from
res = {}

for k,v in data.items():
    scores = 0
    for score in v:
        scores += score
    avg = scores/len(v)
    res[k] = avg

print(res)



