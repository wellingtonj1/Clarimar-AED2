Inicialmente é feito a leitura e extração dos frames do vídeo, 

Para cada frame é aplicado uma rotação de 90 graus antihorario e é aplicado um filtro de sharpening para dar nitidez a imagem, após isso é aplicado uma correção de contraste, e por fim é aplicado uma correção de cor e assim é enviado a função de detecção do adubo.

Para a detecção do adubo é utilizado o algoritmo de detecção de bordas de Canny, onde é utilizado uma matriz de convolução para detectar as bordas do adubo, inicialmente é aplicado uma correção de histograma, após isso é utilizado um filtro de dilatação para aumentar o tamanho das bordas e assim aumentar a precisão da detecção. Após isso é feito a detecção de contornos, onde é utilizado o algoritmo de detecção de contornos de canny, onde é utilizado uma matriz de convolução para detectar os contornos do adubo, após isso é utilizado um filtro de dilatação para aumentar o tamanho dos contornos e assim aumentar a precisão da detecção.

Após isso é ultilizado a função grabcut passando a mascara do adubo como parametro, depois é aplicado a imagem do adubo detectado para a imagem original. Por fim é feito a leitura e extração dos frames do vídeo, e é feito a escrita do vídeo com o adubo detectado.
