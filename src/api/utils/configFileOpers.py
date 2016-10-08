#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os


class ConfigFileOpers(object):

    @staticmethod
    def get_value(filename, key, separator='='):
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.find(key) >= 0 and line.find(separator) > 0:
                    pair = line.split(separator)
                    value = separator.join(pair[1:])
                    return value.strip()
            return ''

    def getValue(self, fileName, keyList=None):
        resultValue = {}
        f = file(fileName, 'r')

        totalDict = {}
        while True:
            line = f.readline()

            if not line:
                break

            pos1 = line.find('=')
            key = line[:pos1]
            value = line[pos1 + 1:len(line)].strip('=').strip('\n')
            totalDict.setdefault(key, value)

        f.close()

        if keyList == None:
            resultValue = totalDict
        else:
            for key in keyList:
                value = totalDict.get(key)
                resultValue.setdefault(key, value)

        return resultValue

    @staticmethod
    def set_value(filename, dic, separator="="):
        with open(filename, 'r') as f:
            readlines = f.readlines()
        writelines = []
        with open(filename, 'w') as f:
            for line in readlines:
                if line.find(separator):
                    pair = line.split(separator)
                    key = pair[0].strip('#').strip()
                    if key in dic:
                        if separator != ':':
                            line = key + separator + str(dic[key]) + '\n'
                        else:
                            line = key + separator + ' ' + str(dic[key]) + '\n'
                writelines.append(line)
            f.writelines(writelines)
            f.flush()

    def retrieve_full_text(self, fileName):
        inputstream = open(fileName)
        lines = inputstream.readlines()
        inputstream.close()

        resultValue = ''
        for line in lines:
            resultValue += line

        return resultValue

    def writeFullText(self, fileName, fullText):
        if os.path.exists(fileName):
            outputstream = open(fileName, 'w')
            outputstream.write('')
            outputstream.close()
        outputstream = open(fileName, 'w')
        outputstream.write(fullText)
        outputstream.close()


if __name__ == "__main__":
    s = ConfigFileOpers()
    resultValue = s.getValue(
        'C:/Users/asus/Downloads/my.cnf', ['wsrep_cluster_address', 'wsrep_sst_auth'])
    print resultValue

    s.setValue('C:/Users/asus/Downloads/my.cnf', {'wsrep_sst_auth': 'zbz:zbz'})
    resultValue = s.getValue(
        'C:/Users/asus/Downloads/my.cnf', ['wsrep_cluster_address', 'wsrep_sst_auth'])
    print resultValue

    resultValue = s.retrieve_full_text('C:/Users/asus/Downloads/my.cnf')
    print resultValue
