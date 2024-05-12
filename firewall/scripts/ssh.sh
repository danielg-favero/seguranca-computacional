# Permitir apenas conexões SSH vindas de um servidor

# -A INPUT: Adiciona uma nova regra ao final da cadeia de entrada
# -i eth0: Pacotes que chegam pela interface eth0 serão verificados por essa regra
# -p tcp -dport 22: Indica que esta regra é para pacotes TCP, a porta de destino no servidor é a 22, que a porta padrão do SSH
# -j ACCEPT: "pula" para o comando de aceitar os pacotes que passam pela regra
# -m conntrack --ctstate NEW,ESTABLISHED: Utiliza o conntrack para verificar o estado da conexão. Permite o tráfego que está em estado NEW e ESTABLISHED
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT

# -A OUTPUT: Adiciona uma regra ao final da cadeia de saída
# --sport 22: Especifica que a porta de origem (source port) é a 22, que a porta padrão do SSH
iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT