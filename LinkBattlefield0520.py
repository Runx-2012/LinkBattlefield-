import sys

import copy
from itertools import permutations
import multiprocessing
from multiprocessing import Manager
from tqdm import tqdm  # 直接导入类，可直接使用 tqdm(...)

import time
start_time0 = time.time()  # 记录开始时间
from deduplicated import deduplicated
from data_filter import filtered_permutations
import atkChk
import ini_data

# HP_list = {1:[1400200,[3],1400200,0],2:[1401600,0],3:[1194590,[8],1194590,0],4:[1412800,[9],1412800,0],
#            5:[1425000,[1]],6:[1226720,0],7:[1468600,0],8:[1502400,0],
#            9:[1313930,[2]],10:[1600000,0],11:[2082750,[3,4],2082750,0],12:[2356560,[3],2356560,0],
#            13:[2299250,[2]],14:[2630880,0],15:[2801250,0],16:[2774000,[1]],
#            17:[2978250,[9],2978250,0],18:[3208000,[3],3208000,0],19:[3464750,[8],3464750,0],20:[3750000,[1]],
#            21:[4878300,[2,4],0,0],22:[6353280,0],23:[6325110,[2]],24:[6247200,[8,9],6247200,0],
#            25:[4525000,[2,3,9],4525000,0],26:[7372800,[8,9],7372800,0],27:[8004900,[1,8],8004900,0],
#            28:[8685600,0],29:[9416700,[1]],30:[11220000,[1]],
#            31:[7358200,[1]],32:[7953600,[2]],33:[12881100,[2]]}
#
#
# #[1,7,27,24,2]
#
# P_list = {}
# P_list[1] = [6,45,3,1,0,"1",1,0]
# P_list[2] = [2,39,1,5,0,"2",1,0]
# P_list[3] = [5,70,2,2,0,"3",2,0]
# P_list[4] = [6,48,3,4,0,"4",2,0]
# P_list[5] = [9,100,2,7,0,"5",1,0]
# P_list[6] = [9,40,5,7,0,"6",1,0]
# P_list[7] = [4,58,2,5,0,"7",1,0]
# P_list[8] = [5,135,1,1,0,"8",2,0]
# P_list[9] = [5,70,2,3,0,"9",1,0]
# P_list[10] = [9,200,1,7,0,"10",1,0]
# P_list[11] = [6,87,2,2,0,"11",2,0]
# P_list[12] = [3,39,2,5,0,"12",1,0]
# P_list[13] = [6,48,3,4,0,"13",1,0]
# P_list[14] = [2,39,1,5,0,"14",1,0]
# P_list[15] = [2,18,2,3,0,"15",2,0]
# P_list[16] = [3,35,2,2,0,"16",2,0]
# P_list[17] = [5,59,2,4,0,"17",1,0]
# P_list[18] = [9,200,1,7,0,"18",1,0]
# P_list[19] = [6,44,5,8,0,"19",1,0]
# P_list[20] = [3,33,2,9,0,"20",2,0]
# P_list[21] = [4,23,1,11,0,"21",1,0]
# P_list[22] = [3,67,1,9,0,"22",1,0]
# P_list[23] = [7,60,3,10,0,"23",1,0]
# P_list[24] = [4,55,2,8,0,"24",2,0]
# P_list[25] = [4,25,4,9,0,"25",1,0]
# P_list[26] = [6,111,2,8,0,"26",1,0]
# P_list[27] = [4,19,2,4,0,"27",1,0]
# P_list[28] = [7,60,3,10,0,"28",2,0]
# P_list[29] = [5,29,3,11,0,"29",1,0]
# P_list[30] = [6,33,4,11,0,"30",2,0]
# P_list[31] = [4,53,2,1,0,"31",1,0]
# P_list[32] = [7,90,2,10,0,"32",2,0]









