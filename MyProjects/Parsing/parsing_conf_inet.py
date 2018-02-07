#!/usr/bin/env python3
# Перенос интерфейсов маршрутизатора находящихся в глобальной таблице на другой маршрутизатор
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
ifd_source = 'xe-2/3/0'
ifl_regex = re.compile('xe-2/3/0.\w+')

with open(target_router_conf, 'w') as target_router_conf:
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, target_router_conf)

    router_conf = codecs.open(router_conf, 'r', encoding='utf-8', errors='ignore').read()
    router_conf_line = router_conf.splitlines()

    # Находим все логические интерфейсы (ifl) c family inet, связанные с физическим интерфейсом (ifd)
    ifl_inet_ifd = []
    for conf_line in router_conf_line:
        if 'interfaces' in conf_line:
            if ifd_source in conf_line:
                if 'unit' in conf_line:
                    if 'family inet address' in conf_line:
                        unit = str([fields.split()[4] for fields in conf_line.splitlines()])
                        ifl = ifd_source + '.' + unit[2:-2]
                        ifl_inet_ifd.append(ifl)

    # Оставляем только уникальные значения ifl
    used = set()
    ifl_inet_ifd = [x for x in ifl_inet_ifd if x not in used and (used.add(x) or True)]

    # Находим ifl находящиеся в routing-instances (ri) и связанные с физическим интерфейсом (ifd)
    ifl_ri_ifd = []
    for conf_line in router_conf_line:
        if 'routing-instances' in conf_line:
            if 'interface' in conf_line:
                if 'protocols' not in conf_line:
                    if re.findall(ifl_regex, conf_line):
                        ifl_ri_ifd.extend(([fields.split()[4] for fields in conf_line.splitlines()]))

    # Находим ifl связанные с GRT путём исключения ifl связанных с routing-instances
    ifl_grt = [x for x in ifl_inet_ifd if x not in ifl_ri_ifd]

    # разделяем ifl на ifd и unit
    ifd_unit = []
    for ifl in ifl_grt:
        ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
        ifd_unit.append(ifl)

    '''
    # выводим конфигурацию ifl и CoS для ifd (!!! проблема с deactivate interfaces !!!)
    for conf_line in router_conf_line:
        for ifl in ifd_unit:
            if ifl in conf_line:
                print(conf_line)
    '''
    # Словарь ip-addresses : ifls
    ip_addr_ifl_dic = {}
    for conf_line in router_conf_line:
        for unit in ifd_unit:
            if unit in conf_line:
                if 'family inet address' in conf_line:
                    match_ip_addr = list([fields.split()[8] for fields in conf_line.splitlines()])[0]
                    ifl = unit.split(' ')[1] + '.' + unit.split(' ')[3]
                    ip_addr_ifl_dic.update({match_ip_addr: ifl})

    # Список static-routes для GRT
    static_routes_list = []
    for conf_line in router_conf_line:
        if 'routing-instances' not in conf_line:
            if 'routing-options static route' in conf_line:
                static_routes_list.extend(([fields.split()[4] for fields in conf_line.splitlines()]))

    # Оставляем только уникальные значения static-routes
    used = set()
    static_routes_list = [x for x in static_routes_list if x not in used and (used.add(x) or True)]

    # Словарь static-routes : next-hops для GRT
    static_routes_nh_dic = {}
    for conf_line in router_conf_line:
        if 'routing-instances' not in conf_line:
            if 'routing-options static route' in conf_line:
                if 'next-hop' in conf_line:
                    for static_route in static_routes_list:
                        if static_route in conf_line:
                            match_next_hop = list([fields.split()[6] for fields in conf_line.splitlines()])[0]
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
    for conf_line in router_conf_line:
        if 'routing-instances' not in conf_line:
            if 'protocols bgp' in conf_line:
                if 'local-address' in conf_line:
                    ip_addresses = [ip_addr.split('/')[0] for ip_addr in list(ip_addr_ifl_dic.keys())]
                    for ip_addr in ip_addresses:
                        if ip_addr in conf_line:
                            for fields in conf_line.splitlines():
                                bgp_neighbors.append(fields.split()[6])
                                bgp_groups.append(fields.split()[4])

    # Уникальные значения bgp-groups и bgp-neighbors
    used = set()
    bgp_neighbors = [x for x in bgp_neighbors if x not in used and (used.add(x) or True)]
    used = set()
    bgp_groups = [x for x in bgp_groups if x not in used and (used.add(x) or True)]

    # Вывод настроек
    for conf_line in router_conf_line:
        if 'routing-instances' not in conf_line:
            if 'routing-options static' in conf_line:
                for static_route, next_hop in static_routes_dic.items():
                    if static_route in conf_line:
                        print(conf_line)
            if 'protocols bgp' in conf_line:
                if 'neighbor' not in conf_line:
                    for group in bgp_groups:
                        if group in conf_line:
                            print(conf_line)
                if 'neighbor' in conf_line:
                    for neighbor in bgp_neighbors:
                        if neighbor in conf_line:
                            print(conf_line)

    sys.stdout = original