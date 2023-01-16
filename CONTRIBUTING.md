# Dicas para contribuir no projeto

A ideia aqui é mais mostrar práticas que o mercado de trabalho utiliza para desenvolvimento em equipe

## 1 - Utilizar branches

Ao invés de fazer commits diretamente na branch principal (main), a ideia garantir que você está com a última versão do código (`git pull`) e em seguida trabalhar em uma branch local (`git checkout -b issue1_versao_inicial`) e fazer os commits nesta branch, quando a versão estiver rodando localmente, enviar esta branch para o repositório remoto (`git push origin issue1_versao_inicial`).
Desta forma, outros contribuidores podem revisar o código antes de mesmo chegar na branch principal.
_NOTA:_ O nome da issue1_versao_inicial e referente ao nome da branch e deve mudar a cada trabalho