'''检查BOSS技能3-3秒时间增加'''
def special_check_HP(Bossxueliang):
    output = []
    minkey = min(Bossxueliang)
    #print(Bossxueliang[minkey])
    if Bossxueliang[minkey][1] != 0:
        if 3 in Bossxueliang[minkey][1]:
            if Bossxueliang[minkey][3] == 0:
                pass
            elif Bossxueliang[minkey][3] % 3 == 0:
                output.append(3)
        if 8 in Bossxueliang[minkey][1]:
            if Bossxueliang[minkey][3] == 0:
                pass
            elif Bossxueliang[minkey][3] % 3 == 0:
                output.append(8)
        if 4 in Bossxueliang[minkey][1]:
            if Bossxueliang[minkey][3] == 0:
                pass
            elif Bossxueliang[minkey][3] % 3 == 0:
                output.append(4)

        if {3, 4,8} & set(Bossxueliang[minkey][1]):
            Bossxueliang[minkey][3] = Bossxueliang[minkey][3] + 1
            ##如果BOSS技能有3or8，说明boss和时间有关，boss时间需要不断自加
        if 9 in Bossxueliang[minkey][1]:  ##特殊技能包括3-时间增加
                output.append(9)
    return output

#物伤-1；魔法-2，友军伤害-3，,三次2倍-5，重制-7，概率两倍-9，
'''BUFF check，也包括概率暴击、次数暴击'''


'''计算11-攻击加次数，8增加时间，4-加伤害，5-治疗'''
def atk_post_check(a,b):
    if a[b][3] == 11:#加攻击次数-11
        a[b][2] = a[b][2]+1
    elif a[b][3] == 8:#加时间-8
        #print(a[b])
        a[b][4] = a[b][4] - 1
    elif a[b][3] == 10:#治疗-10
        for key in a:
            if key != b:
                a[key][4] = a[key][4] -1
                if a[key][4] < 0:
                    a[key][4] = 0



def check_damage(Bossxueliang, wulishanghai, mofashanghai,Boss_Skill,atk_count, zhandouli=400000):
    minkey = min(Bossxueliang)


    if Bossxueliang[minkey][1] != 0:
        if 1 in Bossxueliang[minkey][1]:
            wulishanghai = wulishanghai *0.7
        if 2 in Bossxueliang[minkey][1]:
            mofashanghai = mofashanghai *0.7
    Damage = wulishanghai + mofashanghai
    Damage = Damage * zhandouli / 100


    Falsechk = True
    if Damage > 0:
        ''' BOSS血量和伤害比较。并且考虑要不要8-回血'''

        if Bossxueliang[minkey][0]-Damage <=0:
            #print("消除Boss，进入下一秒")#when 伤害超过剩余血量
            del Bossxueliang[minkey]
            Falsechk= False
            return minkey,Falsechk
        else:
            Bossxueliang[minkey][0]  = Bossxueliang[minkey][0]-Damage
            if 8 in Boss_Skill:
                if len(Bossxueliang[minkey]) > 2:
                    Bossxueliang[minkey][0] = min(Bossxueliang[minkey][0] + Bossxueliang[minkey][2] * 0.1,
                                                  Bossxueliang[minkey][0])
                else:
                    print(minkey)
                    print('长度有问题',Bossxueliang[minkey])
                #print(minkey,"号boss释放了8-3秒回血")
            if 9 in Boss_Skill:
                if len(Bossxueliang[minkey]) > 2:
                    Bossxueliang[minkey][0] = min(Bossxueliang[minkey][0] + Bossxueliang[minkey][2] * 0.01*atk_count,
                                                  Bossxueliang[minkey][0])
                else:
                    print(minkey)
                    print('长度有问题',Bossxueliang[minkey])
                #print("Boss受击回血")
    return minkey,Falsechk


