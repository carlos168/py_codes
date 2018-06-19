#!/usr/bin/env python
#-*- coding:UTF-8 -*-
'''
    Description:监控项目 辅助模块
'''
import sys,os,signal,simplejson,Queue,time
from threading import Thread
from multiprocessing import Process
import get_userlist
from config import DIRS
import config
import cmdtosql
from WebsiteLib import *
from TcpLib import *
from UdpLib import *
from LogLib import *
from Progress import *
from Custom import *
from local_check import *
from Dns import *
import Ping
#from Ping import *
import datetime

import json
import urllib2,urllib

sys.path.append(config.DIRS['OMS_LIB'])
import send_alarm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
if sys.getdefaultencoding() != 'utf8':
    reload(sys)
    sys.setdefaultencoding('utf8')



def monitor_get_iteminfos():
    '''
    @Monitor 获取当前需要监控的项目信息 
    @满足时间条件和 status = 0
    '''
    try :
            time_now = cmdtosql._get_time(1)
            sql = "select * from uxin_alarm where (next_time is null or next_time <='"+time_now+"') and status = 0 "
            log_debug("monitor_get_iteminfos()执行sql语句:"+str(sql)) 
            return cmdtosql.select(sql)
    except Exception as e:
            log_error("monitor_get_iteminfos():"+str(e))

        
        
def monitor_item_nextTime(itemlist):
    '''
    @Monitor 计算项目下次监控时间
    '''
    frequency=int(itemlist[5])
    now_sec = time.time()
    midtime = int(time.mktime(time.localtime()) - now_sec) % int(frequency)        
    next_sec = time.mktime(time.localtime()) + frequency - midtime
    nextTime = time.localtime(next_sec)        
    return time.strftime('%Y-%m-%d %H:%M:%S', nextTime)

        

def monitor_item_lastTime():
    '''
    @Monitor 计算项目上次监控时间
    '''
    now_sec = time.time()
    lastTime = time.localtime(now_sec)
    return time.strftime('%Y-%m-%d %H:%M:%S', lastTime)
        
def monitor_item_updateTime(itemlist):
    '''
    @Monitor 更新项目上次下次监控时间
    '''
    itemlist = list(itemlist)
    lastTime = monitor_item_lastTime()
    nextTime = monitor_item_nextTime(itemlist)
    
    sql = "update uxin_alarm set next_time='"+nextTime+"',last_time='"+lastTime+"',lock_status='' where id="+str(itemlist[0])


#        sql1 = "update uxin_alarm set last_time='"+lastTime+"' where id="+str(itemlist[0])
#        sql_lock = "update uxin_alarm set lock_status='' where id="+str(itemlist[0])
#        log_debug("更新上次:"+str(sql))
    try:
        time.sleep(1)
        log_debug("monitor_item_update_lastTime()执行sql语句:"+str(sql))
        #cmdtosql.update(sql1)
        cmdtosql.update(sql)
        #cmdtosql.update(sql_lock)
    except Exception as e:
        log_error("monitor_item_update_lastTime():"+str(e))






#获取报警持续时间
def Caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    return date2-date1

