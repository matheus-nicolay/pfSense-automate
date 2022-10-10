import requests
import json

url = "http://179.43.43.122/api/v1/"

UpdateWanData = {
  "apply": "true",
  "type": "staticv4",
  "id": "wan",
  "ipaddr": "10.0.0.145",
  "enable": "true",
  "subnet": 24,
  "blockbogons": "false"
}



UpdateLanData = {
  "apply": "true",
  "type": "staticv4",
  "id": "lan",
  "ipaddr": "192.168.95.254",
  "enable": "true",
  "subnet": 24,
  "blockbogons": "false"
}

#UpdateLanConfig = requests.put(url+'interface', auth=('admin', 'Staybox@1'),json=UpdateLanData)

UpdateWanGatewayData = {
  "apply": "true",
  "descr": "WAN interface",
  "gateway": "10.0.0.254",
  "id": 0,
  "interface": "wan",
  "ipprotocol": "inet"
}

UpdateLanGatewayData = {
  "apply": "true",
  "descr": "LAN interface",
  "gateway": "192.168.95.1",
  "id": 1,
  "interface": "lan",
  "ipprotocol": "inet"
}

#UpdateWANGateway = requests.put(url+'routing/gateway', auth=('admin', 'Staybox@1'), json=UpdateWanGatewayData)
#UpdateLanGateway = requests.put(url+'routing/gateway', auth=('admin', 'Staybox@1'), json=UpdateLanGatewayData)

UpdateLanConfigData = {
  "domain": "nomeempresa.staybox.com.br",
  "hostname": "fw01"
}

#UpdateLanConfig = requests.put(url+'system/hostname', auth=('admin', 'Staybox@1'), json=UpdateLanConfigData)

UpdateUserPasswordData = {
  "password": "Staybox@1",
  "username": "admin"
}

#UpdateUserPassword = requests.put(url+'user', auth=('admin', 'Staybox@1'), json=UpdateUserPasswordData)

OutboundCreateData = {
  "apply": "true",
  "descr": "Outbound pfSense",
  "dst": "any",
  "dstport": "any",
  "interface": "wan",
  "protocol": "any",
  "src": "10.0.0.254",
  "target": ""
}

#OutboundCreate = requests.post(url+'firewall/nat/outbound/mapping', auth=('admin', 'Staybox@1'), json=OutboundCreateData)

AcmePackageInstall = requests.post(url+'system/package', auth=('admin', 'Staybox@1'), json={"name": "pfSense-pkg-acme"})

###################################### FAZER REGRAS DE FORWARD/FILTER RULES  ################################################

""" {
    "wanIP"
    "wanGW"
    "lanIP"
    "domain"
    "hostname"
    "adminPassword"
}

Processos manuais: Ajustar hostname Zabbix, Instalar certificado ACME, Atualizar pfBlocker """

dataForward = {
  "apply": "true",
  "descr": "VM 2314 - REGRA TESTE",
  "disabled": "false",
  "dst": "vtnet0",
  "dstport": "80",
  "interface": "wan",
  "local-port": "80",
  "natreflection": "enable",
  "nordr": "false",
  "nosync": "false",
  "protocol": "tcp",
  "src": "Gerencia_Staybox",
  "srcport": "any",
  "target": "10.0.0.10",
  "top": "false",
}

#ForwardResponse = requests.post(url+'firewall/nat/port_forward', auth=('admin', 'Staybox@1'),json=data)

dataRule = {
  "apply": "true",
  "descr": "VM 2314 - REGRA TESTE",
  "direction": "any",
  "disabled": "false",
  "dst": "10.0.0.10",
  "dstport": "80",
  "floating": "false",
  "icmptype": [
    "althost"
  ],
  "interface": "wan",
  "ipprotocol": "inet",
  "log": "false",
  "protocol": "tcp",
  "src": "any",
  "srcport": "any",
  "top": "false",
  "type": "pass"
}

#RulesResponse = requests.post(url+'firewall/rule', auth=('admin', 'Staybox@1'),json=dataRule)


#print(AcmePackageInstall.json())



