# Criar um repositórios de chaves e importar o arquivo localhost.p12 em keystore Java
# A partir de então o certificado poderá ser usado em uma aplicação Java

# -importkeystore: Indica que será importado um keystore de um formato para outro.
# -srckeystore localhost.p12: Especifica o arquivo de keystore de origem (PKCS #12) que será importado.
# -srcstoretype PKCS12: Especifica o tipo de keystore de origem
# -destkeystore keystore.jks: Especifica o nome do novo keystore de destino (JKS) que será criado ou sobrescrito
# -deststoretype JKS: Especifica o tipo de keystore de destino
keytool -importkeystore -srckeystore localhost.p12 -srcstoretype PKCS12 -destkeystore keystore.jks -deststoretype JKS