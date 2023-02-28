### TESTE 1

Deve iniciar com a lista de localizacao vazia
Assim, no inicio eh esperado
lista de latlon = []

### TESTE 2

Deve salvar primeiro ponto
Ao chamar o metodo savePosition a
lista de latlon = [[28.1, -45.2]]
(tem que conter o ponto salvo)

### TESTE 3

Deve salvar primeiro ponto mesmo com uma acuracia ruim
Dado a regra qeu se a acuracia eh muito ruim (exemplo 50 metros) onde descartamos pontos ruins, MAS se
eh o primeiro ponto, eh melhor salvar um ponto inicial
ruim do que simplesmente ficar ignorando os primeiros pontos.

### TESTE 4

Deve descartar um ponto com acuracia ruim, ao receber
diversos pontos com uma acuracia aceitavel (entre 1, 10 ou ate 20 metros por exemplo, e se no meio disto vem um ponto com acuracia > 40, este ultimo nao deve ser salvo

### TESTE 5

Deve descartar pontos ruins, tambem podemos ter pontos 
com acuracia entre, 20, 28 apenas onde embora nao
seja muito bom, mas sao os melhores que temos, iremos salva-los. Mas se aparecer pontos fora disto, talvez > 30
estes poderiam ser descartados
