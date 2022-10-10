import requests
import json

url = "https://fw01.zimbra.clientes.staybox.com.br/api/v1/"

#url = "http://179.43.43.122/api/v1/"

ports = ["25", "80", "443", "8080", "8443", "143", "465", "587", "993", "995", "7025"]

portsGerencia = ["22", "10050", "5001", "7071", "9071", "7780"]

for port in ports:
    dataForward = {
        "apply": "true",
        "descr": "VM 4026 RIPF-Ubuntu20-Zimbra "+port,
        "disabled": "false",
        "dst": "179.43.40.148",
        "dstport": port,
        "interface": "wan",
        "local-port": port,
        "natreflection": "enable",
        "nordr": "false",
        "nosync": "false",
        "protocol": "tcp",
        "src": "any",
        "srcport": "any",
        "target": "192.168.91.6",
        "top": "false",
    }

    dataRule = {
        "apply": "true",
        "descr": "VM 4026 RIPF-Ubuntu20-Zimbra "+port,
        "direction": "any",
        "disabled": "false",
        "dst": "192.168.91.6",
        "dstport": port,
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

    ForwardResponse = requests.post(url+'firewall/nat/port_forward', auth=('admin', 'ghZ-h(1YNoLp?JfTclz3kN5_Jh.OJkB/i9[NM5b?'),json=dataForward)
    RulesResponse = requests.post(url+'firewall/rule', auth=('admin', 'ghZ-h(1YNoLp?JfTclz3kN5_Jh.OJkB/i9[NM5b?'),json=dataRule)

    print(ForwardResponse.json())
    print(RulesResponse.json())

for port in portsGerencia:
    dataForward = {
        "apply": "true",
        "descr": "VM 4026 RIPF-Ubuntu20-Zimbra "+port,
        "disabled": "false",
        "dst": "179.43.40.148",
        "dstport": port,
        "interface": "wan",
        "local-port": port,
        "natreflection": "enable",
        "nordr": "false",
        "nosync": "false",
        "protocol": "tcp",
        "src": "Gerencia_Staybox",
        "srcport": "any",
        "target": "192.168.91.6",
        "top": "false",
    }

    dataRule = {
        "apply": "true",
        "descr": "VM 4026 RIPF-Ubuntu20-Zimbra "+port,
        "direction": "any",
        "disabled": "false",
        "dst": "192.168.91.6",
        "dstport": port,
        "floating": "false",
        "interface": "wan",
        "ipprotocol": "inet",
        "log": "false",
        "protocol": "tcp",
        "src": "Gerencia_Staybox",
        "srcport": "any",
        "top": "false",
        "type": "pass"
    }

    ForwardResponse = requests.post(url+'firewall/nat/port_forward', auth=('admin', 'ghZ-h(1YNoLp?JfTclz3kN5_Jh.OJkB/i9[NM5b?'),json=dataForward)
    RulesResponse = requests.post(url+'firewall/rule', auth=('admin', 'ghZ-h(1YNoLp?JfTclz3kN5_Jh.OJkB/i9[NM5b?'),json=dataRule)

    print(ForwardResponse.json())
    print(RulesResponse.json())


dataForward = {
  "apply": "true",
  "descr": "VM 4026 RIPF-Ubuntu20-Zimbra",
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

#ForwardResponse = requests.post(url+'firewall/nat/port_forward', auth=('admin', 'ghZ-h(1YNoLp?JfTclz3kN5_Jh.OJkB/i9[NM5b?'),json=dataForward)

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

#RulesResponse = requests.post(url+'firewall/rule', auth=('admin', 'ghZ-h(1YNoLp?JfTclz3kN5_Jh.OJkB/i9[NM5b?'),json=dataRule)


# DESENVOLVER PARA CRIAR ALIASES
	# DESENVOLVER PARA CRIAR OUTBOUNT
# DESENVOLVER PARA CRIAR VIRTUAL IPS
# DESENVOLVER PARA CONFIGURAR OPENVPN E USUÁRIOS

# ALTERAR SENHA EM ÚLTIMO PASSO

# COISAS A SER FEITAS MANUAIS: COLOCAR VLAN NA LAN E TROCAR MAC, GERAR CERTIFICADO, AJUSTAR HOSTNAME NO ZABBIX AGENT 
