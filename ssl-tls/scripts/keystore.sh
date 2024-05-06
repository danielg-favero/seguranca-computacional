# Armazenar as chaves privadas e o certificado assinado em um arquivo PKCS#12

# -export: Indica que será exportado o conteúdo para um arquivo PKCS #12
# -out localhost.p12: Especifica o nome do arquivo de saída PKCS #12
# -name "localhost": Especifica o nome a ser atribuído ao certificado dentro do arquivo PKCS #12
# -inkey localhost.key: Especifica o arquivo que contém a chave privada correspondente ao certificado
# -in localhost.crt: Especifica o arquivo que contém o certificado a ser incluído no arquivo PKCS #12
openssl pkcs12 -export -out localhost.p12 -name "localhost" -inkey localhost.key -in localhost.crt