#####################################分割线 -----------项目监控过程中 数据库操作----------- 分割线############################
def email_alarm_title(otype,name,ip,server,Reason,status,lasterr,error_start_time,oid):
    '''
    @ 格式化报警主题，内容
    '''
    monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


    content = "告警类型: "+str(status)+" \n\n"
    content1 = "告警名称: "+str(name)+" \n"
    content2 = "告警IP: "+str(ip)+" \n"
    content3 = "告警服务: "+str(server)+" \n"
    content4 = "检查时间:"+str(monitorTime)+" \n\n"
    content5 = "故障信息: \n "+str(Reason)+" \n"
    content6 = "上次故障信息: \n "+str(lasterr)+" \n"
    content7 = ""

    #清除故障首次发生时间
    if status=='RECOVERY':
        error_time=Caltime(error_start_time,monitorTime)
        sql='update uxin_alarm set error_start_time="" where id=%s' %(oid)
        content7 = "故障持续时间: "+str(error_time)+" "
        cmdtosql.update(sql)
    
    if otype=='progress':
        topTemp = "OMS监控:"+str(name)+"  IP:"+str(ip)+" 服务:"+str(Reason)+" 状态:"+str(status)+""
    else:
        topTemp = "OMS监控:"+str(name)+"  IP:"+str(ip)+" 服务:"+str(server)+" 状态:"+str(status)+""

    if status=='PROBLEM':
        if otype=='progress':
            topTemp = "OMS监控:"+str(name)+"  IP:"+str(ip)+" 服务:"+str(Reason)+" 状态:"+str(status)+""
        else:
            topTemp = "OMS监控:"+str(name)+"  IP:"+str(ip)+" 服务:"+str(server)+" 状态:"+str(status)+""
        subject = "【故障】" + "【监控源" + str(config.monitor_point) + "】"    +str(topTemp) + " " + monitorTime
        template = content + content1 + content2 + content3 + content4 + content5
    elif status=='DOWN':
        subject = "【宕机】"  + "【监控源" + str(config.monitor_point) +  "】" +str(topTemp) + " " + monitorTime
        template = content + content1 + content2 + content3 + content4 + content5
    elif status=='RECOVERY':
        if otype=='progress':
            topTemp = "OMS监控:"+str(name)+"  IP:"+str(ip)+" 服务:"+str(lasterr)+" 状态:"+str(status)+""
        else:
            topTemp = "OMS监控:"+str(name)+"  IP:"+str(ip)+" 服务:"+str(server)+" 状态:"+str(status)+""
        subject = "【恢复】" + "【监控源" + str(config.monitor_point) +  "】" +str(topTemp) + " " + monitorTime + " " +  content7
        template = content + content1 + content2 + content3 + content4 + content6 + content7


    log_info(str(subject + template))

    return subject,template        



def update_fail_count(item,fail_count):

    id=item[0]
    host=item[2]
    check_type=item[1]
    port=item[4]
    check_name=item[3]

    if fail_count != '0':
        #fail_count 清零
        sql='update uxin_alarm set fail_count="0" where id=%s' %(id)
        cmdtosql.update(sql)

        log_info("IP地址: " + str(host) + " 类型:" + str(check_type) + "  报警名:" + str(check_name) + "  检测对象:" + str(port) + " 恢复")

#检测失败后，更新这里
def update_table(item,reason):

    id=item[0]
    host=item[2]
    check_type=item[1]
    port=item[4]
    check_name=item[3]

    #更新fail_count字段+1
    sql='update uxin_alarm set fail_count=fail_count + 1 where id="%s"' %(id)
    cmdtosql.update(sql)

    #更新上次失败原因
    sql='update uxin_alarm set last_result="%s" where id=%s' %(reason,id)
    cmdtosql.update(sql)

    #更新首次失败的时间
    monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if item[21] == 'NULL' or item[21] == ''  or item[21] is None:
        sql1='update uxin_alarm set error_start_time="%s" where id=%s' %(item[11],item[0])
        cmdtosql.update(sql1)

    #更新日志
    log_info("IP地址: " + str(host) + " 类型:" + str(check_type) + "  报警名:" + str(check_name) + "  检测对象:" + str(port) + " 失败内容:" +str(reason))



