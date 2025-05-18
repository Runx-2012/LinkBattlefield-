import sys

import copy
from itertools import permutations
import multiprocessing
from multiprocessing import Manager
from tqdm import tqdm  # 直接导入类，可直接使用 tqdm(...)

import time
start_time0 = time.time()  # 记录开始时间




HP_list = {1:[1400200,[3],0,0],2:[1401600,0],3:[1194590,[8],1400200,0],4:[1412800,[9],0,0],5:[1425000,[1]],
      6:[1226720,0],7:[1468600,0],8:[1502400,0],9:[1313930,[2]],10:[1600000,0],
      11:[2082750,[3,4],0,0],12:[2356560,[3],0,0],13:[2299250,[2]],14:[2630880,0],15:[2801250,0],
      16:[2774000,[1]],17:[2978250,[9],0,0],18:[3208000,[3],0,0],19:[3464750,[8],1400200,0],20:[3750000,[1]],
      21:[4878300,[2,4]],22:[6353280,0],23:[6325110,[2]],24:[6247200,[8,9],1400200,0],25:[4525000,[2,3,9],0,0],
      26:[7372800,[8,9],1400200,0],27:[8004900,[1,8],1400200,0],28:[8685600,0],29:[9416700,[1]],30:[11220000,[1]],
      31:[7358200,[1]],32:[7953600,[2]],33:[12881100,[2]]}
#3-时间吞噬，每过3秒减少1秒召唤时间
#4-CD增加
#8-恢复血量，每过3秒恢复10%的血量
#9-次数回血，每段1%，汇总回血


#物伤-1；魔法-2，友军伤害-3，,三次2倍-5，重制-7，概率两倍-9，
#post_check：个人伤害-4,加时间-8，治疗-10，加攻击次数-11
#预留-6

#[1,7,27,24,2]

P_list = {}
P_list[1] = [5,45,3,1,0,"黑骑士",1,0]
P_list[2] = [1,39,1,5,0,"莫玄",1,0]
P_list[3] = [4,70,2,2,0,"冰雷",2,0]
P_list[4] = [5,48,3,4,0,"火毒",2,0]
P_list[5] = [8,100,2,7,0,"圣骑",1,0]
P_list[6] = [8,40,5,7,0,"队长",1,0]
P_list[7] = [3,58,2,5,0,"英雄",1,0]
P_list[8] = [4,135,1,1,0,"船长",2,0]
P_list[9] = [4,70,2,3,0,"神射",1,0]
P_list[10] = [8,200,1,7,0,"箭神",1,0]
P_list[11] = [5,87,2,2,0,"炎术士",2,0]
P_list[12] = [2,39,2,5,0,"夜行者",1,0]
P_list[13] = [5,48,3,4,0,"侠影",1,0]
P_list[14] = [1,39,1,5,0,"战神",1,0]
P_list[15] = [1,18,2,3,0,"幻影",2,0]
P_list[16] = [2,35,2,2,0,"唤灵",2,0]
P_list[17] = [4,59,2,4,0,"红毛",1,0]
P_list[18] = [8,200,1,7,0,"魂骑士",1,0]
P_list[19] = [5,44,5,8,0,"白毛",1,0]
P_list[20] = [2,33,2,9,0,"机械师",2,0]
P_list[21] = [3,23,1,11,0,"隐士",1,0]
P_list[22] = [2,67,1,9,0,"奇袭者",1,0]
P_list[23] = [6,60,3,10,0,"风灵",1,0]
P_list[24] = [3,55,2,8,0,"夜光",2,0]
P_list[25] = [3,25,4,9,0,"火炮",1,0]
P_list[26] = [5,111,2,8,0,"双刀",1,0]
P_list[27] = [3,19,2,4,0,"隐月",1,0]
P_list[28] = [6,60,3,10,0,"施亚",2,0]
P_list[29] = [4,29,3,11,0,"尖兵",1,0]
P_list[30] = [5,33,4,11,0,"龙神",2,0]
P_list[31] = [3,53,2,1,0,"双弩",1,0]
P_list[32] = [6,540,2,10,0,"主教",2,0]


