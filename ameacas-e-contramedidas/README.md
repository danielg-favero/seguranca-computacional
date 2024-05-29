# Instalando um Log Server no Ubuntu

## Instalando o Rsyslog

Ele geralmente já vem baixado no Ubuntu. Para verificar:

```bash
apt list -a rsyslog
```

Para habilitar o serviço do rsyslog:

```bash
sudo systemctl enable --now rsyslog
```

## Configurando o Rsyslog como um Server

Editar o arquivo de configurações

```bash
sudo nano /etc/rsyslog.conf
```

### Recebendo log de protocolo UDP

```
# provides UDP syslog reception
module(load="imudp")
input(type="imudp" port="514")
```

### Recebendo log de protocolo TCP

```
# provides TCP syslog reception
module(load="imtcp")
input(type="imtcp" port="50514")
```

## Reiniciar serviço do Rsyslog

```bash
sudo systemctl restart rsyslog
```

Para verificar se o `Rsyslog` está escutando para as duas portas configuradas:

```bash
sudo ss -4altunp | grep 514
```

Para verificar se as configurações estão ok:

```bash
sudo rsyslogd -f /etc/rsyslog.conf -N1
```

## Habilitar o Rsyslog através do Firewall

```bash
sudo ufw allow 514/udp
```

```bash
sudo ufw allow 50514/tcp
```

## Definir quem poderá mandar logs para o servidor

Dentro do arquivo de configurações do rsyslog:

```
###########################
#### GLOBAL DIRECTIVES ####
###########################
# $AllowedSender - specifies which remote systems are allowed to send syslog messages to rsyslogd
$AllowedSender UDP, 192.168.58.0/24, [::1]/128, *.example.net, servera.example.com
$AllowedSender TCP, 192.168.59.0/24, [::1]/128, *.example.net, serverb.example.com
```

## Definir um template para os logs

Dentro do arquivo de configurações do servidor

```
$template TEMPLATE_NAME,"text %PROPERTY% more text", [OPTION]
```

Por exemplo:
```
#Custom template to generate the log filename dynamically based on the client's IP address.
$template RemInputLogs, "/var/log/remotelogs/%HOSTNAME%/%PROGRAMNAME%.log"
*.* ?RemInputLogs
& ~
```


## Mandar os Logs do cliente para o servidor

Dentro do arquivo do Rsyslog do cliente:

```
# Send logs to remote syslog server over UDP
auth,authpriv.* @192.168.59.38:514

# Send logs to remote syslog server over TCP 50514
*.* @@192.168.59.38:50514
```

Para verificar o recebimento pode executar o comando no server:

```bash
logger "Test log message from rsyslog setup"
```

E dentro do servidor, o log deve aparecer em: `/var/log/remotelogs`