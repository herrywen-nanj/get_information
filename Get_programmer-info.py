#!/usr/bin/python
#coding=utf-8
import commands

def getComStr(comand):
    try:
        stat, proStr = commands.getstatusoutput(comand)
    except:
        print "command %s execute failed, exit" % comand
    return proStr

def filterList():
    command = 'netstat -tlnp | grep -v "tcp6" | grep -v "master" | grep -v "cupsd" | grep -v "sshd" | grep -v "-"'
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
        # 获取PID
        a.append(valTmp[0])
        # 获取程序名称
        a.append(valTmp[1])
        if a[1] != '-' and a not in newList:
            newList.append(a)
    return newList

# 使用format格式化，出现$NF无法识别,待解决
def filterprocess(PID):
    command = "pwdx {PID}".format(PID=PID)  + "|" + "awk '{print $NF}'"
    workdir = getComStr(command)
    return workdir

def main():
    netInfo = filterList()
    json_data = "{\n" + "\t" + '"data":[' + "\n"
    for net in netInfo:
        workdir = filterprocess(net[1])
        if net != netInfo[-1]:
           json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#PPORT}":"' + str(net[0]) + "\",\n" + "\t\t\t" + '"{#PROGRAMWORKPATH}":"' + workdir + "\",\n" + "\t\t\t" + '"{#PNAME}":"' + str(net[2]) + "\"},\n"
        else:
           json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#PPORT}":"' + str(net[0]) + "\",\n" + "\t\t\t" + '"{#PROGRAMWORKPATH}":"' + workdir + "\",\n" + "\t\t\t" + '"{#PNAME}":"' + str(net[2]) + "\"}]}"
    print json_data

if __name__ == "__main__":
    main()