def filtered_permutations(input_dict):
    # 筛选出value小于10的元素
    filtered_items = [key for key, value in input_dict.items() if value[0] <= 6]
    #filtered_items = [item for item in input_dict.items() if item[1][0] <= 6]
    return list(permutations(filtered_items, 5))
temp = filtered_permutations(P_list)
# end_time = time.time()  # 记录结束时间
# run_time = end_time - start_time0  # 计算运行时间
# print("计算样本空间耗时：",run_time)

#print(temp)
'''计算AD和AP伤害sum_damage(Pgroup[key][0], Pgroup[key][4] - 1, Pgroup[key][1], Pgroup[key][2], Pgroup[key][6])'''
def sum_damage(atk_para):
    ad =0
    ap =0
    atk_count = atk_para[2]
    if 1 <= atk_para[0] <= 8:
        if atk_para[7] % atk_para[0] == 0:
            if atk_para[6] == 1:
                ad = atk_para[1] * atk_para[2]
            else:
                ap = atk_para[1] * atk_para[2]

    else:
        raise ValueError("攻击间隔校验出错")
    return ad, ap, atk_count
'''检查伤害是否打过BOSS'''


'''检查BOSS技能3-3秒时间增加'''
def special_check_HP(Bossxueliang):
    output = []
    minkey = min(Bossxueliang)
    #print(Bossxueliang[minkey])
    if Bossxueliang[minkey][1] != 0:
        if 3 in Bossxueliang[minkey][1]:##特殊技能包括3-时间增加
            if Bossxueliang[minkey][3] == 0:
                pass
            elif Bossxueliang[minkey][3] % 3 == 0:
                output.append(3)
        if 8 in Bossxueliang[minkey][1]:  ##特殊技能包括3-时间增加
            if Bossxueliang[minkey][3] == 0:
                pass
            elif Bossxueliang[minkey][3] % 3 == 0:
                output.append(8)
        if {3, 8} & set(Bossxueliang[minkey][1]):
            Bossxueliang[minkey][3] = Bossxueliang[minkey][3] + 1
            ##如果BOSS技能有3or8，说明boss和时间有关，boss时间需要不断自加
        if 9 in Bossxueliang[minkey][1]:  ##特殊技能包括3-时间增加
                output.append(9)
    return output

#物伤-1；魔法-2，友军伤害-3，,三次2倍-5，重制-7，概率两倍-9，
'''BUFF check，也包括概率暴击、次数暴击'''
def atk_pre_check(a,b,c,d):
    buff=[]
    ad_buff=1
    ap_buff=1
    '''第一段：计算技能伤害'''
    '''##检查本次攻击是否满足9-概率翻倍或5-三次两倍'''
    if a[b][3] == 9:
        c = c * 1
        d = d * 1
    elif a[b][3] == 5:
        if a[b][7] != 0:
            if (a[b][7] +a[b][1])%a[b][1]  == 3:
                c = 2 * c
                d = 2 * d
    elif a[b][3] == 4:#个人伤害-4
        #print(a[b])
        if a[b][7] == 0:
            pass
        elif a[b][7] % a[b][0] == 0:
            ad_buff = ad_buff + 0.1
            ap_buff = ap_buff + 0.1

    '''第二段，计算buff'''
    for items in a.values():
        #print("items[3]",items[3])
        buff.append(items[3])
        # print(buff)
        if 1 in buff:
            ad_buff = ad_buff + 0.1
        if 2 in buff:
            ap_buff = ap_buff + 0.1
        if 3 in buff:
            ad_buff = ad_buff + 0.1
            ap_buff = ap_buff + 0.1
        c = c*ad_buff
        d = d*ap_buff
    return c,d

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



