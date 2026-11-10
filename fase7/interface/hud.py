import pygame

BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)


def formatar_tempo(quadros):
    """Converte quadros (60 por segundo) em mm:ss.d"""
    segundos = quadros / 60
    minutos = int(segundos // 60)
    return f"{minutos:02d}:{segundos - minutos * 60:04.1f}"


def texto(screen, fonte, msg, pos, cor=BRANCO, centralizar=False):
    """Escreve um texto com sombra preta para ficar legível sobre qualquer fundo."""
    sombra = fonte.render(msg, True, (0, 0, 0))
    principal = fonte.render(msg, True, cor)
    x, y = pos
    if centralizar:
        x -= principal.get_width() // 2
    screen.blit(sombra, (x + 1, y + 1))
    screen.blit(principal, (x, y))
    return principal.get_width()


def desenhar_coracao(screen, x, y, tam, cheio):
    cor = (235, 55, 75) if cheio else (70, 45, 55)
    r = tam // 4
    pygame.draw.circle(screen, cor, (x + r, y + r), r)
    pygame.draw.circle(screen, cor, (x + 3 * r, y + r), r)
    pygame.draw.polygon(screen, cor, [(x, y + r + 1), (x + 4 * r, y + r + 1), (x + 2 * r, y + 4 * r)])
    pygame.draw.polygon(screen, (20, 10, 15), [(x, y + r + 1), (x + 4 * r, y + r + 1), (x + 2 * r, y + 4 * r)], 1)


def desenhar_chave_icone(screen, x, y, cor):
    pygame.draw.circle(screen, cor, (x + 5, y + 6), 5, 2)
    pygame.draw.rect(screen, cor, (x + 9, y + 5, 10, 3))
    pygame.draw.rect(screen, cor, (x + 14, y + 8, 3, 4))
    pygame.draw.rect(screen, cor, (x + 18, y + 8, 3, 6))


def desenhar_gema_icone(screen, x, y):
    cx, cy = x + 7, y + 7
    pts = [(cx, cy - 7), (cx + 6, cy), (cx, cy + 7), (cx - 6, cy)]
    pygame.draw.polygon(screen, (80, 220, 255), pts)
    pygame.draw.polygon(screen, (20, 90, 130), pts, 1)


def desenhar_hud(screen, jogo, fonte):
    largura = screen.get_width()

    # --- vidas (canto superior esquerdo) ---
    for i in range(jogo.vidas_max):
        desenhar_coracao(screen, 10 + i * 24, 8, 20, i < jogo.vidas)

    # --- chave e gemas ---
    cor_chave = (255, 205, 40) if jogo.tem_chave else (95, 95, 105)
    desenhar_chave_icone(screen, 10, 36, cor_chave)
    desenhar_gema_icone(screen, 42, 36)
    texto(screen, fonte, f"{jogo.gemas_coletadas}/{len(jogo.gemas)}", (60, 36))

    # --- cronômetro (canto superior direito) ---
    t = formatar_tempo(jogo.quadros)
    texto(screen, fonte, t, (largura - 10 - fonte.size(t)[0], 8))

    # --- barra do açaí ---
    if jogo.player.acai_timer > 0:
        from personagem.player import ACAI_FRAMES
        frac = jogo.player.acai_timer / ACAI_FRAMES
        pygame.draw.rect(screen, (30, 10, 45), (10, 58, 104, 10))
        pygame.draw.rect(screen, (190, 90, 255), (12, 60, int(100 * frac), 6))
        pygame.draw.rect(screen, (235, 200, 255), (10, 58, 104, 10), 1)
        texto(screen, fonte, "Açaí!", (120, 54), (225, 170, 255))

    # --- mensagem temporária no meio da tela ---
    if jogo.mensagem_timer > 0:
        texto(screen, fonte, jogo.mensagem, (largura // 2, 92), AMARELO, centralizar=True)


def desenhar_tela_derrota(screen, jogo, fonte_grande, fonte):
    largura, altura = screen.get_size()
    screen.fill((100, 0, 0))
    texto(screen, fonte_grande, "VOCÊ PERDEU TODAS AS VIDAS!", (largura // 2, altura // 2 - 50), BRANCO, True)
    texto(screen, fonte, f"Tempo: {formatar_tempo(jogo.quadros)}   Gemas: {jogo.gemas_coletadas}/{len(jogo.gemas)}",
          (largura // 2, altura // 2 - 5), (255, 220, 220), True)
    texto(screen, fonte, "Aperte R para tentar de novo", (largura // 2, altura // 2 + 30), BRANCO, True)


def desenhar_tela_vitoria(screen, jogo, fonte_grande, fonte):
    largura, altura = screen.get_size()
    screen.fill((0, 0, 0))
    cx = largura // 2
    texto(screen, fonte_grande, "PARABÉNS! VOCÊ ZEROU O JOGO!", (cx, 70), AMARELO, True)

    total = len(jogo.gemas)
    texto(screen, fonte, f"Tempo: {formatar_tempo(jogo.quadros)}", (cx, 130), BRANCO, True)
    texto(screen, fonte, f"Gemas: {jogo.gemas_coletadas}/{total}", (cx, 155), (120, 230, 255), True)
    texto(screen, fonte, f"Vidas restantes: {jogo.vidas}/{jogo.vidas_max}", (cx, 180), (255, 120, 140), True)

    if jogo.gemas_coletadas == total:
        texto(screen, fonte, "Todas as gemas! Perfeito!", (cx, 215), (255, 230, 120), True)
    else:
        texto(screen, fonte, "Será que dá pra pegar todas as gemas?", (cx, 215), (200, 200, 200), True)

    if jogo.melhor_tempo is not None:
        texto(screen, fonte,
              f"Recorde de hoje: {formatar_tempo(jogo.melhor_tempo)}  |  {jogo.melhor_gemas} gemas",
              (cx, 245), (180, 255, 180), True)
    texto(screen, fonte, "Aperte R para jogar de novo", (cx, 290), BRANCO, True)
