# Permitir que o servidor respond a conexões SMTP

# -p icmp: Especifica que a regra está sobre o Protocolo ICMP, geralmente atribuído ao ping
# -j DROP: Especifica que a ação a ser tomada se o tráfego corresponder a esta regra é descartá-lo. Ou seja, bloquear pacotes ICMP.
iptables -A OUTPUT -p icmp -i eth0 -j DROP
iptables -A INPUT -p icmp -i eth0 -j DROP