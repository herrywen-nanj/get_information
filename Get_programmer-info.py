#!/usr/bin/python
#coding=utf-8
import commands
# python3中使用subprocess替代commands模块,如果你使用python3请打开注释
# import subprocess
#def getComstr(command):
#    try:
#        proStr = subprocess.getoutput(command)
#    except:
#        print "command {0} execute failed,exit".format(command)
#    return proStr



def getComStr(comand):
    try:
        stat, proStr = commands.getstatusoutput(comand)
    except:
        print "command %s execute failed, exit" % comand
    return proStr


# 获取程序的端口号和名字
def filterList():
    command = 'netstat -tlnp | grep -v ":::" | grep -v "master" | grep -v "cupsd"'
    tmpStr = getComStr(command)
    tmpList = tmpStr.split("\n")
    del tmpList[0:2]
    newList = []
    for i in tmpList:
        a = []
        val = i.split()
        del val[0:3]
        del val[1:3]
        valTmp = val[0].split(":")
        a.append(valTmp[1])
        valTmp = val[1].split("/")
        a.append(valTmp[0])
        try:
            a.append(valTmp[1])
        except IndexError:
            pass
        if a[1] != '-' and a not in newList:
            newList.append(a)
    return newList


# 获取程序的工作路径
def filterprocess(PID):
    command = "pwdx {PID}".format(PID=PID)  + "|" + "awk '{print $NF}'"
    workdir = getComStr(command)
    return workdir

# 获取程序的启动命令
def GetStartProcessCommand(PID):
    # 精确匹配内容
    command = "ps aux | grep -w {PID}".format(PID=PID) + "|"  + "grep -v 'grep'"
    tmplist1 = getComStr(command)
    tmplist1 = tmplist1.split()
    ProcessCommand = " ".join(tmplist1[10:])
    return ProcessCommand

# 将数据拼接成json格式
def InformationChangeJson():
    netInfo = filterList()
    json_data = "[" + "\n"
    for net in netInfo:
        workdir = filterprocess(net[1])
        ProcessCommand = GetStartProcessCommand(net[1])
        if net != netInfo[-1] and workdir == "/":
            json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#PPORT}":"' + str(net[0]) + "\",\n" + "\t\t\t" + '"{#PROGRAMWORKPATH}":"' + workdir + "\",\n" + "\t\t\t" + '"{#ProcessStartCommand}":"' + ProcessCommand + "\",\n" + "\t\t\t" + '"{#PNAME}":"' + str(net[2]) + "\"},\n"
        elif net != netInfo[-1] and workdir != "/":
            ProcessCommand = workdir + "/" + ProcessCommand
            json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#PPORT}":"' + str(net[0]) + "\",\n" + "\t\t\t" + '"{#PROGRAMWORKPATH}":"' + workdir + "\",\n" + "\t\t\t" + '"{#ProcessStartCommand}":"' + ProcessCommand + "\",\n" + "\t\t\t" + '"{#PNAME}":"' + str(net[2]) + "\"},\n"
        else:
            json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#PPORT}":"' + str(net[0]) + "\",\n" + "\t\t\t" + '"{#PROGRAMWORKPATH}":"' + workdir + "\",\n" + "\t\t\t" + '"{#ProcessStartCommand}":"' + ProcessCommand + "\",\n" + "\t\t\t" + '"{#PNAME}":"' + str(net[2]) + "\"}]}"
    return json_data

# 获取当前网卡IP地址，注意需要查看当前网卡名称，做相应修改
def GetNetworkIp():
    command = "ifconfig ens32 | grep -w inet | awk '{print $2}'"
    networkip = getComStr(command)
    return networkip

# 写入到当前路径下，文件格式是ip.txt
def main():
    ip = GetNetworkIp()
    filename = ip + ".txt"
    with open(filename,"w") as object:
        Information = InformationChangeJson()
        object.write(Information)

if __name__ == "__main__":
    main()
