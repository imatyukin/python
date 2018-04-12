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


# Конфигуационные файлы коммутатора и маршрутизатора
# show | display set | save /var/tmp/switch.conf
switch_conf = 'spbr-astk1.conf'
switch_conf = codecs.open(switch_conf, 'r', encoding='utf-8', errors='ignore').read().splitlines()
# show | display set | save /var/tmp/router.conf
router_conf = 'spbr-ar2.conf'
router_conf = codecs.open(router_conf, 'r', encoding='utf-8', errors='ignore').read().splitlines()

# Файл вывода результатов
f_out = 'a.out'

# Интерфейсы коммутатора
# в сторону коммутаторов связанных с маршрутизатором
switch_to_sw_ifd = ' ge-0/0/2 ', ' ge-0/0/3 '

# Интерфейс маршрутизатора в сторону коммутатора
router_ifd = ' xe-9/3/3 ',

# Интерфейс нового маршрутизатора
ifd_target = 'ae0'

def main():
    # Объявление глобальных переменных
    global switch_conf, router_conf, f_out
    global switch_to_sw_ifd, router_ifd

    with open(f_out, 'w') as f_out:
        # This will go to stdout and the file
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, f_out)

        # Находим все VLANы на физ. интерфейсах (ifd) коммутатора
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
        # print(sw_vlans)

        # Находим VLANы на физ. интерфейсах (ifd) маршрутизатора
        # Создаём словарь r_vlans {ifl(ifd.unit): [VLAN]}
        r_vlans = {}
        for line in router_conf:
            for ifd in router_ifd:
                if 'set interfaces' + ifd in line and 'unit' in line:
                    # Для vlan-id
                    if ' vlan-id ' in line and 'input-vlan-map' not in line:
                        line = str(line).split(' ')
                        key = line[2].strip() + '.' + line[4].strip()
                        value = line[6].strip()
                        value = int(value.split()[-1])
                        if key not in r_vlans:
                            r_vlans.setdefault(key, []).append(value)
                        else:
                            r_vlans.key = value
                    # Для QinQ
                    elif 'vlan-tags outer' in line:
                        line = str(line).split(' ')
                        key = line[2].strip() + '.' + line[4].strip()
                        value = line[7].strip()
                        value = int(value.split()[-1])
                        if key not in r_vlans:
                            r_vlans.setdefault(key, []).append(value)
                        else:
                            r_vlans.key = value
        # print(r_vlans)

        # Находим общие значения двух словарей (VLANы) и создаём словарь r_sw_vlans {ifl(ifd.unit): [VLAN]}
        r_sw_vlans = {}
        for sw_k, sw_v in sw_vlans.items():
            for r_k, r_v in r_vlans.items():
                for i in sw_v:
                    for j in r_v:
                        if i == j:
                            r_v = ''.join(str(e) for e in r_v)
                            if r_k not in r_sw_vlans:
                                r_sw_vlans.setdefault(r_k, []).append(int(r_v))
                            else:
                                r_sw_vlans.r_k = int(r_v)
        # print(r_sw_vlans)

        # INET
        print("\nINTERNET is starting. Please wait...\n")
        # Находим все логические интерфейсы (ifl) c family inet, связанные с физическим интерфейсом (ifd)
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
            ifl_regex = re.compile(ifl+'$')
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
        for ifl in r_sw_vlans.keys():
            ifl_regex = re.compile(ifl + '$')
            for line in router_conf:
                if 'routing-instances' in line:
                    if 'protocols vpls' in line:
                        if 'interface' in line:
                            if re.findall(ifl_regex, line):
                                ifl_ri_vpls.extend(([fields.split()[8] for fields in line.splitlines()]))
        # print(ifl_ri_vpls)

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
                                        ifl_regex = re.compile(ifl + '$')
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


if __name__ == "__main__":
    main()