# Gerar um certificado SSL/TLS para um domínio local, que será útil para desenvolvimento.
# Criar uma solicitação de certificado assinado (CSR)

# -new: Indica que estamos gerando uma nova solicitação de certificado
# -newkey rsa:4096: Cria uma nova chave RSA de 4096 bits e a associa à solicitação de certificado.
# -keyout localhost.key: Especifica o nome do arquivo onde a chave privada será salva.
# -out localhost.csr: especifica o nome do arquivo onde a solicitação de certificado será salva 
openssl req -new -newkey rsa:4096 -keyout localhost.key -out localhost.csr


# Assinar a solicitação com o certificado rootCA
# Isso gerará um certificado SSL/TLS válido.

# -CA rootCA.crt: Especifica o arquivo que contém o certificado da autoridade de certificação
# -CAkey rootCA.key: Especifica o arquivo que contém a chave privada da autoridade de certificação
# -in localhost.csr: Especifica o arquivo que contém a solicitação de certificado a ser assinada
# -out localhost.crt: especifica o nome do arquivo onde o certificado assinado será salvo.
# -days 365: Define a validade do certificado em dias.
# -CAcreateserial: Indica para criar um arquivo serial para o certificado assinado
# -extfile localhost.ext: Especifica o arquivo quem contém extensões de certificado personalizadas a serem adicionadas ao certificado assinado
openssl x509 -req -CA rootCA.crt -CAkey rootCA.key -in localhost.csr -out localhost.crt -days 365 -CAcreateserial -extfile localhost.ext
