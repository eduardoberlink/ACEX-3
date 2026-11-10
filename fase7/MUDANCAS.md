# Fase 6 – o que foi implementado

Rodar: `python fase6/fase6.py` (a partir da raiz do ACEX) **ou** `python fase6.py` (dentro da pasta).

**Controles:** A/D mover · W/Espaço pular (segure = mais alto) · E dash · F purificar · R reiniciar (na tela final)

## Onde está cada melhoria

| # | Melhoria | Onde |
|---|----------|------|
| 1 | Pulo na parede | `personagem/player.py` (`_pulo_parede`, `_contato_parede`, deslize em `update`) · `objetos/plataformas.py` (`Parede`) · torre em `fase6.py` |
| 2 | Plataformas móveis | `objetos/plataformas.py` (`PlataformaMovel`) · `Player._ser_levado` · 3 plataformas no setor 4 |
| 3 | Purificar capivaras (F) | `Player.atacar/hitbox_ataque` · `inimigos/enemy.py` (`receber_purificacao`, sprite curado) · `Jogo.verificar_golpe` |
| 4 | Chave e porta trancada | `objetos/itens.py` (`Chave`) · `objetos/porta.py` (`trancada`) · `Jogo.verificar_itens/verificar_porta` |
| 5 | Açaí | `objetos/itens.py` (`Acai`) · `Player.ativar_acai` (8 s, velocidade 6, 3 pulos, brilho roxo) |
| 6 | Altura de pulo variável | `Player.update` passo 4 (`CORTE_PULO`) |
| 7 | Coyote time + buffer | `COYOTE_FRAMES`, `BUFFER_FRAMES` em `player.py`; cair da borda deixa só 1 pulo |
| 8 | Dash suave | `DASH_VEL x DASH_FRAMES` (9 px x 6 quadros), sem cair, com rastro |
| 9 | Velocidade máxima de queda | `VEL_QUEDA_MAX = 11` |
| 10 | Pisar nos inimigos | `Jogo.verificar_inimigos` (purifica + quique + recupera dash) |
| 11 | Checkpoints | `objetos/checkpoint.py` · bandeiras nos setores 3 e 4 |
| 12 | Vidas + invencibilidade | `Jogo.perder_vida`, `Player.levar_dano` (3 vidas, 1,5 s piscando, empurrão) |
| 13 | Gemas + cronômetro | `objetos/itens.py` (`Gema`) · `interface/hud.py` · 8 gemas, tela de vitória com resultado e recorde |

Todas as constantes de "sensação" (gravidade, tempos, distâncias) ficam no começo de `personagem/player.py`.

## Roteiro da fase (para jogar/apresentar)
1. **Setor 1:** a primeira capivara ensina o golpe (F) e a pisada.
2. **Setor 3:** purifique a capivara da torre, suba nela, entre no poço e suba pulando de parede em parede até a **chave**.
3. **Setor 4:** pegue o **açaí** (o atalho por cima só é alcançável com o 3º pulo) ou atravesse as plataformas móveis.
4. Passe pelo guardião (3 golpes/pisadas, ou corra) e abra a **porta**.

## Notas importantes
- **Escalada (segurar W):** o código antigo não funcionava (o `colliderect` dava `False` com o jogador só encostado na parede). Foi removida e substituída pelo pulo na parede, que só vale nas `Parede` (troncos da torre).
- **Física do pulo preservada:** 1 pulo = 64 px, 2 = 128 px, 3 = 192 px (igual ao original); o nível foi desenhado em cima disso.
- A plataforma aérea do setor 3 (y=200) continua inalcançável, como já era; é só obstáculo/cenário.
- Os caminhos dos assets agora são relativos ao arquivo (`support.caminho_asset`), então o jogo abre de qualquer pasta.
