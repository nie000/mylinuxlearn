# def compute_num(max_price,goods_list,result=None):
#     sum_result = 0
#     if result is None:
#         result=[]
#     else:
#         for obj in result:
#             sum_result+=obj[0]
#     for index,obj in enumerate(goods_list):
#         if max_price>sum_result+obj[0]:
#             result.append(obj)
#             goods_list.remove(obj)
#             if goods_list:
#                 return compute_num(max_price,goods_list,result)
#         return result
# print(compute_num(1500,[(300,2,0),(200,3,0),(400,3,0),(400,3,0),(800,3,0)]))

def pack1(w, v, c):
    #它是先得到第一行的值，存到dp中，然后再直接用dp相当于就是上一行的值，所以下面必须用逆序
    #否则dp[j-w[i-1]]可能会用到你本行的值，从大到小就不会
    dp = [0 for _ in range(c+1)]
    one_list=range(1, len(w)+1)
    two_list=list(reversed(range(1, c+1)))
    for i in one_list:
        for j in two_list:#这里必须用逆序
            if w[i-1] <= j:
                print(dp[j-w[i-1]]+v[i-1])
                dp[j] = max(dp[j], dp[j-w[i-1]]+v[i-1])
    return dp[c]

print(pack1([2,3,4,5], [3,4,5,6], 8))
print(max(1,2))