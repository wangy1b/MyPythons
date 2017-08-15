# encoding=utf-8

'''命令行火车票查看器

Usage:
    tickets [-dgktz] <from> <to> <date>

Options:
    -h, --help 查看帮助
    -d         动车
    -g         高铁
    -k         快速
    -t         特快
    -z         直达

Examples:
    tickets 上海 北京 2016-10-10
    tickets -dg 成都 南京 2016-10-10
'''
import re
import requests
from pprint import pprint
from prettytable import PrettyTable
from colorama import Fore



from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def stations():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9021'
    response = requests.get(url, verify=False)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    dict = {}
    for item in stations:
        dict[item[0]]=item[1]
    #pprint(dict)
    return  dict

def wyb():
    fname= input('请输入开始车站:')#'北京'
    tname = input('请到达开始车站:')#'上海'
    gdate = input('请输入购票日期:') #'2017-08-04'
    option=input('请选择车次类型(dhkdz):').upper() #'td'
    options = [i for i in option]
    stations_name=stations() #根据代码获取站名
    stations_code={v:k for k,v in stations_name.items()} #根据站名获取代码
    from_station = stations_name.get(fname,None)
    to_station = stations_name.get(tname,None)
    date = gdate
    # 构建URL

    url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)
    #print(url)
    #     https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date=2017-08-03&leftTicketDTO.from_station=UUH&leftTicketDTO.to_station=ENH&purpose_codes=ADULT
    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    raw_trains=r.json()['data']['result']
    pt=PrettyTable()
    pt._set_field_names('车次 出发站 到达站 出发时间 到达时间 历时 一等座 二等座 软卧 硬卧 硬座 无座'.split())
    #pt._set_field_names('车次 车站 时间 历时 一等座 二等座 软卧 硬卧 硬座 无座'.split())
    for train in raw_trains:
        date_list=train.split('|')
        train_no=date_list[3]
        initial = train_no[0],
        initl=''.join(j for j in initial if j.isalpha())
        if not options or initl in options:
            from_station_code=date_list[6]
            to_station_code=date_list[7]
            from_station_name=stations_code.get(from_station_code,None)
            to_station_name=stations_code.get(to_station_code,None)
            start_time=date_list[8]
            arrive_time=date_list[9]
            time_duration=date_list[10]
            first_class_seat=date_list[31] or '--'
            second_class_seat=date_list[30] or '--'
            soft_sleep=date_list[23] or '--'
            hard_sleep=date_list[28] or '--'
            hard_seat=date_list[29] or '--'
            no_seat=date_list[33] or '--'
            pt.add_row([train_no,
                        Fore.GREEN + from_station_name + Fore.RESET,
                        Fore.RED + to_station_name + Fore.RESET,
                        Fore.GREEN + start_time + Fore.RESET,
                        Fore.RED + arrive_time + Fore.RESET,
                        time_duration,
                        first_class_seat,
                        second_class_seat,
                        soft_sleep,
                        hard_sleep,
                        hard_seat,
                        no_seat])
            '''
          pt.add_row([train_no,
                    '\n'.join([Fore.GREEN + from_station_name + Fore.RESET,Fore.RED+to_station_name + Fore.RESET]),
                    '\n'.join([Fore.GREEN + start_time+ Fore.RESET,Fore.RED+ arrive_time + Fore.RESET ]),
                    time_duration,
                    first_class_seat,
                    second_class_seat,
                    soft_sleep,
                    hard_sleep,
                    hard_seat,
                    no_seat])'''
    print(pt)


wyb()