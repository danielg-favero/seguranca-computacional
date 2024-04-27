# Criptografia Assimétrica

## Usando SSH Keygen

### RSA
```bash
ssh-keygen -t rsa -b 4096
```

- `-t rsa` especifica o tipo de chave a ser gerado
- `-b 4096` define o número de bits da chave

### EC
```bash
ssh-keygen -t ecdsa -b 521
```

- `-t ecdsa` especifica o tipo de chave ECDSA
- `-b 521` seleciona a curva de 521 bits

## Usando OpenSSL

### RSA
```bash
openssl genrsa -out caminho-do-arquivo/chave-privada.pem 2048
```

- Gera uma chave privada de 2048 bits

```bash
openssl rsa -in caminho-do-arquivo/chave-privada.pem -outform PEM -pubout -out caminho-do-arquivo/chave-publica.pem
```

- Extrai a chave pública da chave privada

### EC
```bash
openssl ecparam -name prime256v1 -genkey -noout -out caminho-do-arquivo/chave-privada.pem
```

```bash
openssl ec -in caminho-do-arquivo/chave-privada.pem -pubout -out caminho-do-arquivo/chave-publica.pem
```

- Extrai a chave pública da chave privada