def send_messages(iteminfo,reason,status):

    #根据通知对象获取通知用户
    if iteminfo[16]:
        send_list= get_userlist.get_sendto_users(iteminfo[16],iteminfo[20])
    else:
        send_list= get_userlist.get_sendto_users('1NULL',iteminfo[20])
    log_info(str(send_list) + "======send_messages=======")

    #获取报警内容
    subject ,mailContent= email_alarm_title(iteminfo[1],iteminfo[3],iteminfo[2],iteminfo[4],reason,status,iteminfo[10],iteminfo[21],iteminfo[0])

    #发送邮件
    sql='select * from uxin_alarm_email limit 1'
    mailset=cmdtosql.select(sql)
    if send_list['emaillist']:
        for i in send_list['emaillist']:
            send_alarm.send_mail(mailset[0][1],mailset[0][2],mailset[0][3],i,subject,mailContent)
            log_info(str(iteminfo[2]) +  str(status)  + ",发送邮件至" + str(i) + "成功.")

    #发送微信
    if send_list['weixinlist']:
        #合并所有微信帐号，一次发送
        wx=''
        for i in send_list['weixinlist']:
            wx = wx + '|' + str(i)

        #如果告警内容大于2000个字节,拆分发送
        if len(subject) >= 2000:
            c = 1000
            s = subject.decode('utf-8')
            try:
             d = [s[i:i+c] for i in xrange(0,len(s),c)]
            except Exception, e:
             log_info(e)
            sum=0
            for i in d:
                sum = sum + 1
                i = "【长消息 第" + str(sum) + "条】"  + str(i)
                if sum >= 2:
                    i = "[接上条]" + str(i)
                url = config.WEIXIN+"SendWeixinMsg?alarm_list=%s&alarm_content=%s" %(wx,i.encode('utf-8'))
                ss=urllib.urlopen(url).read()
                log_info(str(iteminfo[2]) +  str(status)  + ",发送微信至" + str(wx) + "结果" + str(ss))
        else:
            url = config.WEIXIN+"SendWeixinMsg?alarm_list=%s&alarm_content=%s" %(wx,subject)
            log_info(url)
            try:
                s=urllib.urlopen(url.encode('utf-8')).read()
                log_info(str(iteminfo[2]) +  str(status)  + ",发送微信至" + str(wx) + "结果" + str(s))
            except Exception, e:
                log_info(e)

    #短信告警次数限制
    if int(iteminfo[12]) - int(iteminfo[6]) >= int(iteminfo[7]) and int(iteminfo[7]) != 0:
        if status=='RECOVERY':
            pass
        else:
            log_info(str(iteminfo[2]) + "  短信告警次数上限" + " 限制 " + iteminfo[7]  )
            return True

    #判断是否需要发送短信 逻辑fail_count - Alarm_retry  大于等于 Alarm_email_num
    if int(iteminfo[12]) - int(iteminfo[8]) + 2  >= int(iteminfo[6]) and send_list['smslist']:
        sd=0

        # 相等时，不发送恢复短信
        if status=='RECOVERY' and int(iteminfo[12]) - int(iteminfo[8]) + 2  == int(iteminfo[6]):
            sd=1
            
        if sd == 0:
            for i in send_list['smslist']:
                send_alarm.send_SMS(subject,i)
                log_info(str(iteminfo[2]) + str(status) + ",发送短信至" + str(i) + "成功.")

        #判断是否需要打电话
        if int(iteminfo[12]) - int(iteminfo[8]) - int(iteminfo[6]) + 2 >= int(iteminfo[18]) and int(iteminfo[18]) != 0:
            if status=='RECOVERY':
                pass
            else:
                for i in send_list['smslist']:
                    try:
                        url="http://117.121.55.194:8888/autocall?brandid=4g&uid=11712155194&voicename=dhalert&caller=%s" %(i)
                        log_info(str(url)+'网址')
                        f = urllib2.urlopen(url, timeout=5).read()
                        log_info(str(iteminfo[2]) + str(status) + ",拨打电话至" + str(i) + str(f))
                    except Exception as e:
                        log_error("send_phone_err:"+str(e)+' '+ str(i))
                


