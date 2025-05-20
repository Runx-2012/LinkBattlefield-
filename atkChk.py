
def skillEffect(a,b,c):##a是Pgroup，b是序号，C是groupBuff
    buff = 1
    ad = 0
    ap = 0

    damage = a[b][1] * a[b][2] if a[b][6] == 1 else -a[b][1] * a[b][2]
    if a[b][3] == 9:
        damage = damage * 1
    elif a[b][3] == 5:#每三下翻倍-5
        if ((a[b][7] + a[b][0])/a[b][0])%3==0:
            damage = 2*damage
    elif a[b][3] == 4:#个人伤害10%递增-4
        if (a[b][7] != 0) and (a[b][7] % a[b][0] == 0):
            buff = buff + 0.1

    if 3 in c:##团队通用伤害
        buff = buff + 0.1

    if damage > 0:
        if 1 in c:##团队物理伤害
            buff = buff + 0.1
        ad = damage * buff
    else:
        if 2 in c:##团队魔法伤害
            buff = buff + 0.1
        ap = -damage * buff
    return ad, ap, a[b][2]

def atk_pre_check(Pgroup,key):
    #print("atk_pre_check检查", Pgroup,key)
    ad= 0
    ap=0
    atk_count = 0
    cd_reset = 0
    groupBuff = [items[3] for items in Pgroup.values()]
    '''下面是循环生成的方案。性能比列表生成式更弱'''
    # for items in Pgroup.values():
    #     groupBuff.append(items[3])

    if Pgroup[key][7] % Pgroup[key][0] == 0:##技能释放判定：先检查是否释放技能
        if Pgroup[key][3] == 8:
            #print(Pgroup)
            cd_reset = 1
            for k in Pgroup.keys():
                d = skillEffect(Pgroup, k, groupBuff)
                ad += d[0]  # 累加物理伤害
                ap += d[1]  # 累加魔法伤害
                atk_count += d[2]  # 累加攻击次数
        else:
            d = skillEffect(Pgroup, key, groupBuff)
            ad = d[0]
            ap = d[1]
            atk_count = d[2]
    return ad ,ap,atk_count,cd_reset





if __name__ == '__main__':
    a = {1: [5, 70, 2, 2, 29, '3', 2, 29], 2: [7, 60, 3, 10, 30, '23', 1, 27], 3: [6, 44, 5, 8, 19, '19', 1, 24],
         4: [2, 39, 1, 5, 0, '2', 1, 0]}
    b = 0
    c = [2, 10, 8, 5]


    skillEffect(a,b,c)