def check_damage(Bossxueliang, wulishanghai, mofashanghai,Boss_Skill,atk_count, zhandouli=300000):
    minkey = min(Bossxueliang)
    if Bossxueliang[minkey][1] != 0:
        if 1 in Bossxueliang[minkey][1]:
            wulishanghai = wulishanghai *0.7
        if 2 in Bossxueliang[minkey][1]:
            mofashanghai = mofashanghai *0.7
    Damage = wulishanghai + mofashanghai
    Damage = Damage * zhandouli / 100

    if Damage > 0:
        ''' BOSS血量和伤害比较。并且考虑要不要8-回血'''
        if Bossxueliang[minkey][0]-Damage <=0:
            #print("消除Boss，进入下一秒")#when 伤害超过剩余血量
            del Bossxueliang[minkey]
            return minkey,False
        else:
            Bossxueliang[minkey][0]  = Bossxueliang[minkey][0]-Damage
            if 8 in Boss_Skill:
                Bossxueliang[minkey][0] = min(Bossxueliang[minkey][0] + Bossxueliang[minkey][2] * 0.1,
                                              Bossxueliang[minkey][0])
                #print(minkey,"号boss释放了8-3秒回血")
            if 9 in Boss_Skill:
                Bossxueliang[minkey][0] = min(Bossxueliang[minkey][0] + Bossxueliang[minkey][2] * 0.01*atk_count,
                                              Bossxueliang[minkey][0])
                #print("Boss受击回血")
            if 4 in Boss_Skill:
                pass
    return minkey,True


def process_item(shared_dict,lock,item):
    #print("进入主进程")
    HP = copy.deepcopy(HP_list)
    P = copy.deepcopy(P_list)
    temp1 = [item[0], item[1], item[2], item[3]]
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
    Damage1 = 0
    Damage2 = 0

    if current_time == 0:
        #print("current_time = ", current_time)
        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad = sum_damage(Pgroup[key])[0]
            ap = sum_damage(Pgroup[key])[1]
            atk_count = sum_damage(Pgroup[key])[2]
            ad, ap = atk_pre_check(Pgroup, key, ad, ap)

            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        current_time += 1
        Damage1 = 0
        Damage2 = 0
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

            ad = sum_damage(Pgroup[key])[0]
            ap = sum_damage(Pgroup[key])[1]
            atk_count = sum_damage(Pgroup[key])[2]
            ad, ap = atk_pre_check(Pgroup, key, ad, ap)

            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        Damage1 = 0
        Damage2 = 0
        current_time += 1
    if current_time == 2:
        #print("current_time = ", current_time)
        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad = sum_damage(Pgroup[key])[0]
            ap = sum_damage(Pgroup[key])[1]
            atk_count = sum_damage(Pgroup[key])[2]
            ad, ap = atk_pre_check(Pgroup, key, ad, ap)

            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        current_time += 1
        Damage1 = 0
        Damage2 = 0
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

            ad = sum_damage(Pgroup[key])[0]
            ap = sum_damage(Pgroup[key])[1]
            atk_count = sum_damage(Pgroup[key])[2]
            ad, ap = atk_pre_check(Pgroup, key, ad, ap)

            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        Damage1 = 0
        Damage2 = 0
        current_time += 1
    if current_time == 4:
        #print("current_time = ", current_time)
        chkeck_HP = special_check_HP(HP)
        for key in Pgroup:
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1

            ad = sum_damage(Pgroup[key])[0]
            ap = sum_damage(Pgroup[key])[1]
            atk_count = sum_damage(Pgroup[key])[2]
            ad, ap = atk_pre_check(Pgroup, key, ad, ap)

            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        Damage1 = 0
        Damage2 = 0
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

            ad = sum_damage(Pgroup[key])[0]
            ap = sum_damage(Pgroup[key])[1]
            atk_count = sum_damage(Pgroup[key])[2]
            ad, ap = atk_pre_check(Pgroup, key, ad, ap)

            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        Damage1 = 0
        Damage2 = 0
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


        #print("current_time = ", current_time)
        chkeck_HP = special_check_HP(HP)
        min_key = min(Pgroup)
        if Pgroup[min_key][4] == 30:
            del Pgroup[min_key]
            if len(Pgroup) == 0:
                print("程序结束：队伍耗尽")
                break
        elif 3 in chkeck_HP:
            if Pgroup[min_key][4] +1 >= 30:
                del Pgroup[min_key]

        if global_count < len(sorted_indices):  # 检查link池子用没有用尽
            if len(Pgroup) < 4:  ###检查要不要新增link
                new_key = max(Pgroup.keys()) + 1
                Pgroup[new_key] = P[sorted_indices[global_count]]
                final_list.append(sorted_indices[global_count])
                global_count = global_count + 1
                # if global_count == 9:
                #     print("已使用8个Link，程序终止")
                #     sys.exit()  # 退出整个程序，后续代码不会执行

        # print("场上队员",Pgroup)

        for key in Pgroup:
            #print(Pgroup)
            if 3 in chkeck_HP:
                Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][4] = Pgroup[key][4] + 1
            Pgroup[key][7] = Pgroup[key][7] + 1
            if Pgroup[key][4] >= 30:
                continue
            '''计算伤害（计算伤害前先precheck，看看buff）'''

            ad = sum_damage(Pgroup[key])[0]
            ap = sum_damage(Pgroup[key])[1]
            atk_count = sum_damage(Pgroup[key])[2]
            ad, ap = atk_pre_check(Pgroup, key, ad, ap)

            minkey, Falsechk = check_damage(HP, ad, ap, chkeck_HP, atk_count)
            if ad > 0 or ap > 0:
                atk_post_check(Pgroup, key)
            if Falsechk is False:
                break
        Damage1 = 0
        Damage2 = 0
        #print("minkey层数===", minkey)


        if len(HP) == 0:
            print("程序结束：H已经耗尽")
            break
        current_time += 1
    #     print("final_list", final_list)
    # print("时间耗尽")
    # print("已使用Link数 = ", global_count)
    # print("finallist", final_list)
    if minkey == 30:
        with lock:
            shared_dict['call_count'] = shared_dict.get('call_count', 0) + 1
            shared_dict['max_list'][shared_dict['call_count']]= final_list
    return minkey, final_list



