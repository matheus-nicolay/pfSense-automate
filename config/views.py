from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.

def index(request):
    return render(request, 'pfsense/index.html')

def sendConf(request):
    dictResponse = dict(request.POST)

    hostname = request.POST['hostname']
    domain = request.POST['domain']
    lanIP = request.POST['lanIP']
    wanIP = request.POST['wanIP']
    password = request.POST['password']
    del dictResponse['hostname']
    del dictResponse['domain']
    del dictResponse['lanIP']
    del dictResponse['wanIP']
    del dictResponse['password']
    del dictResponse['csrfmiddlewaretoken']

    pfSenseURL = "http://exampleip/api/v1/"
    pfSenseUser = 'admin'
    pfSensePass = 'admin'

    UpdateUserPasswordData = {
        "password": password,
        "username": "admin"
    }


    UpdateSystemConfigData = {
        "domain": domain,
        "hostname": hostname
    }

    UpdateLanData = {
        "apply": "true",
        "type": "staticv4",
        "id": "lan",
        "ipaddr": lanIP,
        "enable": "true",
        "subnet": 24,
        "blockbogons": "false"
    }

    UpdateWanData = {
        "apply": "falsa",
        "type": "staticv4",
        "id": "wan",
        "ipaddr": wanIP,
        "enable": "true",
        "subnet": 24,
        "blockbogons": "false"
    }

    UpdateLanGatewayData = {
        "apply": "true",
        "descr": "LAN interface",
        "gateway": lanIP,
        "id": 1,
        "interface": "lan",
        "ipprotocol": "inet"
    }

    dataOutboundLan = {
        "apply": "true",
        "descr": "Outbound pfSense",
        "dst": "any",
        "dstport": "any",
        "interface": "wan",
        "protocol": "any",
        "src": lanIP,
        "srcport": "any",
        "target": wanIP
    } 

    UpdateSystemConfig_Request = requests.put(pfSenseURL+'system/hostname', auth=(pfSenseUser, pfSensePass), json=UpdateSystemConfigData)
    UpdateLan_Request  = requests.put(pfSenseURL+'interface', auth=(pfSenseUser, pfSensePass), json=UpdateLanData)
    UpdateLanGateway_Request = requests.put(pfSenseURL+'routing/gateway', auth=(pfSenseUser, pfSensePass), json=UpdateLanGatewayData)
    OutboundLan_Request = requests.post(pfSenseURL+'firewall/nat/outbound/mapping', auth=(pfSenseUser, pfSensePass), json=dataOutboundLan)

    for key in dictResponse:
        if(key.split(".")[0] == "virtualIP"):
            virtualIP = dictResponse[key]

            dataOutboundVirtual = {
                "apply": "true",
                "descr": "",
                "dst": "any",
                "dstport": "any",
                "interface": "wan",
                "protocol": "any",
                "src": virtualIP[1],
                "srcport": "any",
                "target": virtualIP[0]
            } 

            dataVirtualIP = {
                "interface": "wan",
                "mode": "proxyarp",
                "descr": "",
                "subnet": virtualIP[0]
            }
            VirtualIP_Request = requests.post(pfSenseURL+'firewall/virtual_ip', auth=(pfSenseUser, pfSensePass), json=dataVirtualIP)
            OutboundVirtualIP_Request = requests.post(pfSenseURL+'firewall/nat/outbound/mapping', auth=(pfSenseUser, pfSensePass), json=dataOutboundVirtual)

            if(VirtualIP_Request.json()['code'] != 200):
                print(f"Erro ao cadastrar o IP virtual: {virtualIP}: {VirtualIP_Request.json()['message']}")
            if(OutboundVirtualIP_Request.json()['code'] != 200):
                print(f"Erro ao cadastrar o Outbound: {virtualIP}: {OutboundVirtualIP_Request.json()['message']}")
                
        if(key.split(".")[0] == "alias"):
            alias = dictResponse[key] 

            dataCreateAlias = {
                "type": "host",
                "name": alias[0],
                "address": alias[1],     
            }
            CreateAlias_Request = requests.post(pfSenseURL+'firewall/alias', auth=(pfSenseUser, pfSensePass), json=dataCreateAlias)

            if(CreateAlias_Request.json()['code'] != 200):
                print(f"Erro ao cadastrar o Alias {alias}: {CreateAlias_Request.json()['message']}")

        if(key.split(".")[0] == "rule"):
            externalIP = dictResponse[key][0]
            if(externalIP == ""):
                externalIP = wanIP

            internalIP = dictResponse[key][1]
            ports = dictResponse[key][2].split(",")

            for port in ports:
                dataForwardRule = {
                    "apply": "true",
                    "descr": f"NAT {internalIP} - {port}",
                    "disabled": "false",
                    "dst": externalIP,
                    "dstport": port.lstrip(),
                    "interface": "wan",
                    "local-port": port.lstrip(),
                    "natreflection": "enable",
                    "nordr": "false",
                    "nosync": "false",
                    "protocol": "tcp",
                    "src": "any",
                    "srcport": "any",
                    "target": internalIP,
                    "top": "false",
                }

                dataRule = {
                    "apply": "true",
                    "descr": f"Rule {internalIP} - {port}",
                    "dst": lanIP,
                    "dstport": port.lstrip(),
                    "floating": "false",
                    "interface": "wan",
                    "ipprotocol": "inet",
                    "log": "false",
                    "protocol": "tcp",
                    "src": "any",
                    "srcport": "any",
                    "top": "false",
                    "type": "pass"
                }

                ForwardRuleHTTP_Request = requests.post(pfSenseURL+'firewall/nat/port_forward', auth=(pfSenseUser, pfSensePass), json=dataForwardRule)
                RulepfSenseHTTP_Request = requests.post(pfSenseURL+'firewall/rule', auth=(pfSenseUser, pfSensePass), json=dataRule)

                if(ForwardRuleHTTP_Request.json()['code'] != 200):
                    print(f"Erro ao criar direcionamento {internalIP} - {port} "+ForwardRuleHTTP_Request.json()['message'])
                if(RulepfSenseHTTP_Request.json()['code'] != 200):
                    print(f"Erro ao criar regra {internalIP} - {port}"+RulepfSenseHTTP_Request.json()['message'])

    UpdateWan_Request  = requests.put(pfSenseURL+'interface', auth=(pfSenseUser, pfSensePass), json=UpdateWanData)

    UpdateUserPassword_Request = requests.put(pfSenseURL+'user', auth=(pfSenseUser, pfSensePass), json=UpdateUserPasswordData)

    if(UpdateSystemConfig_Request.json()['code'] != 200):
        print("Erro ao atualizar domínio/hostname: "+UpdateSystemConfig_Request.json()['message'])
    if(OutboundLan_Request.json()['code'] != 200):
        print("Erro ao atualizar configurações outbound da LAN: "+OutboundLan_Request.json()['message'])
    if(UpdateSystemConfig_Request.json()['code'] != 200):
        print("Erro ao atualizar domínio/hostname: "+UpdateSystemConfig_Request.json()['message'])

    if(UpdateUserPassword_Request.json()['code'] != 200):
        print("Erro ao atualizar domínio/hostname: "+UpdateUserPassword_Request.json()['message'])

    #applyChanges_Request = requests.put(pfSenseURL+'firewall/apply', auth=(pfSenseUser, pfSensePass))

    print(dictResponse)

    return HttpResponse(request.POST)   

