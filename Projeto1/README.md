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