final_final_list = {}
result1 = []


if __name__ == '__main__':

    print("总样本数量", len(temp))
    start_time1 = time.time()  # 记录开始时间
    # with Pool(processes=8) as pool:
    #     print("总样本数量",len(temp))
    #     #temp = temp[0:20000]
    #     results = pool.map(process_item, temp)
    #print("初始化共享状态")

    with Manager() as manager:
        shared_dict = manager.dict()
        shared_dict['max_first_4_result'] = 0  # 初始值
        shared_dict['call_count'] = 0
        shared_dict['max_list'] = manager.dict()
        lock = manager.Lock()

        with multiprocessing.Pool(processes=9) as pool:
            print('进入主进程')
            temp = temp[0:60000]
            results = pool.starmap(process_item, [(shared_dict, lock, item) for item in temp])
            # 使用偏函数绑定共享变量
        print(f"process_item 函数共被调用 次",shared_dict['call_count'])
        print(f"有关的名单", shared_dict['max_list'])

    final_final_list = {minkey: final_list for minkey, final_list in results}

    ##把Results解析成level:final_list键值对的形式，存成字典

    max_key = max(final_final_list.keys())  # 或者直接用 max(my_dict)
    min_key = min(final_final_list.keys())


    result = final_final_list[max_key]
    result1 = []
    for i in result:
        result1.append(P_list[i][5])
    print("最大的层数是", max_key, "阵容为", result1)
    result1 = []
    result = final_final_list[min_key]
    for i in result:
        result1.append(P_list[i][5])
    print("最小的层数是", min_key, "阵容为", result1)

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






