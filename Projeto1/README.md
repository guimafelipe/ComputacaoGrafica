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

Fizemos um shader básico e usamos modelos 3D para fazer o teste estético. O código do toon shader é extremamente simples e usa a intensidade da luz para definir a discretização do albedo do personagem.

```glsl
varying vec3 lightVec;

void fragment() {	
  vec3 albedoAux;
  vec2 base_uv = UV;	
  vec4 albedo_tex = texture(texture_albedo,base_uv);
  albedoAux = albedo.rgb * albedo_tex.rgb;
  float intensity;
  intensity = dot(lightVec, normalize(NORMAL));
  if (intensity > 0.95)	ALBEDO = albedoAux*1.0;
  else if (intensity > 0.5) ALBEDO = albedoAux*0.6;
  else if (intensity > 0.25)  ALBEDO = albedoAux*0.4;
  else		ALBEDO = albedoAux*0.2;
}

void light(){	
  lightVec = LIGHT;
}
```

O shader acima foi rodado na game engine Godot em modelos 3D e o resultado é mostrado abaixo:

![Toon Shader](https://i.imgur.com/xu9X1FA.png)

Apenas a uva em destaque tem o toon shader, os outros alimentos tem o shader padrão. Vemos a discretização das cores do albedo da uva na imagem enquanto as outras comidas apresentam um visual mais metálico e brilhante.

Como podemos ver, é uma solução sólida para jogos em 3D e já bem famosa na indústria. Mas adiante testaremos outras soluções e como elas funcionariam se fossem usadas.

### K-Means
O segundo algoritmo foi simplesmente implementar um shader com o K-means visto em sala de aula. O código do shader é o seguinte:

```glsl
uniform int PaletteSize;
uniform float2 RandomPoints[100];

fixed4 frag (v2f i) : SV_Target {
    fixed4 basecol = tex2D(_MainTex, i.uv);
    fixed4 finalcol;
    float mindist = 10000000.0;
    for(int i = 0; i < PaletteSize; i++) {
        fixed4 paletteCol = tex2D(_MainTex, RandomPoints[i]);
        float dist = distance(basecol, paletteCol); 
        if(dist < mindist) {
            mindist = dist;
            finalcol = paletteCol;
        }
    }
    return finalcol;
}
```

Porém, esse shader depende de uma geração de paleta de cores externa, que é feito no seguinto código adicionado à textura onde a câmera renderiza a imagem do jogo (código implementado na game engine Unity 3D):

```c#
public class QuantizeFinalImage : MonoBehaviour {
  public Material mat;
  public int PaletteSize;
  public float PaletteChangeTime;

  void Start() {
    StartCoroutine(ChangePalette());
  }

  IEnumerator ChangePalette() {
    while (true) {
      var points = new List<Vector4>(PaletteSize);
      for (int i = 0; i < PaletteSize; i++)  {
        points.Add(new Vector4(Random.value, Random.value, 0, 0));
      }
      mat.SetInt("PaletteSize", PaletteSize);
      mat.SetVectorArray("RandomPoints", points);
      yield return new WaitForSeconds(PaletteChangeTime);
    }
  }

  void OnRenderImage(RenderTexture src, RenderTexture dst)  {
    Graphics.Blit(src, dst, mat);
  }
}
```
O efeito é bem estranho aos olhos, devido à mudança brusca de paleta que ocorre a cada 100ms. Abaixo segue um vídeo mostrando o efeito ocorrido:

https://streamable.com/frhdw

### Dithering

Uma forma de aproximar tonalidades que não estão presentes em uma certa paleta de cores é através da técnica de "dithering", por meio da qual uma difusão de pixels coloridos dentro da paleta produzem a ilusão de estarem representando essas outras cores.

![Roxo](https://upload.wikimedia.org/wikipedia/commons/6/6d/Dithering_example_red_blue.png)

Nesta figura, vemos que as cores azul e vermelho podem ser usadas para assemelharem-se visualmente à cor roxa.

Um dos algoritmos usados para produzir efeito é o de Floyd-Steinberg, que atinge o dithering usando a difusão de erros, de forma que o erro de quantização residual de cada pixel é transferido, parcialmente, aos seus pixels vizinhos.

O algoritmo de Floyd-Steinberg percorre os pixels da imagem da esquerda para a direita, de cima para baixo, e somente transfere os erros de quantização para os pixels seguintes (não altera os pixels já percorridos). Dessa forma, se um conjunto de pixels são sucessivamente arredondados para baixo, aumenta-se a chance de o próximo pixel ser arredondado para cima de tal forma que, na média, o erro de quantização tenda a zero.

Os coeficientes de difusão usados no algoritmo apresentam a propriedade de, caso o valor do pixel original esteja exatamente na metade entre as duas cores mais próximas disponíveis na paleta, o resultado do dithering é um padrão xadrez. Por exemplo, o cinza 50% seria aproximado para um padrão xadrez preto e branco.

![Gato](https://upload.wikimedia.org/wikipedia/commons/f/fd/Dithering_-_exemple.jpg)

Nesta imagem, vemos a imagem original do gato (à esquerda), uma imagem com paleta de cores reduzida, porém sem dithering (ao centro) e uma imagem com paleta de cores reduzida que faz uso de dithering (à direita). Percebe-se que a imagem da direita aproxima-se muito mais da original do que a do centro, mesmo fazendo uso da mesma paleta reduzida de cores. A do centro apenas aproxima a tonalidade de cada pixel à tonalidade mais próxima disponível na paleta, ao passo que a imagem da direita produz a difusão do erro de quantização residual para os pixels vizinhos (ao tirar melhor proveito dessa informação, permite que o erro de quantização tenda a zero , o que resulta em uma imagem mais fiel à original).