def monitor_website_index(iteminfo):
    '''
    @Monitor 网页存活入口函数
    '''
    try:
        monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        monitor_item_updateTime(iteminfo)
        itemconfig = iteminfo
        url = iteminfo[4]
        isAlarm,result,reason,level = website_alive_check(url,itemconfig)
        
        if isAlarm == 0: #表示不报警
            #fail_count 清零
            update_fail_count(iteminfo,iteminfo[12])

            #逻辑fail_count - Alarm_retry
            if int(iteminfo[12]) - int(iteminfo[8]) >= 0:#表示上次报警了，是否恢复报警
                if iteminfo[16]:
                        send_messages(iteminfo,reason,'RECOVERY')

                #恢复 ,插入alarm_log记录
                sql="insert into uxin_alarm_log values(NULL,'%s','%s','%s','%s','RECOVERY')" %(iteminfo[2],iteminfo[3],monitorTime,iteminfo[10])
                cmdtosql.execsql(sql)
                log_info(str(sql))

        else:#报警:
            #更新fail_count  last_result数据表
            update_table(iteminfo,reason)

            #判断失败次数,需要 + 1  因为数据是最初被获取的
            if int(iteminfo[12]) + 1 >= int(iteminfo[8]):
                if iteminfo[16]:
                    send_messages(iteminfo,reason,'PROBLEM')


            #异常通知 ,插入alarm_log记录
            sql="insert into uxin_alarm_log values('','%s','%s','%s','%s','PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,reason)
            log_debug("打印日志LOG" +str(sql))
            cmdtosql.execsql(sql)
        #所有流程走完后,更新时间
        #monitor_item_updateTime(iteminfo)

    except Exception as e:
        log_error("monitor_website_index():"+str(e))         


def monitor_ping_index(iteminfo):
    '''
    @Monitor ping 入口函数
    '''
    try:
        monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        monitor_item_updateTime(iteminfo)
        ip = iteminfo[2]
        isAlarm = Ping.ping_connect_check(ip)
        #log_info(ip +  " 结果 ")
        #log_info(isAlarm)
        if isAlarm == True:
            update_fail_count(iteminfo,iteminfo[12])
            if int(iteminfo[12]) - int(iteminfo[8]) >= 0:
                if iteminfo[16]:
                    send_messages(iteminfo,' ','RECOVERY')

                sql="insert into uxin_alarm_log values(NULL,'%s','%s','%s','%s','RECOVERY')" %(iteminfo[2],iteminfo[3],monitorTime,iteminfo[10])
                log_info("打印日志LOG" +str(sql))
                cmdtosql.execsql(sql)

        else:#报警：1.ping 不通
            reason = 'DOWN'
            #更新fail_count  last_result数据表
            update_table(iteminfo,reason)
            #判断失败次数
            if int(iteminfo[12]) + 1 >= int(iteminfo[8]):
                if iteminfo[16]:
                    send_messages(iteminfo,reason,'DOWN')
            #异常通知 ,插入alarm_log记录
            sql="insert into uxin_alarm_log values('','%s','%s','%s','%s','PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,reason)
            log_debug("打印日志LOG" +str(sql))
            cmdtosql.execsql(sql)

    except Exception as e:
        log_error("monitor_ping_index():"+str(iteminfo[2]) + ' ' + str(e))


def monitor_dns_index(iteminfo):
    '''
    @Monitor dns 入口函数
    '''
    try:
        monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        monitor_item_updateTime(iteminfo)
        ip = iteminfo[2]
        isAlarm = Dns_check(ip)
        if isAlarm == True:
            update_fail_count(iteminfo,iteminfo[12])
            if int(iteminfo[12]) - int(iteminfo[8]) >= 0:
                if iteminfo[16]:
                    send_messages(iteminfo,' ','RECOVERY')
                sql="insert into uxin_alarm_log values('','%s','%s','%s','%s','RECOVERY')" %(iteminfo[2],iteminfo[3],monitorTime,iteminfo[10])
                log_info("打印日志LOG" +str(sql))
                cmdtosql.execsql(sql)

        else:#报警：1.DNS 不通
            reason = isAlarm
            #更新fail_count  last_result数据表
            update_table(iteminfo,reason)
            #判断失败次数
            if int(iteminfo[12]) + 1 >= int(iteminfo[8]):
                if iteminfo[16]:
                    send_messages(iteminfo,reason,'PROBLEM')
            #异常通知 ,插入alarm_log记录
            sql="insert into uxin_alarm_log values('','%s','%s','%s','%s','PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,reason)
            log_debug("打印日志LOG" +str(sql))
            cmdtosql.execsql(sql)

    except Exception as e:
        log_error("monitor_ping_index():"+str(iteminfo[2]) + ' ' + str(e))


