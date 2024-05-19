# Squid Proxy Server

## Instalar o Squid

```bash
sudo apt install squid
```

## Configurar o servidor squid

### Criar uma cópia do arquivo de configuração original

```bash
sudo cp -v /etc/squid/squid.conf{,.factory}
```

### Abrir arquivo de configurações

```bash
sudo nano /etc/squid/squid.conf
```

## Configurando ACL para portas

ACL são esquemas de acesso que permitem ou negam acesso a um determinado recurso na rede.

### Permitir ou bloquear acesso a serviços

```bash
# Bloqueio de sites específicos
acl block_websites dstdomain "caminho/para/arquivo/de/dominios/bloqueados"
acl block_keywords url_regex -i "caminho/para/arquivo/de/palavras/chave/bloqueadas"

# Aplicando as regras de bloqueio
http_access deny block_websites
http_access deny block_keywords

# Permitir acesso ao restante da web
http_access allow all
```

## Inicializar serviço do squid

### Ligar o serviço do Squid na inicialização do sistema

```bash
sudo systemctl enable squid.service
```

### Iniciar serviço do Squid

```bash
sudo systemctl start squid.service
```

### Recarregar as configurações do squid após alterá-las

```bash
sudo systemctl reload squid.service
```

### Para serviço do squid

```bash
sudo systemctl stop squid.service
```

## Configurar o Navegador / SO para usar o servidor Proxy

- Listar o endereço IP do servidor

```bash
ip addr
```

- Nas configurações de Proxy do Navegador ou SO informe:
    - Endereço ip do Servidor
    - Porta padrão do Proxy: `3128`