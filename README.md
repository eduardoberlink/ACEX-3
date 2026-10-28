# ACEX - Jogo de plataforma em fases

Cada fase é um jogo completo e independente. A ideia do projeto é a
complexidade aumentar de uma fase para a outra, então cada pasta guarda
o código **daquele estágio**.

| Fase | O que entra de novo |
|------|---------------------|
| 1 | Loop do jogo, gravidade, pulo, chão e porta de saída |
| 2 | Lista de plataformas e colisão por todos os lados |
| 3 | Inimigo que patrulha e tela de "você morreu" |
| 4 | Pulo duplo, dash (E) e escalada (W na parede) |
| 5 | Mundo maior que a tela, câmera, imagem de fundo e `config.py` |
| 6 | Sprites e animação, espinhos, vários inimigos, mapa em `nivel.py`, classe `Jogo` |

## Como rodar

Uma vez só, na pasta do projeto (Windows):

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Depois, para jogar uma fase:

```
python fase1/fase1.py
```

(Troque `fase1` pela fase que quiser. Funciona de qualquer pasta.)

## Controles

A/D andam, W ou Espaço pulam e R reinicia depois de vencer ou morrer.
A partir da fase 4: E dá dash e W encostado numa parede escala.
