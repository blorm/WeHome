import pymysql.cursors
import cPickle

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
             #      2239        1720      9437 4408      1466
    sum = 0
    show_index = [16, 17, 19, 25]
    for t in [12]:
        # print title[t]
        list = []

        with open('seattle.csv', 'r') as f:
            for i in range(N):
                data = f.readline()
                if data != '':
                    line = data.strip().split('\t')

                    if line[t] not in list:
                        list.append(line[t])

                    # for j in range(len(line)):

                    # if line[16] == '1':     #  and line[25] != '\N'
                    #     sum += 1
                    #     for j in show_index:
                    #         if j == 16:
                    #             print '%20s: %s %s' % (title[j], line[j], status[int(line[j])])
                    #         else:
                    #             print '%20s: %s' %(title[j], line[j])
                    #     print '=============='
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
            lineout = ''
            # rent: throw decimal parts... 2315.234 -> 2315
            if line[25] != '\N':
                line[25] = str(int(float(line[25])))
            for i in keep_index:
                lineout += line[i] + '\t'
            lineout = lineout[:-1] + '\n'
            fout.write(lineout)

    fin.close()
    fout.close()


if __name__ == '__main__':
    # inspect()
    clean()