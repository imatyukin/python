#!/usr/bin/env python3
import sys
import codecs
import re
import netaddr


class Tee(object):
    # Output on the console and file

    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # The output to be visible immediately

    def flush(self):
        for f in self.files:
            f.flush()


# VLAN'ы на access switch
# show vlan
access_switch_vlans = 'ud_spb-sw3_vlans.conf'
access_switch_vlans = codecs.open(access_switch_vlans, 'r', encoding='utf-8', errors='ignore').read().splitlines()

# Конфигуационные файлы коммутатора и маршрутизатора
# show | display set | save /var/tmp/switch.conf
switch_conf = 'spbr-astk1.conf'
switch_conf = codecs.open(switch_conf, 'r', encoding='utf-8', errors='ignore').read().splitlines()
# show | display set | save /var/tmp/router.conf
router_conf = 'spbr-ar2.conf'
router_conf = codecs.open(router_conf, 'r', encoding='utf-8', errors='ignore').read().splitlines()

# Файл вывода результатов
f_out = 'a.out'

# Целевые файлы: load set /var/tmp/router
source_router_conf = 'spbr-ar2'
target_router_conf = 'spbr-ar4'
target_switch_conf = 'spbr-asw15'

# Интерфейсы коммутатора
# в сторону коммутаторов связанных с маршрутизатором
switch_to_sw_ifd = ' ge-0/0/2 ', ' ge-0/0/3 '

# Интерфейс маршрутизатора в сторону коммутатора
router_ifd = ['xe-9/3/3', 'xe-8/0/0', 'xe-5/3/0']

# Интерфейсы старого и нового маршрутизатора
ifd_source = 'xe-9/3/3'
ifd_target = 'ae8'

ip_source_neighbor = '95.167.88.60'
ip_target_neighbor = '213.59.207.99'


