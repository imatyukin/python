#!/usr/bin/env python3
# Вывод конфигурации настроек IP/VPN связанных с интерфейсом маршрутизатора
import sys
import codecs
import re
import netaddr


class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # The output to be visible immediately

    def flush(self):
        for f in self.files:
            f.flush()


# Файл источник: show | display set | save /var/tmp/router.conf
router_conf = 'spbr-ar1.conf'
# Целевой файл: load set /var/tmp/router
target_router_conf = 'spbr-ar1'

# Объявление регулярных выражений и переменных
ifl_regex = re.compile('xe-2/3/0.\w+')

with open(target_router_conf, 'w') as target_router_conf:
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, target_router_conf)

    router_conf = codecs.open(router_conf, 'r', encoding='utf-8', errors='ignore').read()
    router_conf_line = router_conf.splitlines()

    # Логические интерфейсы (ifl) находящиеся в routing-instances (ri) и связанные с физическим интерфейсом (ifd)
    ri_ifl = []
    for conf_line in router_conf_line:
        if 'routing-instances' in conf_line:
            if 'protocols' not in conf_line:
                if 'interface' in conf_line:
                    if re.findall(ifl_regex, conf_line):
                        ri_ifl.extend(([fields.split()[4] for fields in conf_line.splitlines()]))
    # print(len(ri_ifl))
    # ifl связанные с VPLS
    ri_vpls_ifl = []
    for conf_line in router_conf_line:
        if 'routing-instances' in conf_line:
            if 'protocols vpls' in conf_line:
                if 'interface' in conf_line:
                    if re.findall(ifl_regex, conf_line):
                        ri_vpls_ifl.extend(([fields.split()[8] for fields in conf_line.splitlines()]))
    # print(len(ri_vpls_ifl))
    # Исключаем ifl связанные с VPLS
    ri_ifl = [x for x in ri_ifl if x not in ri_vpls_ifl]
    # print(len(ri_ifl))

    # разделяем ifl на ifd и unit
    ifd_unit = []
    for ifl in ri_ifl:
        ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
        ifd_unit.append(ifl)

    # выводим конфигурацию ifl и CoS для ifd
    for conf_line in router_conf_line:
        for ifl in ifd_unit:
            if ifl in conf_line:
                print(conf_line)

    # Словарь ifls : routing-instances
    ifl_ri_dic = {}
    for conf_line in router_conf_line:
        for ifl in ri_ifl:
            if 'routing-instances' in conf_line:
                if 'protocols' not in conf_line:
                    if 'interface' in conf_line:
                        if ifl in conf_line:
                            match_vrf = list([fields.split()[2] for fields in conf_line.splitlines()])[0]
                            ifl_ri_dic.update({ifl: match_vrf})

    # Уникальные имена routing-instances
    ifl_ri_list = []
    ifl_ri_list.append(ifl_ri_dic.copy())
    ri_names = list(set(val for dic in ifl_ri_list for val in dic.values()))

    # Словарь ifls : ip-addresses
    ifl_ip_addr_dic = {}
    for conf_line in router_conf_line:
        for unit in ifd_unit:
            if unit in conf_line:
                if 'family inet address' in conf_line:
                    match_ip_addr = list([fields.split()[8] for fields in conf_line.splitlines()])[0]
                    ifl = unit.split(' ')[1] + '.' + unit.split(' ')[3]
                    ifl_ip_addr_dic.update({ifl: match_ip_addr})

    # Словарь static-routes : routing-instances
    static_routes_ri_dic = {}
    for conf_line in router_conf_line:
        if 'routing-instances' in conf_line:
            if 'routing-options static' in conf_line:
                for vrf in ri_names:
                    if vrf in conf_line:
                        if 'next-hop' in conf_line:
                            match_static_route = list([fields.split()[6] for fields in conf_line.splitlines()])[0]
                            static_routes_ri_dic.update({match_static_route: vrf})

    # Словарь static-routes : next-hops для routing-instances
    static_routes_nh_dic = {}
    for conf_line in router_conf_line:
        if 'routing-instances' in conf_line:
            if 'routing-options static' in conf_line:
                for vrf in ri_names:
                    if vrf in conf_line:
                        if 'next-hop' in conf_line:
                            for static_route, routing_instance in static_routes_ri_dic.items():
                                if static_route in conf_line:
                                    match_next_hop = list([fields.split()[8] for fields in
                                                               conf_line.splitlines()])[0]
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
    for conf_line in router_conf_line:
        if 'routing-instances' in conf_line:
            for vrf in ri_names:
                if vrf in conf_line:
                    if 'protocols bgp' in conf_line:
                        if 'local-address' in conf_line:
                            ip_addresses = [ip_addr.split('/')[0] for ip_addr in list(ifl_ip_addr_dic.values())]
                            for ip_addr in ip_addresses:
                                if ip_addr in conf_line:
                                    for fields in conf_line.splitlines():
                                        bgp_neighbors.append(fields.split()[8])
                                        bgp_groups.append(fields.split()[6])

    # Уникальные значения bgp-groups и bgp-neighbors
    used = set()
    bgp_neighbors = [x for x in bgp_neighbors if x not in used and (used.add(x) or True)]
    used = set()
    bgp_groups = [x for x in bgp_groups if x not in used and (used.add(x) or True)]

    # Вывод настроек routing-instances
    for conf_line in router_conf_line:
        if 'routing-instances' in conf_line:
            for vrf in ri_names:
                if vrf in conf_line:
                    if 'routing-options static' in conf_line:
                        for static_route, next_hop in static_routes_dic.items():
                            if static_route in conf_line:
                                print(conf_line)
                    if 'routing-options static' not in conf_line:
                        if 'protocols bgp' not in conf_line:
                            if 'interface lo0' in conf_line:
                                print(conf_line)
                            if 'interface' in conf_line:
                                if re.findall(ifl_regex, conf_line):
                                    print(conf_line)
                            if 'interface' not in conf_line:
                                print(conf_line)
                        if 'protocols bgp' in conf_line:
                            if 'protocols bgp group' not in conf_line:
                                print(conf_line)
                            if 'neighbor' not in conf_line:
                                for group in bgp_groups:
                                    if group in conf_line:
                                        print(conf_line)
                            if 'neighbor' in conf_line:
                                for neighbor in bgp_neighbors:
                                    if neighbor in conf_line:
                                        print(conf_line)

    sys.stdout = original