def monitor_tcp_index(iteminfo):
    '''
    @Monitor tcp 入口函数
    '''
    try:
        monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        monitor_item_updateTime(iteminfo)
        ip = iteminfo[2]
        itemconfig = iteminfo
        port = itemconfig[4]
        isAlarm = tcp_check(ip,port)

        if isAlarm == True:#表示不报警
            #fail_count 清零
            update_fail_count(iteminfo,iteminfo[12])
            #逻辑fail_count - Alarm_retry
            if int(iteminfo[12]) - int(iteminfo[8]) >= 0:#表示上次报警了，是否恢复报警
                if iteminfo[16]:
                    send_messages(iteminfo,' ','RECOVERY')

                #恢复 ,插入alarm_log记录
                sql="insert into uxin_alarm_log values(NULL,'%s','%s','%s','%s','RECOVERY')" %(iteminfo[2],iteminfo[3],monitorTime,iteminfo[10])
                log_debug("打印日志LOG" +str(sql))
                cmdtosql.execsql(sql)

        else:#报警：1.ping 不通
            reason = isAlarm
            #更新fail_count  last_result数据表
            update_table(iteminfo,reason)
            #判断失败次数
            if int(iteminfo[12]) + 1 >= int(iteminfo[8]):
                if iteminfo[16]:
                    send_messages(iteminfo,reason,'PROBLEM')

            #异常通知 ,插入alarm_log记录
            sql="insert into uxin_alarm_log values('','%s','%s','%s','%s','PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,reason)
            log_debug("打印日志LOG" +str(sql))
            cmdtosql.execsql(sql)

    except Exception as e:
        log_error("monitor_tcp_index():"+str(iteminfo[2]) + ' ' + str(e))
        
def monitor_udp_index(iteminfo):
    '''
    @Monitor udp 入口函数
    '''
    try:
        monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        monitor_item_updateTime(iteminfo)
        ip = iteminfo[2]
        itemconfig = iteminfo
        port = itemconfig[4]
        isAlarm = udp_connect_check(ip,port)
        if isAlarm == True:#表示不报警
            #fail_count 清零
            update_fail_count(iteminfo,iteminfo[12])
            #逻辑fail_count - Alarm_retry
            if int(iteminfo[12]) - int(iteminfo[8]) >= 0:
                if iteminfo[16]:
                    send_messages(iteminfo,' ','RECOVERY')
                    #恢复 ,插入alarm_log记录
                sql="insert into uxin_alarm_log values(NULL,'%s','%s','%s','%s','RECOVERY')" %(iteminfo[2],iteminfo[3],monitorTime,iteminfo[10])
                log_debug("打印日志LOG" +str(sql))
                cmdtosql.execsql(sql)

        else:#报警:
            reason = isAlarm
            #更新fail_count  last_result数据表
            update_table(iteminfo,reason)
            #判断失败次数
            if int(iteminfo[12]) + 1 >= int(iteminfo[8]):
                if iteminfo[16]:
                    send_messages(iteminfo,reason,'PROBLEM')

            #异常通知 ,插入alarm_log记录
            sql="insert into uxin_alarm_log values('','%s','%s','%s','%s','PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,reason)
            log_debug("打印日志LOG" +str(sql))
            cmdtosql.execsql(sql)


        #所有流程走完后,更新时间
        #monitor_item_updateTime(iteminfo)

    except Exception as e:
        log_error("monitor_udp_index():"+str(iteminfo[2]) + ' ' + str(e))


