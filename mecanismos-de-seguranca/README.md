# Snort

## Instalação do Snort:

### Baixar as dependências necessárias para o Snort

```bash
sudo apt install -y gcc libpcre3-dev zlib1g-dev libluajit-5.1-dev 
libpcap-dev openssl libssl-dev libnghttp2-dev libdumbnet-dev 
bison flex libdnet autoconf libtool
```

### Baixar o repositório do Snort

```bash
sudo apt-get install snort
```

```bash
cd /etc/snort
```

### Alterar arquivo de configurações

```bash
sudo nano snort.conf
```

> Agora é preciso comentar todas as regras do snort, menos a primeria que contém `$RULE_PATH`

### Criar regras customizadas

```bash
cd rules
```

```bash
sudo nano local.rules
```

As seguintes regras foram adicionadas:

```
alert tcp any any -> $HOME_NET 21 (msg: "FTP connection attempt"; sid:1000001; rev:1;)
alert icmp any any -> $HOME_NET any (msg: "ICMP test detected"; GID:1; sid:10000001; rev:001;)
alert tcp any any -> $HOME_NET 80 (msg: "HTTP connection attempt"; sid:1000005; rev:1;)
```

### Executar o teste de funcionamento do Snort

Esse comando executa um teste `(-T)` indicando o arquivo de configuração `(-c)` e a interface `(-i)`

```bash
sudo snort -T -c /etc/snort/snort.conf -i nome_da_interface_de_rede
```

### Executar o Snort

Esse comando executa efetivamente o snort

```bash
sudo snort -A console -q -u snort -g snort -c /etc/snort/snort.conf -i nome_da_interface_de_rede
```

Agora é possível testar um ping para a máquina que uma série de avisos irão aparecer.