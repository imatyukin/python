#!/usr/bin/env python3
# Перенос L2VPN с одного интерфейса маршрутизатора на другой маршрутизатор
import sys
import codecs
import re


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
# Целевые файлы: load set /var/tmp/router.conf
source_router_conf = 'spbr-ar1'
target_router_conf = 'spbr-ar2'

with open(target_router_conf, 'w') as target_router_conf:
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, target_router_conf)

    router_conf = codecs.open(router_conf, 'r', encoding='utf-8', errors='ignore').read()
    router_conf_line = router_conf.splitlines()

    # Объявление регулярных выражений и переменных
    ifl_regex = re.compile('xe-2/1/0.\w+')
    ifd_source = 'xe-2/1/0'
    ifd_target = 'xe-0/0/2'
    ip_source_neighbor = '87.226.134.133'
    ip_target_neighbor = '95.167.88.60'
    # Интерфейсы, которые переносить не нужно
    ifl_except = ' xe-9/1/0 unit 4700 ', ' xe-9/1/0 unit 4800 ', ' xe-9/1/0 unit 4900 ', \
                 ' xe-9/1/0 unit 11000 ', ' xe-9/1/0 unit 14700 '
    ifl_except_short = 'xe-9/1/0.4700', 'xe-9/1/0.4800', 'xe-9/1/0.4900', \
                       'xe-9/1/0.11000', 'xe-9/1/0.14700'

    # Логические интерфейсы (ifl) протокола l2circuit связанные с физическим интерфейсом (ifd)
    neighbor_ifl = []
    local_switching_ifl = []
    for conf_line in router_conf_line:
        if 'set protocols l2circuit' in conf_line:
            if 'set protocols l2circuit neighbor' in conf_line:
                if re.findall(ifl_regex, conf_line):
                    neighbor_ifl.extend(([fields.split()[6] for fields in conf_line.splitlines()]))
            if 'set protocols l2circuit local-switching' in conf_line:
                if 'end-interface' in conf_line:
                    if re.findall(ifl_regex, conf_line):
                        for fields in conf_line.splitlines():
                            local_switching_ifl.append(fields.split()[5])
                            local_switching_ifl.append(fields.split()[8])

    # Уникальные значения ifl для l2circuit neighbor
    used = set()
    neighbor_ifl = [x for x in neighbor_ifl if x not in used and (used.add(x) or True)]

    # local-switching ifl связанные с ifd
    local_switching_ifl_ifd = list(filter(ifl_regex.search, local_switching_ifl))

    # ifl других ifd с которыми настроен local-switching
    # local_switching_ifl_filtered = list(filter(lambda i: not ifl_regex.search(i), local_switching_ifl))

    # разделяем ifl на ifd и unit
    neighbor_ifd_unit = []
    for ifl in neighbor_ifl:
        ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
        neighbor_ifd_unit.append(ifl)

    local_switching_ifd_unit = []
    for ifl in local_switching_ifl_ifd:
        ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
        local_switching_ifd_unit.append(ifl)

    # выводим конфигурацию l2circuit neighbor для ifd с заменой его имени на новое
    for conf_line in router_conf_line:
        for unit in neighbor_ifd_unit:
            if unit not in ifl_except:
                if unit in conf_line:
                    print(conf_line.replace(unit.split( )[0], ifd_target))
    for conf_line in router_conf_line:
        for unit in neighbor_ifl:
            if unit not in ifl_except_short:
                unit = ' ' + unit + ' '
                if unit in conf_line:
                    print(conf_line.replace(unit.split('.')[0], ' ' + ifd_target))

    # выводим конфигурацию l2circuit local-switching для ifd с заменой его имени на новое
    for conf_line in router_conf_line:
        for unit in local_switching_ifd_unit:
            if unit not in ifl_except:
                if unit in conf_line:
                    print(conf_line.replace(unit.split( )[0], ifd_target))

    # если "front" и "end" ifl local-switching на одном ifd заменяем его имя на новое
    local_switching_list = []
    for conf_line in router_conf_line:
        for unit in local_switching_ifl_ifd:
            unit = ' ' + unit
            if conf_line.endswith(unit):
                local_switching_list.append(conf_line)
    for i in local_switching_list:
        if 'set protocols l2circuit local-switching interface ' + ifd_source in i:
            print(i.replace(ifd_source, ifd_target))
        local_switching_ifl_description = []
    for conf_line in router_conf_line:
        for unit in local_switching_ifl_ifd:
            if unit not in ifl_except_short:
                if 'set protocols l2circuit local-switching interface ' + ifd_source in conf_line:
                    if 'end-interface interface ' + ifd_source in conf_line:
                        local_switching_ifl_description.extend(([fields.split()[5] for fields in
                                                                 conf_line.splitlines()]))
    used = set()
    local_switching_ifl_description = [x for x in local_switching_ifl_description
                                       if x not in used and (used.add(x) or True)]
    for conf_line in router_conf_line:
        for unit in local_switching_ifl_description:
            if 'set protocols l2circuit local-switching interface ' + ifd_source in conf_line:
                if unit in conf_line:
                    if 'description' in conf_line:
                        print(conf_line.replace('set protocols l2circuit local-switching interface ' + ifd_source,
                                                'set protocols l2circuit local-switching interface ' + ifd_target))

    # если local-switching на разных ifd делаем neighbor к новому маршрутизатору
    # для front-interface в local-switching
    local_switching_front_ifl = []
    for conf_line in router_conf_line:
        for unit in local_switching_ifl_ifd:
            if unit not in ifl_except:
                unit = ' ' + unit + ' '
                if unit in conf_line:
                    if 'set protocols l2circuit local-switching interface ' + ifd_source in conf_line:
                        if 'end-interface interface ' in conf_line:
                            if 'end-interface interface ' + ifd_source not in conf_line:
                                local_switching_front_ifl.append(unit)
    used = set()
    local_switching_front_ifl = [x for x in local_switching_front_ifl if x not in used and (used.add(x) or True)]
    for conf_line in router_conf_line:
        for unit in local_switching_front_ifl:
            if unit in conf_line:
                if 'set protocols l2circuit local-switching interface ' + ifd_source in conf_line:
                    if 'description' in conf_line:
                        print(conf_line.replace('set protocols l2circuit local-switching interface ' + ifd_source,
                                                'set protocols l2circuit neighbor ' + ip_source_neighbor
                                                + ' interface ' + ifd_target))
    for unit in local_switching_front_ifl:
        if unit not in ifl_except:
            print('set protocols l2circuit neighbor ' + ip_source_neighbor + ' interface ' + ifd_target + '.'
                  + unit.split('.')[1] + 'ignore-mtu-mismatch')
            print('set protocols l2circuit neighbor ' + ip_source_neighbor + ' interface ' + ifd_target + '.'
                  + unit.split('.')[1] + 'virtual-circuit-id ' + unit.split('.')[1])

    # для end-interface в local-switching
    for conf_line in router_conf_line:
        for unit in local_switching_ifl_ifd:
            if unit not in ifl_except_short:
                unit = ' ' + unit
                if unit in conf_line:
                    if 'end-interface interface' + unit in conf_line:
                        print('set protocols l2circuit neighbor ' + ip_source_neighbor + ' interface ' + ifd_target
                              + '.' + unit.split('.')[1] + ' ignore-mtu-mismatch')
                        print('set protocols l2circuit neighbor ' + ip_source_neighbor + ' interface ' + ifd_target
                              + '.' + unit.split('.')[1] + ' virtual-circuit-id ' + unit.split('.')[1])

    sys.stdout = original

