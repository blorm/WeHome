import pymysql.cursors
import time

def mysql():
    connection = pymysql.connect(host='localhost', port=3306,
                                 user='root', password='admin',
                                 db='how', charset='utf8')

    with open('structures.txt', 'r') as f:
        sql = f.readlines()
    # print sql
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()

def inspect():
    N = 15019
    title = ['id', 'source_id', 'source_name', 'state', 'city', 'area_id', 'neighborhood',
             #                    'zillow'      'WA'   'Seattle' '42660'       111
             'neighborhood_id', 'zipcode', 'addr', 'longitude', 'latitude', 'room_type',
             #      114             39     14629      4004         4068         12
              'beds', 'baths', 'size', 'status', 'price', 'zetimate', 'rent_zestimate',
             #  16      32       1917  1,2,3,4,5   1827      8929         886
             'pict_urls', 'updated_at', 'created_at', 'score', 'house_price', 'rent',
             #                16            6           46          7726        2310
             'ratio_radio', 'increase_radio', 'rental_income_ratio', 'adjust_score',
             # 8030             35                  8030                19
             'property_score', 'neightborhood_score', 'latlng', 'neighbor_knn',
             # [100, 60]         [30, 50, 60, 70]      4168         881
             'neighbor_from_zip', 'score_version', 'airbnb_rent', 'tax', 'insurance',
             # t \N                   '0'             478           7726    7726
             'pm_long', 'pm_short', 'year_built', 'online_date']
             # 2310         478         127         294
    # status: for rent=1, for sale=2, off market=3, sold=4, pre-market=5
    # price: rental or for sale

    status = ['', 'for rent', 'for sale', 'off market', 'sold', 'pre-market']
             #      2239        1720      9437 4408      1466       157
             # 2000 + 239       1347        4408         1377       152
    sum = 0
    show_index = [16, 17, 10, 11, 19, 25]
    for t in [12]:
        # print title[t]
        list = []

        with open('seattle.csv', 'r') as f:
            for i in range(N):
                data = f.readline()
                if data != '':
                    line = data.strip().split('\t')

                    # if line[t] not in list:
                    #     list.append(line[t])

                    # for j in range(len(line)):

                    if line[16] == '5':     #  and line[25] != '\N'
                        sum += 1
                        for j in show_index:
                            if j == 16:
                                print '%20s: %s %s' % (title[j], line[j], status[int(line[j])])
                            else:
                                print '%20s: %s' %(title[j], line[j])
                        print '=============='
        print sum
        print list
        print len(list)
        print

def clean():
    keep_index = [0, 10, 11, 12, 13, 14,   15,   16,   17,   19,      25]
                #id lng lat type bed bath size status price rent_z  rent
    fin = open('seattle.csv', 'r')
    fout = open('seattle_valid.csv', 'w')
    if fin == '' or fout == '':
        print 'file error'
        exit()

    while True:
        data = fin.readline()
        if data == '':
            break
        line = data.strip().split('\t')
        # valid info
        if line[16] == '1' or line[25] != '\N':
            # lineout = ''
            # rent: throw decimal parts... 2315.234 -> 2315
            # if line[25] != '\N':
            #     line[25] = str(int(float(line[25])))
            # for i in keep_index:
            #     lineout += line[i] + '\t'
            # lineout = lineout[:-1] + '\n'
            # fout.write(lineout)
            fout.write('\t'.join(line, '\t') + '\n')

    fin.close()
    fout.close()

def divide():
    fin = open('seattle_valid.csv', 'r')
    ftrain = open('seattle_train.csv', 'w')
    ftest = open('seattle_test.csv', 'w')
    sum_train = 0
    if not(fin and ftrain and ftest):
        print 'file error'
        exit()

    while True:
        data = fin.readline()
        if data == '':
            break
        line = data.strip().split('\t')

        # 2000 train data
        if line[16] == '1' and sum_train < 2000:
            sum_train += 1
            ftrain.write('\t'.join(line) + '\n')
        # 7524 test data
        # no... only 200+ data
        elif line[16] == '1':
            ftest.write('\t'.join(line) + '\n')

    fin.close()
    ftrain.close()
    ftest.close()

# y^ = sigma(wi * xi) + b
def y_est(x, w, b):
    d = 0
    for i in range(3):
        if x[i] != '\N':
            d += x[i] * w[i]
    return d + b

# loss: variance = (y - y^)^2 / n
def loss(y, x, w, b):
    lenth = len(x)
    sigma = 0
    for i in range(lenth):
        sigma += (y[i] - y_est(x[i], w, b)) ** 2
    return sigma / lenth

def read(filename):
    data = []
    x, y = [], []
    with open(filename, 'r') as f:
        line = f.readline()
        while line != '':
            line = line.strip().split('\t')
            data.append(line)
            # no size data
            if line[15] == '0' or line[15] == '\N' \
            or line[13] == '\N' or line[14] == '\N':
            # no bed / bath data
                line = f.readline()
                continue
            y.append(float(line[17]))   # ?
            x.append([line[15], line[14], line[13]])
            for i in range(3):
                if x[-1][i] != '\N':
                    x[-1][i] = float(x[-1][i])
            line = f.readline()
    return data, x, y


def linear(data, x, y):
    # bed  bath  size
    # 13   14    15
    len_train = len(x)
    print len_train
    # size bath bed
    w = [1.2, 200, 70]  # 520
    b = 400
    alpha = [0.0000001, 0.0001, 0.0001, 0.1]
    N = 100
    for n in range(5):
        # print data[n][13:15]
        for j in range(3):
            for i in range(len_train): #len_train
                w[j] += alpha[j] * (y[i] - y_est(x[i], w, b)) * x[i][j]
                # print 'x, y', x[i], y[i], y_est(x[i], w, b)
                # print w, b
            # time.sleep(1)
            b += alpha[3] * (y[i] - y_est(x[i], w, b))
    # print w, b
    # print int(loss(y, x, w, b))
    return w, b

def test(data, x, y, w, b):
    print '       zetimate      y     y^    rent'
    sum_zeti = 0
    sigma_zeti = 0
    sigma_rent = 0
    sigma_mine = 0
    for i in range(len(y)):
        print '%16s %7.1f %.2f %s' %(data[i][19], y[i], y_est(x[i], w, b), data[i][25])
        sigma_rent += (float(data[i][25]) - y[i]) ** 2
        if data[i][19] != '\N':
            sum_zeti += 1
            sigma_zeti += (float(data[i][19]) - y[i]) ** 2
            sigma_mine += (y_est(x[i], w, b)  - y[i]) ** 2

    print
    print 'test data lenth:', len(data)
    print 'the variance sigma  :%12.2f' % loss(y, x, w, b)
    print 'the variance of rent:%12.2f' % (sigma_rent / len(data))

    print
    print 'mine V.S. zetimate:'
    print 'the variance of me      : %10.2f' % (sigma_mine / sum_zeti)
    print 'the variance of zetimate: %10.2f' % (sigma_zeti / sum_zeti)



if __name__ == '__main__':
    # inspect()
    # clean()
    # divide()
    data, x, y = read('seattle_train.csv')
    w, b = linear(data, x, y)
    print w, b
    data, x, y = read('seattle_test.csv')
    test(data, x, y, w, b)
