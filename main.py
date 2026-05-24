import pygame
import sys
import random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_RETURN, K_BACKSPACE

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Histogramas")

font = pygame.font.Font(None, 24)
font_grande = pygame.font.Font(None, 36)

lista1 = []
for i in range(60):
    lista1.append(random.randint(10, 100))

num_cat1 = 5

lista2_base = [
    100, 120, 130, 120, 150, 100, 160, 200, 190, 110, 115, 125, 135, 170, 130
]
num_cat2 = 3
min2 = min(lista2_base)
max2 = max(lista2_base)
tam_faixa2 = (max2 - min2) / num_cat2
lista2 = []
sobra = len(lista2_base)
for i in range(num_cat2):
    lim_inf = min2 + i * tam_faixa2
    lim_sup = lim_inf + tam_faixa2
    if i == num_cat2 - 1:
        qtd = sobra
    else:
        qtd = random.randint(0, sobra - (num_cat2 - i - 1))
    sobra -= qtd
    for j in range(qtd):
        if i == num_cat2 - 1:
            lista2.append(max2)
        else:
            lista2.append(random.uniform(lim_inf, lim_sup - 0.01))

lista3 = []
num_cat3 = 4

def contabiliza(nums, num_cat):
    num_min = min(nums)
    num_max = max(nums)
    tam_cat = (num_max - num_min) / num_cat
    lista_total = [0] * num_cat
    for n in nums:
        if n == num_max:
            lista_total[-1] += 1
            continue
        for i in range(num_cat):
            lim_inf = num_min + i * tam_cat
            lim_sup = lim_inf + tam_cat
            if lim_inf <= n < lim_sup:
                lista_total[i] += 1
                break
    return lista_total, num_min, num_max

def gera_cores(num_cat):
    cores = []
    for i in range(num_cat):
        cores.append((random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
    return cores

cores1 = gera_cores(num_cat1)
cores2 = gera_cores(num_cat2)
cores3 = gera_cores(num_cat3)

def desenha_histograma(lista_total, num_cat, num_min, num_max, cores, titulo):
    screen.fill((0, 0, 0))

    txt = font_grande.render(titulo, True, (255, 255, 255))
    screen.blit(txt, (10, 10))

    orig_x = 60
    orig_y = 520
    larg_area = 700
    alt_area = 420

    pygame.draw.line(screen, (255, 255, 255), (orig_x, orig_y), (orig_x, orig_y - alt_area), 2)

    max_contagem = max(lista_total) if max(lista_total) > 0 else 1
    for i in range(6):
        valor = round(max_contagem * i / 5)
        py = orig_y - int(alt_area * i / 5)
        pygame.draw.line(screen, (255, 255, 255), (orig_x - 4, py), (orig_x, py), 1)
        txt_y = font.render(str(valor), True, (255, 255, 255))
        screen.blit(txt_y, (orig_x - txt_y.get_width() - 6, py - 8))

    pygame.draw.line(screen, (255, 255, 255), (orig_x, orig_y), (orig_x + larg_area, orig_y), 2)

    larg_barra = larg_area // num_cat
    tam_cat = (num_max - num_min) / num_cat

    for i in range(num_cat):
        contagem = lista_total[i]
        bx = orig_x + i * larg_barra + 4
        bw = larg_barra - 8
        bh = int(alt_area * contagem / max_contagem) if max_contagem > 0 else 0
        by = orig_y - bh

        pygame.draw.rect(screen, cores[i], (bx, by, bw, bh))

        txt_val = font.render(str(contagem), True, (255, 255, 255))
        screen.blit(txt_val, (bx + bw // 2 - txt_val.get_width() // 2, by - 20))

        lim_inf = num_min + i * tam_cat
        lim_sup = lim_inf + tam_cat
        label = f"{lim_inf:.0f}-{lim_sup:.0f}"
        txt_x = font.render(label, True, (255, 255, 255))
        screen.blit(txt_x, (bx + bw // 2 - txt_x.get_width() // 2, orig_y + 6))

    txt_nav = font.render("<< seta esq    seta dir >>", True, (150, 150, 150))
    screen.blit(txt_nav, (10, 575))


def desenha_tela_input(texto_digitado, lista3, erro):
    screen.fill((0, 0, 0))

    txt = font_grande.render("Histograma 3 - digite os numeros", True, (255, 255, 255))
    screen.blit(txt, (10, 10))

    pygame.draw.rect(screen, (255, 255, 255), (10, 60, 400, 30), 1)
    txt_campo = font.render(texto_digitado + "_", True, (255, 255, 255))
    screen.blit(txt_campo, (15, 65))

    inst = font.render("ENTER para adicionar", True, (200, 200, 200))
    screen.blit(inst, (10, 100))

    nums_str = str([round(n, 1) for n in lista3]) if lista3 else "(nenhum)"
    txt_lista = font.render("lista: " + nums_str, True, (200, 200, 200))
    screen.blit(txt_lista, (10, 130))

    if erro:
        txt_erro = font.render(erro, True, (255, 0, 0))
        screen.blit(txt_erro, (10, 160))

    if len(lista3) >= 2:
        txt_ver = font.render("seta esquerda para ver o grafico", True, (0, 255, 0))
        screen.blit(txt_ver, (10, 190))

    txt_nav = font.render("<< seta esq    seta dir >>", True, (150, 150, 150))
    screen.blit(txt_nav, (10, 575))


histograma_atual = 0
modo_input = False
texto_input = ""
mensagem_erro = ""

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if histograma_atual == 2 and modo_input:
                    if len(lista3) >= 2:
                        modo_input = False
                else:
                    histograma_atual = (histograma_atual - 1) % 3
                    if histograma_atual == 2 and len(lista3) < 2:
                        modo_input = True

            elif event.key == K_RIGHT:
                histograma_atual = (histograma_atual + 1) % 3
                if histograma_atual == 2 and len(lista3) < 2:
                    modo_input = True

            elif modo_input:
                if event.key == K_RETURN:
                    try:
                        valor = float(texto_input)
                        lista3.append(valor)
                        cores3 = gera_cores(num_cat3)
                        texto_input = ""
                        mensagem_erro = ""
                    except:
                        mensagem_erro = "numero invalido!"
                        texto_input = ""
                elif event.key == K_BACKSPACE:
                    texto_input = texto_input[:-1]
                else:
                    if event.unicode in "0123456789.,":
                        texto_input += event.unicode.replace(",", ".")

    if histograma_atual == 0:
        totais1, min1, max1 = contabiliza(lista1, num_cat1)
        desenha_histograma(totais1, num_cat1, min1, max1, cores1,
                           "hist 1 - aleatorio")

    elif histograma_atual == 1:
        totais2, min2c, max2c = contabiliza(lista2, num_cat2)
        desenha_histograma(totais2, num_cat2, min2c, max2c, cores2,
                           "hist 2 - estatico")

    elif histograma_atual == 2:
        if modo_input or len(lista3) < 2:
            modo_input = True
            desenha_tela_input(texto_input, lista3, mensagem_erro)
        else:
            totais3, min3, max3 = contabiliza(lista3, num_cat3)
            desenha_histograma(totais3, num_cat3, min3, max3, cores3,
                               "hist 3 - usuario")

    pygame.display.update()