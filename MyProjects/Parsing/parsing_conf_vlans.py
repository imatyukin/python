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


# Файл вывода результатов
f_out = 'a.out'

# VLAN'ы на существующем коммутаторе агрегации (show vlan)
ag_switch_vlans = 'spbr-asw5_vlans.conf'
ag_switch_vlans = codecs.open(ag_switch_vlans, 'r', encoding='utf-8', errors='ignore').read().splitlines()
# Интерфейс существующего коммутатора агрегации в сторону коммутатора доступа (sh run int Gi3/17)
int_ag_switch = 'spbr-asw5_interface.conf'
int_ag_switch = codecs.open(int_ag_switch, 'r', encoding='utf-8', errors='ignore').read().splitlines()

# Конфигуационные файлы существующего маршрутизатора
# show | display set | save /var/tmp/router.conf
router_conf = 'spbr-ar2.conf'
router_conf = codecs.open(router_conf, 'r', encoding='utf-8', errors='ignore').read().splitlines()

# Интерфейсы существующего маршрутизатора в сторону существующего коммутатора агрегации
router_ifd = ['xe-0/0/2', 'xe-4/1/2', 'xe-5/3/0', 'xe-8/0/0']

# Конфигуационные файлы нового коммутатора агрегации
# show | display set | save /var/tmp/switch.conf
switch_conf = 'spbr-astk3.conf'
switch_conf = codecs.open(switch_conf, 'r', encoding='utf-8', errors='ignore').read().splitlines()

# Интерфейс нового маршрутизатора
ifd_target = 'xe-0/2/3'

ip_source_neighbor = '95.167.88.60'
ip_target_neighbor = '213.59.207.99'

# Целевые файлы: load set /var/tmp/switch
target_switch_conf = 'spbr-astk3'

def main():
    # Объявление глобальных переменных
    global f_out, ag_switch_vlans, int_ag_switch, router_conf, router_ifd, switch_conf, ifd_source, ifd_target, \
        ip_source_neighbor, ip_target_neighbor, target_switch_conf

    with open(f_out, 'w') as f_out:
        # This will go to stdout and the file
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, f_out)

        # Находим все VLANы на коммутаторе агрегации
        # Создаём словарь ag_sw_vlan_name {VLAN: [Name]}
        ag_sw_vlan_name = {}
        for line in ag_switch_vlans:
            vlan_id = int(line.split()[0])
            vlan_name = line.split()[1]
            ag_sw_vlan_name.update({vlan_id: vlan_name})
        #print(ag_sw_vlan_name)

        # Находим allowed vlan на коммутаторе агрегации в сторону коммутатора доступа
        # Создаём список allowed_vlan [VLANs]
        allowed_vlan = []
        for line in int_ag_switch:
            if 'allowed vlan' in line and 'add' not in line:
                line = str(line).split(' ')
                vlans = str(line[5]).split(',')
                for vlan in vlans:
                    if '-' not in vlan:
                        allowed_vlan.append(int(vlan))
                    elif '-' in vlan:
                        vlan_range = str(vlan).split('-')
                        vlan_range = list(range(int(vlan_range[0]), int(vlan_range[1]) + 1))
                        for vlan in vlan_range:
                            allowed_vlan.append(vlan)
            if 'allowed vlan add' in line:
                line = str(line).split(' ')
                vlans = str(line[6]).split(',')
                for vlan in vlans:
                    if '-' not in vlan:
                        allowed_vlan.append(int(vlan))
                    elif '-' in vlan:
                        vlan_range = str(vlan).split('-')
                        vlan_range = list(range(int(vlan_range[0]), int(vlan_range[1]) + 1))
                        for vlan in vlan_range:
                            allowed_vlan.append(vlan)
        #print(allowed_vlan)

        # Находим общие VLAN'ы на коммутаторе доступа и агрегации
        # Создаём словарь shared_vlans {VLAN_id: [Name]}
        shared_vlans = {}
        for vlan_id in allowed_vlan:
            for vlan, name in ag_sw_vlan_name.items():
                if vlan_id == vlan:
                    shared_vlans.update({vlan_id: name})
        #print(shared_vlans)

        # Находим общие VLANы на ifd маршрутизатора
        # Создаём словарь r_ifl {ifl(ifd.unit): [VLAN]}
        r_ifl = {}
        for line in router_conf:
            for ifd in router_ifd:
                if 'set interfaces ' + ifd in line and ' unit' in line:
                    # Для vlan-id
                    if ' vlan-id ' in line and 'input-vlan-map' not in line:
                        line = str(line).split()
                        key = line[2] + '.' + line[4]
                        value = int(line[-1])
                        for vlan_id in shared_vlans.keys():
                            if value == int(vlan_id):
                                if key not in r_ifl:
                                    r_ifl.setdefault(key, []).append(value)
                                else:
                                    r_ifl.key = value
                    # Для QinQ
                    elif 'vlan-tags outer' in line:
                        line = str(line).split()
                        key = line[2] + '.' + line[4]
                        value = int(line[-1])
                        for vlan_id in shared_vlans.keys():
                            if value == int(vlan_id):
                                if key not in r_ifl:
                                    r_ifl.setdefault(key, []).append(value)
                                else:
                                    r_ifl.key = value
        print("IFLs and VLANs SPBR-AR2:")
        print(r_ifl)

        # Список совпадающих VLAN'ов для маршрутизатора и коммутатора
        vlans = []
        for k, v in r_ifl.items():
            ifd = k.split('.')[0]
            for i in router_ifd:
                if ifd == i:
                    for j in v:
                        vlans.append(j)
        print("Sorted VLANs SPBR-ASW5:")
        print(sorted(vlans))

        # Существующие VLAN'ы на новом коммутаторе агрегации
        # Создаём словарь new_ag_sw_vlans {VLAN: [Name]}
        new_ag_sw_vlans = {}
        for line in switch_conf:
            if 'set vlans' in line and 'vlan-id' in line:
                line = str(line).split(' ')
                vlan_id = int(line[4])
                vlan_name = line[2]
                new_ag_sw_vlans.update({vlan_id: vlan_name})
        #print(new_ag_sw_vlans)

        # Проверяем пересекающиеся VLAN'ы на новом коммутаторе агрегации и коммутаторе доступа
        overlapped_vlans = {}
        for vlan_id in shared_vlans.keys():
            for vlan, name in new_ag_sw_vlans.items():
                if vlan_id == vlan:
                    overlapped_vlans.update({vlan: name})
        print("Overlapped VLANs SPBR-ASTK3:")
        print(overlapped_vlans)

        # INET
        print("\nINTERNET is starting. Please wait...\n")
        # Находим все ifl c family inet, связанные с ifd
        ifl_inet = []
        for ifl in r_ifl.keys():
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
            ifl_regex = re.compile(r"\b" + ifl + r"\b")
            for line in router_conf:
                if 'routing-instances' and ' interface ' + ifl in line:
                    if 'protocols' not in line:
                        if re.findall(ifl_regex, line):
                            ifl_ri.append(ifl)
        # print(ifl_ri)

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
        for ifl in r_ifl.keys():
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

        sys.stdout = original
        # Only on stdout

        # Формирование списка VLAN'ов для нового коммутатора агрегации
        with open(target_switch_conf, 'w') as target_switch_conf:
            original = sys.stdout
            sys.stdout = Tee(sys.stdout, target_switch_conf)

            for vlan, name in ag_sw_vlan_name.items():
                target_switch_conf.write('set vlans ' + name + ' vlan-id ' + str(vlan) + '\n')

            sys.stdout = original


if __name__ == "__main__":
    main()