# изменения на маршрутизаторе источнике для local-switching ifl в сторону нового neighbor

with open(source_router_conf, 'w') as source_router_conf:
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, source_router_conf)

    local_switching_front_ifl_dict = {}
    for conf_line in router_conf_line:
        for unit in local_switching_ifl:
            if not conf_line.startswith('set protocols l2circuit local-switching interface ' + ifd_source):
                if 'end-interface interface ' + ifd_source in conf_line:
                    unit = ' ' + unit + ' '
                    if unit in conf_line:
                        match_ifl = re.search(ifl_regex, conf_line).group(0)
                        local_switching_front_ifl_dict.update({unit : match_ifl})
    for conf_line in router_conf_line:
        for key in local_switching_front_ifl_dict.keys():
            if key in conf_line:
                if 'description' in conf_line:
                    print(conf_line.replace('set protocols l2circuit local-switching interface',
                                            'set protocols l2circuit neighbor ' + ip_target_neighbor + ' interface'))
    local_switching_end_ifl_dict = {}
    for conf_line in router_conf_line:
        for unit in local_switching_ifl:
            unit = ' ' + unit
            if conf_line.startswith('set protocols l2circuit local-switching interface ' + ifd_source):
                if 'end-interface interface ' + ifd_source not in conf_line:
                    if 'end-interface interface' + unit in conf_line:
                        match_ifl = re.search(ifl_regex, conf_line).group(0)
                        local_switching_end_ifl_dict.update({unit: match_ifl})
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