def main():
    # Объявление глобальных переменных
    global access_switch_vlans, switch_conf, router_conf, f_out, source_router_conf, target_router_conf, \
        target_switch_conf
    global switch_to_sw_ifd, router_ifd, ifd_source, ifd_target, ip_source_neighbor, \
        ip_target_neighbor

    with open(f_out, 'w') as f_out:
        # This will go to stdout and the file
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, f_out)

        # Находим все VLANы на коммутаторе доступа
        # Создаём словарь access_sw_vlans {VLAN: [Name]}
        access_sw_vlan_name = {}
        for line in access_switch_vlans:
            vlan_id = line.split()[0]
            vlan_name = line.split()[1]
            access_sw_vlan_name.update({vlan_id: vlan_name})
        #print(access_sw_vlan_name)

        # Находим все VLANы на ifd коммутатора агрегации
        # Создаём словарь sw_vlans {ifd: [VLANs]}
        sw_vlans = {}
        for line in switch_conf:
            for ifd in switch_to_sw_ifd:
                if ifd in line:
                    if 'vlan members' in line:
                        line = str(line).split(' ')
                        key = line[2].strip()
                        value = line[9].strip()
                        if '-' in value:
                            value = str(value).split('-')
                            value = list(range(int(value[0]), int(value[1])+1))
                        else:
                            value = int(value.split()[-1])
                        if key not in sw_vlans:
                            sw_vlans.setdefault(key, []).append(value)
                        else:
                            if isinstance(value, list):
                                for v in value:
                                    sw_vlans[key].append(v)
                            else:
                                sw_vlans[key].append(value)
        #print(sw_vlans)

        # Находим все VLANы на коммутаторе агрегации
        # Создаём словарь sw_vlans_name {VLAN: [Name]}
        ag_sw_vlan_name = {}
        for v in sw_vlans.values():
            for vlan_id in v:
                for line in switch_conf:
                    if 'set vlans ' and ' vlan-id ' in line:
                        vlan_id = str(vlan_id)
                        line = line.split()
                        vlan_id_temp = line[-1]
                        if vlan_id == vlan_id_temp:
                            vlan_name = line[2]
                            ag_sw_vlan_name.update({vlan_id: vlan_name})
        #print(ag_sw_vlan_name)

        # Проверка: находим общие VLAN'ы на коммутаторе доступа и агрегации
        # сравниваем keys в словарях access_sw_vlan_name и ag_sw_vlan_name
        # создаём словарь для нового коммутатора агрегации new_ag_sw_vlan_name {VLAN: [Name]}
        shared_vlans = set(access_sw_vlan_name.keys()) & set(ag_sw_vlan_name.keys())
        shared_vlans = sorted([int(x) for x in shared_vlans])
        #print(shared_vlans)
        new_ag_sw_vlan_name = {}
        for vlan_id in shared_vlans:
            for line in switch_conf:
                if 'set vlans ' and ' vlan-id ' in line:
                    vlan_id = str(vlan_id)
                    line = line.split()
                    vlan_id_temp = line[-1]
                    if vlan_id == vlan_id_temp:
                        vlan_name = line[2]
                        new_ag_sw_vlan_name.update({vlan_id: vlan_name})
        #print(new_ag_sw_vlan_name)

        # Находим общие VLANы на ifd маршрутизатора
        # Создаём словарь r_sw_vlans {ifl(ifd.unit): [VLAN]}
        r_sw_vlans = {}
        for line in router_conf:
            for ifd in router_ifd:
                if 'set interfaces ' + ifd in line and ' unit' in line:
                    # Для vlan-id
                    if ' vlan-id ' in line and 'input-vlan-map' not in line:
                        line = str(line).split()
                        key = line[2] + '.' + line[4]
                        value = int(line[-1])
                        for vlan_id in new_ag_sw_vlan_name.keys():
                            if value == int(vlan_id):
                                if key not in r_sw_vlans:
                                    r_sw_vlans.setdefault(key, []).append(value)
                                else:
                                    r_sw_vlans.key = value
                    # Для QinQ
                    elif 'vlan-tags outer' in line:
                        line = str(line).split()
                        key = line[2] + '.' + line[4]
                        value = int(line[-1])
                        for vlan_id in new_ag_sw_vlan_name.keys():
                            if value == int(vlan_id):
                                if key not in r_sw_vlans:
                                    r_sw_vlans.setdefault(key, []).append(value)
                                else:
                                    r_sw_vlans.key = value
        #print(r_sw_vlans)

        # Список совпадающих VLAN'ов для маршрутизатора и коммутатора
        vlans = []
        for k, v in r_sw_vlans.items():
            ifd = k.split('.')[0]
            for i in router_ifd:
                if ifd == i:
                    for j in v:
                        vlans.append(j)
        print("Sorted VLANs:")
        print(sorted(vlans))


        print("\nVLANs is starting. Please wait...\n")

        for line in switch_conf:
            if 'set vlans' and 'vlan-id' in line:
                vlan = int(line.split()[-1])
                for vlan_id in vlans:
                    if vlan_id == vlan:
                        print(line)

        print("\nVLANs completed.\n")


        # INET
        print("\nINTERNET is starting. Please wait...\n")
        # Находим все ifl c family inet, связанные с ifd
        ifl_inet = []
        for ifl in r_sw_vlans.keys():
            ifd = ifl.split('.')[0]
            unit = ifl.split('.')[1]
            for line in router_conf:
                if 'interfaces ' + ifd + ' unit ' + unit + ' family inet address' in line:
                    ifl_inet.append(ifl)

        # Оставляем только уникальные значения ifl в списке ifl_inet
        # (исключаем ifl, где на unit несколько ip-адресов)
        used = set()
        ifl_inet = [x for x in ifl_inet if x not in used and (used.add(x) or True)]
        # print(ifl_inet)

        # Находим ifl находящиеся в routing-instances (ri) из списка ifl_inet
        ifl_ri = []
        for ifl in ifl_inet:
            ifl_regex = re.compile(r"\b"+ifl+r"\b")
            for line in router_conf:
                if 'routing-instances' and ' interface ' + ifl in line:
                    if 'protocols' not in line:
                        if re.findall(ifl_regex, line):
                            ifl_ri.append(ifl)
        #print(ifl_ri)

        # Находим ifl связанные с GRT путём исключения ifl связанных с routing-instances
        ifl_grt = [x for x in ifl_inet if x not in ifl_ri]
        # print(ifl_grt)

        # разделяем ifl на ifd и unit
        ifd_unit = []
        for ifl in ifl_grt:
            ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
            ifd_unit.append(ifl)

        # выводим конфигурацию ifl и CoS для ifd (!!! проблема с deactivate interfaces !!!)
        for line in router_conf:
            for ifl in ifd_unit:
                if ifl in line:
                    print(line.replace(ifl.split()[0], ifd_target))

        # Словарь ip-addresses : ifls
        ip_addr_ifl_dic = {}
        for line in router_conf:
            for unit in ifd_unit:
                if unit in line:
                    if 'family inet address' in line:
                        match_ip_addr = list([fields.split()[8] for fields in line.splitlines()])[0]
                        ifl = unit.split(' ')[1] + '.' + unit.split(' ')[3]
                        ip_addr_ifl_dic.update({match_ip_addr: ifl})

        # Список static-routes для GRT
        static_routes_list = []
        for line in router_conf:
            if 'routing-instances' not in line:
                if 'routing-options static route' in line:
                    static_routes_list.extend(([fields.split()[4] for fields in line.splitlines()]))

        # Оставляем только уникальные значения static-routes
        used = set()
        static_routes_list = [x for x in static_routes_list if x not in used and (used.add(x) or True)]

        # Словарь static-routes : next-hops для GRT
        static_routes_nh_dic = {}
        for line in router_conf:
            if 'routing-instances' not in line:
                if 'routing-options static route' in line:
                    if 'next-hop' in line:
                        for static_route in static_routes_list:
                            if static_route in line:
                                match_next_hop = list([fields.split()[6] for fields in line.splitlines()])[0]
                                static_routes_nh_dic.update({static_route: match_next_hop})

        # Проверка вхождения next-hops для static-routes в подсети ifl
        # Словарь static-routes : next-hops для ifd
        static_routes_dic = {}
        for static_route, next_hop in static_routes_nh_dic.items():
            if next_hop in netaddr.IPSet(list(ip_addr_ifl_dic.keys())):
                static_routes_dic.update(({static_route: next_hop}))

        # Поиск bgp-neighbors и bgp-groups
        bgp_neighbors = []
        bgp_groups = []
        for line in router_conf:
            if 'routing-instances' not in line:
                if 'protocols bgp' in line:
                    if 'local-address' in line:
                        ip_addresses = [ip_addr.split('/')[0] for ip_addr in list(ip_addr_ifl_dic.keys())]
                        for ip_addr in ip_addresses:
                            if ip_addr in line:
                                for fields in line.splitlines():
                                    bgp_neighbors.append(fields.split()[6])
                                    bgp_groups.append(fields.split()[4])

        # Уникальные значения bgp-groups и bgp-neighbors
        used = set()
        bgp_neighbors = [x for x in bgp_neighbors if x not in used and (used.add(x) or True)]
        used = set()
        bgp_groups = [x for x in bgp_groups if x not in used and (used.add(x) or True)]

        # Вывод настроек
        for line in router_conf:
            if 'routing-instances' not in line:
                if 'routing-options static' in line:
                    for static_route, next_hop in static_routes_dic.items():
                        if static_route in line:
                            print(line)
                if 'protocols bgp' in line:
                    if 'neighbor' not in line:
                        for group in bgp_groups:
                            if group in line:
                                print(line)
                    if 'neighbor' in line:
                        for neighbor in bgp_neighbors:
                            if neighbor in line:
                                print(line)

        print("\nINTERNET completed.\n")

        # IP/VPN

        print("\nIP/VPN is starting. Please wait...\n")

        # ifl находящиеся в routing-instances (ri) находятся в списке ifl_ri
        # print(ifl_ri)

        # ifl связанные с VPLS
        ifl_ri_vpls = []
        for ifl in r_sw_vlans.keys():
            ifl_regex = re.compile(r"\b"+ifl+r"\b")
            for line in router_conf:
                if 'routing-instances' in line:
                    if 'protocols vpls' in line:
                        if 'interface' in line:
                            if re.findall(ifl_regex, line):
                                ifl_ri_vpls.extend(([fields.split()[8] for fields in line.splitlines()]))
        #print(ifl_ri_vpls)

        # Исключаем ifl связанные с VPLS
        ifl_ri = [x for x in ifl_ri if x not in ifl_ri_vpls]
        # print(ifl_ri)

        # разделяем ifl на ifd и unit
        ifd_unit = []
        for ifl in ifl_ri:
            ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
            ifd_unit.append(ifl)

        # выводим конфигурацию ifl и CoS для ifd
        for line in router_conf:
            for ifl in ifd_unit:
                if ifl in line:
                    print(line)

        # Словарь ifls : routing-instances
        ifl_ri_dic = {}
        for line in router_conf:
            for ifl in ifl_ri:
                if 'routing-instances' in line:
                    if 'protocols' not in line:
                        if 'interface' in line:
                            if ifl in line:
                                match_vrf = list([fields.split()[2] for fields in line.splitlines()])[0]
                                ifl_ri_dic.update({ifl: match_vrf})

        # Уникальные имена routing-instances
        ifl_ri_list = []
        ifl_ri_list.append(ifl_ri_dic.copy())
        ri_names = list(set(val for dic in ifl_ri_list for val in dic.values()))

        # Словарь ifls : ip-addresses
        ifl_ip_addr_dic = {}
        for line in router_conf:
            for unit in ifd_unit:
                if unit in line:
                    if 'family inet address' in line:
                        match_ip_addr = list([fields.split()[8] for fields in line.splitlines()])[0]
                        ifl = unit.split(' ')[1] + '.' + unit.split(' ')[3]
                        ifl_ip_addr_dic.update({ifl: match_ip_addr})

        # Словарь static-routes : routing-instances
        static_routes_ri_dic = {}
        for line in router_conf:
            if 'routing-instances' in line:
                if 'routing-options static' in line:
                    for vrf in ri_names:
                        if vrf in line:
                            if 'next-hop' in line:
                                match_static_route = list([fields.split()[6] for fields in line.splitlines()])[0]
                                static_routes_ri_dic.update({match_static_route: vrf})

        # Словарь static-routes : next-hops для routing-instances
        static_routes_nh_dic = {}
        for line in router_conf:
            if 'routing-instances' in line:
                if 'routing-options static' in line:
                    for vrf in ri_names:
                        if vrf in line:
                            if 'next-hop' in line:
                                for static_route, routing_instance in static_routes_ri_dic.items():
                                    if static_route in line:
                                        match_next_hop = list([fields.split()[8] for fields in
                                                               line.splitlines()])[0]
                                        static_routes_nh_dic.update({static_route: match_next_hop})

        # Проверка вхождения next-hops для static-routes в подсети ifl
        # Словарь static-routes : next-hops для ifd
        static_routes_dic = {}
        for static_route, next_hop in static_routes_nh_dic.items():
            if next_hop in netaddr.IPSet(list(ifl_ip_addr_dic.values())):
                static_routes_dic.update(({static_route: next_hop}))

        # Поиск bgp-neighbors и bgp-groups
        bgp_neighbors = []
        bgp_groups = []
        for line in router_conf:
            if 'routing-instances' in line:
                for vrf in ri_names:
                    if vrf in line:
                        if 'protocols bgp' in line:
                            if 'local-address' in line:
                                ip_addresses = [ip_addr.split('/')[0] for ip_addr in list(ifl_ip_addr_dic.values())]
                                for ip_addr in ip_addresses:
                                    if ip_addr in line:
                                        for fields in line.splitlines():
                                            bgp_neighbors.append(fields.split()[8])
                                            bgp_groups.append(fields.split()[6])

        # Уникальные значения bgp-groups и bgp-neighbors
        used = set()
        bgp_neighbors = [x for x in bgp_neighbors if x not in used and (used.add(x) or True)]
        used = set()
        bgp_groups = [x for x in bgp_groups if x not in used and (used.add(x) or True)]

        # Вывод настроек routing-instances
        for line in router_conf:
            if 'routing-instances' in line:
                for vrf in ri_names:
                    if vrf in line:
                        if 'routing-options static' in line:
                            for static_route, next_hop in static_routes_dic.items():
                                if static_route in line:
                                    print(line)
                        if 'routing-options static' not in line:
                            if 'protocols bgp' not in line:
                                if 'interface lo0' in line:
                                    print(line)
                                if 'interface' in line:
                                    for ifl in ifl_ri:
                                        ifl_regex = re.compile(r"\b"+ifl+r"\b")
                                        if re.findall(ifl_regex, line):
                                            print(line)
                                if 'interface' not in line:
                                    print(line)
                            if 'protocols bgp' in line:
                                if 'protocols bgp group' not in line:
                                    print(line)
                                if 'neighbor' not in line:
                                    for group in bgp_groups:
                                        if group in line:
                                            print(line)
                                if 'neighbor' in line:
                                    for neighbor in bgp_neighbors:
                                        if neighbor in line:
                                            print(line)

        print("\nIP/VPN completed.\n")


        # L2VPN
        print("\nL2VPN is starting. Please wait...\n")

        # ifl протокола l2circuit связанные с ifd
        neighbor_ifl = []
        local_switching_ifl = []
        for line in router_conf:
            if 'set protocols l2circuit neighbor' in line:
                for ifl in r_sw_vlans.keys():
                    ifl_regex = re.compile(r"\b"+ifl+r"\b")
                    if re.findall(ifl_regex, line):
                        neighbor_ifl.extend(([fields.split()[6] for fields in line.splitlines()]))
            if 'set protocols l2circuit local-switching' in line:
                if 'end-interface' in line:
                    for ifl in r_sw_vlans.keys():
                        ifl_regex = re.compile(r"\b"+ifl+r"\b")
                        if re.findall(ifl_regex, line):
                            for fields in line.splitlines():
                                local_switching_ifl.append(fields.split()[5])
                                local_switching_ifl.append(fields.split()[8])

        # Уникальные значения ifl для l2circuit neighbor
        used = set()
        neighbor_ifl = [x for x in neighbor_ifl if x not in used and (used.add(x) or True)]
        print("L2circuit neighbor ifl (old ifd):\n")
        print(neighbor_ifl, "\n")

        # local-switching ifl связанные с ifd
        print("Local-switching ifl (old ifd):\n")
        print(local_switching_ifl, "\n")

        # разделяем ifl на ifd и unit
        neighbor_ifd_unit = []
        for ifl in neighbor_ifl:
            ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
            neighbor_ifd_unit.append(ifl)

        local_switching_ifd_unit = []
        for ifl in local_switching_ifl:
            ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
            local_switching_ifd_unit.append(ifl)

        # выводим конфигурацию l2circuit neighbor для ifd с заменой его имени на новое
        print("\nConfiguration l2circuit neighbor (new ifd):\n")
        for line in router_conf:
            for unit in neighbor_ifd_unit:
                if unit in line:
                    print(line.replace(unit.split()[0], ifd_target))
        for line in router_conf:
            for unit in neighbor_ifl:
                unit = ' ' + unit + ' '
                if unit in line:
                    if 'neighbor ' + ip_target_neighbor not in line:
                        print(line.replace(unit.split('.')[0], ' ' + ifd_target))
                    if 'neighbor ' + ip_target_neighbor in line:
                        print(line.replace(unit.split('.')[0], ' ' + ifd_target), "// !!! Needs to change !!!")

        # выводим конфигурацию l2circuit local-switching для ifd с заменой его имени на новое
        print("\nConfiguration l2circuit local-switching (new ifd):\n")
        for line in router_conf:
            for unit in local_switching_ifd_unit:
                if unit in line:
                    print(line.replace(unit.split()[0], ifd_target))

        # если "front" и "end" ifl local-switching на одном ifd заменяем его имя на новое
        local_switching_list = []
        for line in router_conf:
            for unit in local_switching_ifl:
                unit = ' ' + unit
                if line.endswith(unit):
                    local_switching_list.append(line)
        for i in local_switching_list:
            if 'set protocols l2circuit local-switching interface ' + ifd_source in i:
                print(i.replace(ifd_source, ifd_target))
            local_switching_ifl_description = []
        for line in router_conf:
            for unit in local_switching_ifl:
                if 'set protocols l2circuit local-switching interface ' + ifd_source in line:
                    if 'end-interface interface ' + ifd_source in line:
                        local_switching_ifl_description.extend(([fields.split()[5] for fields in
                                                                     line.splitlines()]))
        used = set()
        local_switching_ifl_description = [x for x in local_switching_ifl_description
                                           if x not in used and (used.add(x) or True)]
        for line in router_conf:
            for unit in local_switching_ifl_description:
                if 'set protocols l2circuit local-switching interface ' + ifd_source in line:
                    if unit in line:
                        if 'description' in line:
                            print(line.replace('set protocols l2circuit local-switching interface ' + ifd_source,
                                                    'set protocols l2circuit local-switching interface ' + ifd_target))

        # если local-switching на разных ifd делаем neighbor к новому маршрутизатору
        # для front-interface в local-switching
        local_switching_front_ifl = []
        for line in router_conf:
            for unit in local_switching_ifl:
                unit = ' ' + unit + ' '
                if unit in line:
                    if 'set protocols l2circuit local-switching interface ' + ifd_source in line:
                        if 'end-interface interface ' in line:
                            if 'end-interface interface ' + ifd_source not in line:
                                local_switching_front_ifl.append(unit)
        used = set()
        local_switching_front_ifl = [x for x in local_switching_front_ifl if x not in used and (used.add(x) or True)]
        for line in router_conf:
            for unit in local_switching_front_ifl:
                if unit in line:
                    if 'set protocols l2circuit local-switching interface ' + ifd_source in line:
                        if 'description' in line:
                            print(line.replace('set protocols l2circuit local-switching interface ' + ifd_source,
                                                    'set protocols l2circuit neighbor ' + ip_source_neighbor
                                                    + ' interface ' + ifd_target))
        for unit in local_switching_front_ifl:
            print('set protocols l2circuit neighbor ' + ip_source_neighbor + ' interface ' + ifd_target + '.'
                    + unit.split('.')[1] + 'ignore-mtu-mismatch')
            print('set protocols l2circuit neighbor ' + ip_source_neighbor + ' interface ' + ifd_target + '.'
                    + unit.split('.')[1] + 'virtual-circuit-id ' + unit.split('.')[1])

        # для end-interface в local-switching
        for line in router_conf:
            for unit in local_switching_ifl:
                unit = ' ' + unit
                if unit in line:
                    if 'end-interface interface' + unit in line:
                        print('set protocols l2circuit neighbor ' + ip_source_neighbor + ' interface ' + ifd_target
                                + '.' + unit.split('.')[1] + ' ignore-mtu-mismatch')
                        print('set protocols l2circuit neighbor ' + ip_source_neighbor + ' interface ' + ifd_target
                                + '.' + unit.split('.')[1] + ' virtual-circuit-id ' + unit.split('.')[1])

        print("\nL2VPN completed.\n")

        sys.stdout = original


    # Формирование списка VLAN для нового коммутатора агрегации
    with open(target_switch_conf, 'w') as target_switch_conf:
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, target_switch_conf)

        for line in switch_conf:
            if 'set vlans' and 'vlan-id' in line:
                vlan = int(line.split()[-1])
                for vlan_id in vlans:
                    if vlan_id == vlan:
                        target_switch_conf.write(line + '\n')

        sys.stdout = original


    # изменения на маршрутизаторе источнике для local-switching ifl в сторону нового neighbor
    with open(source_router_conf, 'w') as source_router_conf:
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, source_router_conf)

        local_switching_front_ifl_dict = {}
        for line in router_conf:
            for unit in local_switching_ifl:
                if not line.startswith('set protocols l2circuit local-switching interface ' + ifd_source):
                    if 'end-interface interface ' + ifd_source in line:
                        unit = ' ' + unit + ' '
                        if unit in line:
                            for ifl in r_sw_vlans.keys():
                                ifl_regex = re.compile(r"\b"+ifl+r"\b")
                                match_ifl = re.search(ifl_regex, line).group(0)
                                local_switching_front_ifl_dict.update({unit: match_ifl})
        for line in router_conf:
            for key in local_switching_front_ifl_dict.keys():
                if key in line:
                    if 'description' in line:
                        print(line.replace('set protocols l2circuit local-switching interface',
                                           'set protocols l2circuit neighbor ' + ip_target_neighbor + ' interface'))
        local_switching_end_ifl_dict = {}
        for line in router_conf:
            for unit in local_switching_ifl:
                unit = ' ' + unit
                if line.startswith('set protocols l2circuit local-switching interface ' + ifd_source):
                    if 'end-interface interface ' + ifd_source not in line:
                        if 'end-interface interface' + unit in line:
                            for ifl in r_sw_vlans.keys():
                                try:
                                    ifl_regex = re.compile(r"\b"+ifl+r"\b")
                                    match_ifl = re.search(ifl_regex, line).group(0)
                                    local_switching_end_ifl_dict.update({unit: match_ifl})
                                except AttributeError:
                                    match_ifl = None
        for k, v in local_switching_front_ifl_dict.items():
            print('set protocols l2circuit neighbor ' + ip_target_neighbor + ' interface' + k + 'virtual-circuit-id '
                  + v.split('.')[1])
            print('set protocols l2circuit neighbor ' + ip_target_neighbor + ' interface' + k + 'ignore-mtu-mismatch')
            print('deactivate protocols l2circuit neighbor ' + ip_target_neighbor + ' interface' + k)
        for k, v in local_switching_end_ifl_dict.items():
            print('set protocols l2circuit neighbor ' + ip_target_neighbor + ' interface' + k + ' virtual-circuit-id '
                  + v.split('.')[1])
            print('set protocols l2circuit neighbor ' + ip_target_neighbor + ' interface' + k + ' ignore-mtu-mismatch')
            print('deactivate protocols l2circuit neighbor ' + ip_target_neighbor + ' interface' + k)


        sys.stdout = original
        # Only on stdout


if __name__ == "__main__":
    main()