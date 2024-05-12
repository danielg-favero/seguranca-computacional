# Excluir todas as regras do IPTables

# -F: Esvazia todas as cadeias
sudo iptables -F

# -t nat -F: esvazia todas tabela nat
sudo iptables -t nat -F

# -X: esvazia todas as tabelas não padrões
sudo iptables -X

sudo iptables -L