fp = open('C:/Users/acer/Downloads/OR111-2_midtermProject_dataAndPrograms/data/instance01.txt', 'r')
lines = fp.readlines()
Number_of_station, Number_of_car, number_of_level, number_of_order, number_of_day, moving_limit=map(int, lines[1].split(","))
pointer=4

station_status=[] #每個站點儲存不同level的車子數
car_rent_status={} #每個站點儲存的車子
global car_level_fee
car_level_fee = {} #每個車子的價位

order=[] #每個站點存不同的訂單排程
distance=[] #每個站之間的時間


assignment_plan=[]
arrangement_plan=[]

for i in range(Number_of_station):
    station_status.append([0]*number_of_level)
    car_rent_status[i+1]=([])
    distance.append([])

#讓每個站點儲存不同level的車子數
for i in range(Number_of_car):
    item = list(map(int, lines[pointer].strip().split(",")))
    car_rent_status[item[2]].append(item)
    station_status[item[2]-1][item[1]-1]+=1
    pointer+=1

pointer+=2

#每個level車子的價位
for i in range(number_of_level):
    typ = list(map(int, lines[pointer].strip().split(",")))
    car_level_fee[typ[0]]=typ[1]
    pointer+=1
    
pointer+=2

for i in range(number_of_order):
    typ1=lines[pointer].strip().split(",")[-2:]
    typ= list(map(int, lines[pointer].strip().split(",")[:-2]))+typ1
    pointer+=1
    order.append(typ)
    assignment_plan.append(0)
    arrangement_plan.append([])


pointer+=2
for i in range(Number_of_station):
    for j in range(Number_of_station):
        typ = list(map(int, lines[pointer].strip().split(",")))
        pointer+=1
        distance[i].append(typ[2])

#print(order)

# 根据訂單時間由早到晚排序
#order.sort(key=lambda x: x[4])
print(order)
print(car_rent_status)
print(station_status)
print(car_level_fee)