def monitor_progress_index(iteminfo):
    '''
    @Monitor progress 入口函数
    '''
    try:
        monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        monitor_item_updateTime(iteminfo)
        ip = iteminfo[2]
        itemconfig = iteminfo
        progress = itemconfig[4]
        log_info(ip)
        log_info(progress)
        log_info(itemconfig[19])
        isAlarm = progress_check(ip,progress,itemconfig[19])
        log_info(88)
          #批量连接不上时，有用
        if isAlarm == True or isAlarm == "Connection Refused": #表示不报警
            #if isAlarm == True:  #表示不报警
     
            #fail_count 清零
            update_fail_count(iteminfo,iteminfo[12])
            log_info(22)
            #逻辑fail_count - Alarm_retry
            if int(iteminfo[12]) - int(iteminfo[8]) >= 0:#表示上次报警了，是否恢复报警
                log_info(33)
                if iteminfo[16] or iteminfo[20]:
                    log_info(44)
                    send_messages(iteminfo,' ','RECOVERY')
                #恢复 ,插入alarm_log记录
                sql="insert into uxin_alarm_log values(NULL,'%s','%s','%s',\"%s\",'RECOVERY')" %(iteminfo[2],iteminfo[3],monitorTime,iteminfo[10])
                log_debug("打印日志LOG" +str(sql))
                cmdtosql.execsql(sql)

        #连接不上时，跳过， 保持失败， 但不告警， 不更新
        elif isAlarm == "Connection Refused":
            pass

        else:#报警:
            reason = isAlarm
            #更新fail_count  last_result数据表
            update_table(iteminfo,reason)
            #判断失败次数
            if int(iteminfo[12]) + 1 >= int(iteminfo[8]):
                if iteminfo[16] or iteminfo[20]:
                    send_messages(iteminfo,reason,'PROBLEM')

            #异常通知 ,插入alarm_log记录
            sql="insert into uxin_alarm_log values('','%s','%s','%s',\"%s\",'PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,reason)
            cmdtosql.execsql(sql)
            log_debug("打印日志LOG" +str(sql))


        #所有流程走完后,更新时间
        if isAlarm == "Connection Refused":
            sql="insert into uxin_alarm_log values('','%s','%s','%s',\"%s\",'PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,'Connection Refused')
            cmdtosql.execsql(sql)
            log_info("IP地址: " + str(iteminfo[2]) + " 类型:" + str(iteminfo[1]) + "  报警名:" + str(iteminfo[3]) + \
                         "  检测对象:" + str(iteminfo[4]) + " Connection Refused")
        else:
            pass
            #monitor_item_updateTime(iteminfo)

    except Exception as e:
        ip = iteminfo[2]
        log_error( str(ip) + "monitor_progress_index():"+str(e))
                

        