def process_item(shared_dict,lock,item,HP_list,P_list):
    processtime0 = time.time()
    #print("进入主进程")
    HP = copy.deepcopy(HP_list)
    P = copy.deepcopy(P_list)

    temp1 = list(item)
    #temp1 = [item[0][0], item[1][0], item[2][0], item[3][0]]
    sorted_indices = sorted([k for k in P.keys() if k not in (temp1 +[]) ], key=lambda x: P[x][0])
    sorted_indices = temp1 + sorted_indices

    #print('当前循环的阵容', sorted_indices)
    '''每一个阵容都要跑下面这一段'''
    final_list = []
    current_time = 0  # 1指的是进程已经开始了，时间已经大于0了
    Pgroup = {}
    # print(P_list[sorted_indices[0]])
    # print(P[sorted_indices[0]])
    Pgroup[0] = P[sorted_indices[0]]
    final_list.append(sorted_indices[0])

    global_count = 1


    if current_time == 0:
        #print("current_time = ", current_time)
        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad ,ap,atk_count ,cd_reset= atkChk.atk_pre_check(Pgroup,key)
            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                print("结算了，跳过本轮后续结算")
                break
            if 4 in chkeck_HP:
                Pgroup[key][0] = Pgroup[key][0] + 1
        current_time += 1

    if current_time == 1:
        #print("current_time = ", current_time)
        if len(Pgroup) < 4:
            new_key = max(Pgroup.keys()) + 1
            Pgroup[new_key] = P[sorted_indices[1]]
            final_list.append(sorted_indices[1])
            global_count = global_count+1
        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad ,ap,atk_count ,cd_reset= atkChk.atk_pre_check(Pgroup, key)
            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        current_time += 1
    if current_time == 2:
        #print("current_time = ", current_time)
        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad ,ap,atk_count ,cd_reset= atkChk.atk_pre_check(Pgroup, key)
            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        current_time += 1

    if current_time == 3:
        #print("current_time = ", current_time)
        if len(Pgroup) < 4:
            new_key = max(Pgroup.keys()) + 1
            Pgroup[new_key] = P[sorted_indices[2]]
            final_list.append(sorted_indices[2])
            global_count = global_count+1

        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad ,ap,atk_count ,cd_reset= atkChk.atk_pre_check(Pgroup, key)
            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break

        current_time += 1
    if current_time == 4:
        #print("current_time = ", current_time)
        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad ,ap,atk_count ,cd_reset= atkChk.atk_pre_check(Pgroup, key)
            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break

        current_time += 1
    if current_time == 5:
        #print("current_time = ", current_time)
        if len(Pgroup) < 4:
            new_key = max(Pgroup.keys()) + 1
            Pgroup[new_key] = P[sorted_indices[3]]
            final_list.append(sorted_indices[3])

            global_count = global_count+1
        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad ,ap,atk_count ,cd_reset= atkChk.atk_pre_check(Pgroup, key)
            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break

        current_time += 1

    while current_time <= 180:
        # if global_count == 5:###当1～4阵容结束的时候，检查阵容是否是当前最大层数
        #     #print("5个角色登场")
        #     current_max_first_4_result = shared_dict['max_first_4_result']
        #
        #     if minkey < current_max_first_4_result:
        #         break
        #     elif minkey == current_max_first_4_result:
        #         continue
        #     else:
        #         with lock:  # 获取锁以确保线程安全
        #             shared_dict['max_first_4_result'] = minkey
        #         print("unlocked")




        chkeck_HP = special_check_HP(HP)
        min_key = min(Pgroup)
        # print("current_time = ", current_time)
        # print("current_floor",minkey)


        '''想设计一个最低层数隔断，如果120秒还没跑到这一层，就直接放弃这个组合'''
        if current_time==60:
            if min_key <=11:
                break



        if 3 in chkeck_HP:
            if Pgroup[min_key][4] >= 29:
                del Pgroup[min_key]
        else:
            if Pgroup[min_key][4] >= 30:
                del Pgroup[min_key]
        if len(Pgroup) == 0:
            print("程序结束：队伍耗尽")
            break

        if 4 in chkeck_HP:
            for key in Pgroup:
                Pgroup[key][0] += 1

        if global_count < len(sorted_indices):  # 检查link池子用没有用尽
            if len(Pgroup) < 4:  ###检查要不要新增link
                new_key = max(Pgroup.keys()) + 1
                Pgroup[new_key] = P[sorted_indices[global_count]]
                final_list.append(sorted_indices[global_count])
                global_count = global_count + 1

        for key in Pgroup:
            #print(key, Pgroup[key])
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1##lifetime+1，更快到达30
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            '''计算伤害（计算伤害前先precheck，看看buff）'''

            ad, ap, atk_count,cd_reset = atkChk.atk_pre_check(Pgroup, key)
            minkey, defeatchk = check_damage(HP, ad, ap, chkeck_HP, atk_count)

            if ad > 0 or ap > 0:
                if cd_reset == 1:
                    for key in Pgroup:
                        atk_post_check(Pgroup, key)
                else:
                    atk_post_check(Pgroup, key)

                #print(Pgroup[key],"频率+1")
            if defeatchk is False:
                break#######不确定如果第三秒如果成功结算了，还会不会加CD
        #print("minkey层数===", minkey)
        if 4 in chkeck_HP:
            for key in Pgroup:
                Pgroup[key][0] -= 1

            #print("删除当前HP里面的4",HP[minHP])

        if len(HP) == 0:
            #print("程序结束：H已经耗尽")
            break
        current_time += 1
    #     print("final_list", final_list)
    # print("时间耗尽")
    # print("已使用Link数 = ", global_count)
    # print("finallist", final_list)
    processtime1 = time.time()
    processtime = processtime1-processtime0
    with lock:
        # current_max_minkey = shared_dict.get('max_minkey', float('-inf'))
        # current_max_processtime = shared_dict.get('max_processtime', float('-inf'))
        # if minkey < 28:
        #     shared_dict['trash_list'][shared_dict['call_count']]= final_list
        if minkey >=32:
            # shared_dict['max_minkey'] = minkey
            shared_dict['call_count'] = shared_dict.get('call_count', 0) + 1
            shared_dict['max_list'][shared_dict['call_count']]= final_list
        # if processtime> current_max_processtime:
        #     shared_dict['max_processtime'] = processtime

    return minkey, final_list




