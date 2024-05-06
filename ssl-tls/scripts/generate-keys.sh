# Criar um certificado de Autoridade de Certificação (CA) Autoassinado
# CA Raiz: Responsável por assinar os certificados criados.

# -x509: Indica que o formato do certificado gerado será um certificado autoassinado
# -sha259: Algoritmo de hash utilizado
# -days 3650: Validade do certificado em dias
# -newkey rsa:4096: Indica que o par de chaves públicas e privadas são do tipo RSA de 4096 bits
# -keyout rootCA.key: Indica o nome do arquivo onde a chave privada será salva
# -out rootCA.crt: Especifica o nome do arquivo onde o arquivo será salvo
openssl req -x509 -sha256 -days 3650 -newkey rsa:4096 -keyout rootCA.key -out rootCA.crt