def monitor_custom_index(iteminfo):
    '''
    @Monitor 自定义监控 入口函数  暂定3个参数  IP  端口 对比字段
    '''
    try:
        monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        monitor_item_updateTime(iteminfo)
        ip = iteminfo[2]
        arg2 = iteminfo[4]
        arg3 = iteminfo[15]
        scripts_list=DIRS['PY_OMS_LIB']
        isAlarm,reason = custom_connect_check(ip,arg2,arg3)
        if isAlarm == 0:#表示不报警
            #fail_count 清零
            update_fail_count(iteminfo,iteminfo[12])
            #逻辑fail_count - Alarm_retry
            if int(iteminfo[12]) - int(iteminfo[8]) >= 0:#表示上次报警了，是否恢复报警
                if iteminfo[16]:
                    send_messages(iteminfo,' ','RECOVERY')
                #恢复 ,插入alarm_log记录
                sql="insert into uxin_alarm_log values(NULL,'%s','%s','%s',\"%s\",'RECOVERY')" %(iteminfo[2],iteminfo[3],monitorTime,iteminfo[10])
                cmdtosql.execsql(sql)
                log_info(str(sql))

        else:#报警:
            #更新fail_count  last_result数据表
            update_table(iteminfo,reason)
            #判断失败次数
            if int(iteminfo[12]) + 1 >= int(iteminfo[8]):
                if iteminfo[16]:
                    send_messages(iteminfo,reason,'PROBLEM')

            #异常通知 ,插入alarm_log记录
            sql="insert into uxin_alarm_log values('','%s','%s','%s',\"%s\",'PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,reason)
            cmdtosql.execsql(sql)
            log_info(str(sql))


        #所有流程走完后,更新时间
        #monitor_item_updateTime(iteminfo)

    except Exception as e:
        log_error("monitor_custom_index():"+str(iteminfo[2]) + ' ' + str(e))


def monitor_local_index(iteminfo):
    '''
    @Monitor 本地脚本监控 入口函数  暂定3个参数  IP  脚本绝对路径 对比字段
    '''
    try:
        monitorTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        monitor_item_updateTime(iteminfo)
        ip = iteminfo[2]
        arg2 = iteminfo[4]
        arg3 = iteminfo[15]
        isAlarm,reason = local_shell_check(ip,arg2,arg3)
        
        if isAlarm == True or isAlarm == "Connection Refused":#表示不报警
            #fail_count 清零
            update_fail_count(iteminfo,iteminfo[12])
            #逻辑fail_count - Alarm_retry
            if int(iteminfo[12]) - int(iteminfo[8]) >= 0:#表示上次报警了，是否恢复报警
                if iteminfo[16]:
                    send_messages(iteminfo,' ','RECOVERY')
                #恢复 ,插入alarm_log记录
                sql="insert into uxin_alarm_log values(NULL,'%s','%s','%s',\"%s\",'RECOVERY')" %(iteminfo[2],iteminfo[3],monitorTime,iteminfo[10])
                log_debug("打印日志LOG" +str(sql))
                cmdtosql.execsql(sql)

        else:#报警:
            #更新fail_count  last_result数据表
            update_table(iteminfo,reason)
            #判断失败次数
            #加1， 是因为iteminfo的值是 update_table 前获取的， 所以+1
            if int(iteminfo[12]) + 1 >= int(iteminfo[8]):
                if iteminfo[16]:
                    send_messages(iteminfo,reason,'PROBLEM')

            #异常通知 ,插入alarm_log记录
            sql="insert into uxin_alarm_log values('','%s','%s','%s',\"%s\",'PROBLEM')" %(iteminfo[2],iteminfo[3],monitorTime,reason)
            log_debug("打印日志LOG" +str(sql))
            cmdtosql.execsql(sql)


        #所有流程走完后,更新时间
        #monitor_item_updateTime(iteminfo)

    except Exception as e:
        log_error("monitor_local_index():"+str(iteminfo[2]) + ' ' + str(e))


def monitor_function_choose(itemtype):
    '''
    @ 根据监控项目类型来选择要执行的函数方法
    '''
    if itemtype == 'web':
            return monitor_website_index
    elif itemtype == 'ping':
            return monitor_ping_index
    elif itemtype == 'tcp':
            return monitor_tcp_index
    elif itemtype == 'udp':
            return monitor_udp_index
    elif itemtype == 'progress':#进程监控
            return monitor_progress_index
    elif itemtype == 'dns':#进程监控
            return monitor_dns_index
    elif itemtype == 'custom':#自定义
            return monitor_custom_index
    elif itemtype == 'local':#脚本
            return monitor_local_index
    else:
            return None

if __name__ == '__main__':
    '''
    @test
    '''
    pass
        