final_final_list = {}
result1 = []


if __name__ == '__main__':

    P_list,HP_list = ini_data.ini_data()
    temp =  filtered_permutations(P_list, first_link=[], depth=5)
    range =0
    if range != 0 :
        temp = temp[:range]

    # filtered_permutations(P_list, first_link=[], depth=5)
    # [(1, 4, 26, 22, 14, 2, 15, 12, 16)]
    print("总样本数量", len(temp))
    start_time1 = time.time()  # 记录开始时间

    with Manager() as manager:
        shared_dict = manager.dict()
        shared_dict['max_first_4_result'] = 0  # 初始值
        shared_dict['call_count'] = 0
        shared_dict['max_minkey'] = float('-inf')
        shared_dict['max_processtime'] = float('-inf')
        shared_dict['max_list'] = manager.dict()
        shared_dict['trash_list'] = manager.dict()
        lock = manager.Lock()

        with multiprocessing.Pool(processes=9) as pool:
            print('进入主进程')
            #temp = temp[:30000]
            results = pool.starmap(process_item, [(shared_dict, lock, item,HP_list,P_list) for item in temp])
            # 使用偏函数绑定共享变量
            pool.close()
            pool.join()
        print(f"process_item 函数共被调用 次",shared_dict['call_count'])
        print(f"有关的名单", shared_dict['max_list'])
        print(f"单次最大运行时间",shared_dict['max_processtime'])
        max_list = copy.deepcopy(shared_dict['max_list'])

    aaa = deduplicated(max_list, depth = 5)
    #print(aaa)
    X = {1: [1, 12, 24, 22, 8], 2: [1, 17, 14, 12, 16]}

    final_final_list = {minkey: final_list for minkey, final_list in results}

    ##把Results解析成level:final_list键值对的形式，存成字典

    max_key = max(final_final_list.keys())  # 或者直接用 max(my_dict)
    min_key = min(final_final_list.keys())


    result = final_final_list[max_key]
    result1 = []
    for i in result:
        result1.append(P_list[i][5])
    print("最大的层数是", max_key, "组合为", result1)
    result1 = []
    result = final_final_list[min_key]
    for i in result:
        result1.append(P_list[i][5])
    print("最小的层数是", min_key, "组合为", result1)

    end_time = time.time()    # 记录结束时间
    run_time = end_time - start_time1  # 计算运行时间
    print(f"程序运行时间: {run_time} 秒")




    # if level == 27:
    #     print(final_list)
    #     sys.exit()





    #
    #
    #
    # final_final_list[level] = final_list

#
# max_key = max(final_final_list.keys())  # 或者直接用 max(my_dict)
# min_key = min(final_final_list.keys())
# # 获取对应的值
# result = final_final_list[max_key]
# for i in result:
#     result1.append(P[i][5])
# print("最大的层数是",max_key,"阵容为",result1)
# result1= []
# result = final_final_list[min_key]
# for i in result:
#     result1.append(P[i][5])
# print("最小的层数是",min_key,"阵容为",result1)
#






