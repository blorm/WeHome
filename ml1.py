

def diff(y, x, w):
    if len(x) != len(w):
        print 'error'
        exit()
    d = 0
    for i in range(len(x)):
        d += w[i] * x[i]
    return y - d

def loss():
    l = 0
    for i in range(n):
        l += (t_price[i] - price[i]) ** 2
    return l / n

n = 5
size   = [50,   50,  80,  80, 100]
beds   = [ 1,    2,   2,   3,   3]
washer = [ 0,    1,   1,   1,   1]
price  = [250, 300, 400, 450, 490]

iter = 100
a_size, a_beds, a_washer = 0, 0, 0

# y = wx + b
w = [2.76, 39, 24]
b = 73
alpha = [0.0001, 0.0001, 0.1, 0.2]
N = 10000
for i in range(N):
    for j in range(5):
        w[0] += alpha[0] * (diff(price[j], [size[j], beds[j], washer[j]], w) - b) * size[j]
        w[1] += alpha[1] *(diff(price[j], [size[j], beds[j], washer[j]], w) - b) * beds[j]
        w[2] += alpha[2] * (diff(price[j], [size[j], beds[j], washer[j]], w) - b) * washer[j]
        b += alpha[3] * (diff(price[j], [size[j], beds[j], washer[j]], w) - b)
    print w, b


t_price = [0 for i in range(n)]
for i in range(n):
    t_price[i] = int( size[i] * w[0] + beds[i] * w[1] + washer[i] * w[2] + b)
print t_price

print loss()


# for i in range(2):
#     # price = a_size * size + ...
#     a = []
#     for i in range(5):
#         a.append((price[i] - a_beds * beds[i] - a_washer * washer[i]) / 1.0 / size[i])
#         # print a[i]
#     a_size = sum(a) / n
#     print 'a_size', a_size
#
#     # price = a_size * size + a_beds * beds +...
#     a = []
#     for i in range(5):
#         a.append( (price[i] - a_size * size[i] - a_washer * washer[i]) / 1.0 / beds[i])
#         # print a[i]
#     a_beds = sum(a) / n
#     print 'a_beds', a_beds
#
#     # price = ... + a_washer * washer
#     a = []
#     for i in range(5):
#         if washer[i] == 0:
#             a.append(0)
#             continue
#         a.append( (price[i] - a_size * size[i] - a_beds * beds[i]) / 1.0 / washer[i] )
#         # print a[i]
#     a_washer = sum(a) / len(a)
#     print 'a_washer', a_washer
#     print

t_n = 2
t_size = [40, 60]
t_beds = [1, 2]
t_washer = [0, 0]
t_price = [0, 0]
for i in range(t_n):
    t_price[i] = t_size[i] * w[0] + t_beds[i] * w[1] + t_washer[i] * w[2] + b
print t_price

t_price = [0 for i in range(n)]
for i in range(n):
    t_price[i] = int( size[i] * a_size + beds[i] * a_beds + washer[i] * a_washer )
print t_price

# a = []
# for i in range(5):
#     a.append( (price[i] - a_beds * beds[i] - a_washer * washer[i] ) / 1.0 / size[i] )
#     print a[i]
# a_size = sum(a) / n
# print 'a_size_2', a_size
#
# t_price = [0 for i in range(n)]
# for i in range(n):
#     t_price[i] = int( size[i] * a_size + beds[i] * a_beds + washer[i] * a_washer )
# print t_price