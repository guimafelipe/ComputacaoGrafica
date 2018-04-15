# Primeiro relatório de Computação Gráfica

Autores: Felipe Guimarães e Gustavo Nahum

## Assunto: Algoritmos de Quantização de Cores

### Introdução

No segundo experimento da disciplina, fizemos um algoritmo de quantização de cores de imagens usando o método k-means. Esse método reduzia as cores da imagem em uma paleta de n cores e recoloria a imagem utilizando apenas essa paleta.

Quantização de cores é algo muito buscado artísticamente, e jogos digitais é um bom exemplo de aplicação desse efeito. Nesse relatório vamos falar de uma solução existente e muito famosa na indústria, o cel shader, e da nossa implementação do k-means como um shader para jogos e também sobre uma discussão do método de dithering de quantização de cores.

### Cel Shader (Toon shader)

Uma das soluções artísticas de quantização de cores mais conhecidas na indústria de games é o cel shader. Ele funciona fazendo um tratamento de discretização da luz incidente no vértice do modelo 3D e gera um efeito parecido com o de desenhos animados. Um jogo recente e famoso por fazer um ótimo uso dessa técnica é o Zelda: Breath of The Wild:

![Zelda](https://cdn3.whatculture.com/images/2017/03/339cdeff6ec52c0c-600x400.png)

Essa é uma solução apenas para jogos 3D e vamos ver abaixo um pouco do código de sua implementação.

### Dithering

Uma forma de aproximar tonalidades que não estão presentes em uma certa paleta de cores é através da técnica de "dithering", por meio da qual uma difusão de pixels coloridos dentro da paleta produzem a ilusão de estarem representando essas outras cores.

![Roxo](https://upload.wikimedia.org/wikipedia/commons/6/6d/Dithering_example_red_blue.png)

Nesta figura, vemos que as cores azul e vermelho podem ser usadas para assemelharem-se visualmente à cor roxa.

Um dos algoritmos usados para produzir efeito é o de Floyd-Steinberg, que atinge o dithering usando a difusão de erros, de forma que o erro de quantização residual de cada pixel é transferido, parcialmente, aos seus pixels vizinhos.

O algoritmo de Floyd-Steinberg percorre os pixels da imagem da esquerda para a direita, de cima para baixo, e somente transfere os erros de quantização para os pixels seguintes (não altera os pixels já percorridos). Dessa forma, se um conjunto de pixels são sucessivamente arredondados para baixo, aumenta-se a chance de o próximo pixel ser arredondado para cima de tal forma que, na média, o erro de quantização tenda a zero.

Os coeficientes de difusão usados no algoritmo apresentam a propriedade de, caso o valor do pixel original esteja exatamente na metade entre as duas cores mais próximas disponíveis na paleta, o resultado do dithering é um padrão xadrez. Por exemplo, o cinza 50% seria aproximado para um padrão xadrez preto e branco.
