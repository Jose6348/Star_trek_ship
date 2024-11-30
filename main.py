import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import random


# Configuração inicial do Pygame e OpenGL
pygame.init()
screen = pygame.display.set_mode((1300, 700), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Star Trek USS Ganges - ZEZINHO")
clock = pygame.time.Clock()
glutInit()

# Configurações de rotação
rotacao_x = 0
rotacao_y = 0

# Variáveis
posicao_nave_x = -3
posicao_nave_y = -2
posicao_nave_z = 10
velocidade_warp = False
buraco_negro_ativo = False

tempo_para_dobra = 0
luz_dobra_ativa = False
intensidade_luz = 0

# Variáveis para aceleração
velocidade_x = 0
velocidade_y = 0
aceleracao = 0.005
desaceleracao = 0.98
velocidade_max = 0.5


def reiniciar_simulacao():
    global rotacao_x, rotacao_y, posicao_nave_x, posicao_nave_y, posicao_nave_z
    global velocidade_warp, buraco_negro_ativo, tempo_para_dobra, luz_dobra_ativa
    global intensidade_luz, velocidade_x, velocidade_y

    # Reinicia todas as variáveis
    rotacao_x = 0
    rotacao_y = 0
    posicao_nave_x = -3
    posicao_nave_y = -2
    posicao_nave_z = 10
    velocidade_warp = False
    buraco_negro_ativo = False
    tempo_para_dobra = 0
    luz_dobra_ativa = False
    intensidade_luz = 0
    velocidade_x = 0
    velocidade_y = 0
    print("Simulação reiniciada")


def configurar_iluminacao():
    # Ativar iluminação
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Configurar a posição da luz principal
    luz_posicao = [10.0, 15.0, 10.0, 1.0]
    luz_ambiente = [0.3, 0.3, 0.3, 1.0]
    luz_difusa = [0.9, 0.9, 0.8, 1.0]
    luz_especular = [1.0, 1.0, 0.9, 1.0]

    # Aplicar as configurações de luz principal
    glLightfv(GL_LIGHT0, GL_POSITION, luz_posicao)
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)

    # Adicionar uma nova luz
    glEnable(GL_LIGHT1)
    luz_estrelas_posicao = [-15.0, 20.0, -10.0, 1.0]
    luz_estrelas_cor = [0.2, 0.2, 0.8, 1.0]

    glLightfv(GL_LIGHT1, GL_POSITION, luz_estrelas_posicao)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, luz_estrelas_cor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, luz_estrelas_cor)

    # Habilitar material de cor
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


def configurar_material():
    brilho_especular = [1.0, 1.0, 1.0, 1.0]
    glMaterialfv(GL_FRONT, GL_SPECULAR, brilho_especular)
    glMaterialfv(GL_FRONT, GL_SHININESS, 100)

    brilho_ambiente = [0.2, 0.2, 0.2, 1.0]
    glMaterialfv(GL_FRONT, GL_AMBIENT, brilho_ambiente)

    brilho_difuso = [0.6, 0.6, 0.6, 1.0]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, brilho_difuso)


def configurar_luz_dobra():
    global intensidade_luz

    glEnable(GL_LIGHT1)
    luz_posicao = [posicao_nave_x, posicao_nave_y, posicao_nave_z, 1.0]  # Posicione a luz na nave
    luz_cor = [intensidade_luz, intensidade_luz, intensidade_luz, 1.0]

    glLightfv(GL_LIGHT1, GL_POSITION, luz_posicao)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, luz_cor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, luz_cor)



def animar_ponto_dobra():
    global portal_raio, posicao_nave_z, velocidade_warp

    if 'portal_raio' not in globals():
        portal_raio = 10  # Raio inicial do portal

    if velocidade_warp:
        glPushMatrix()
        glTranslatef(-2, 0, -50)  # Posição do portal
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBegin(GL_TRIANGLE_FAN)
        glColor4f(1.0, 1.0, 1.0, 0.8)
        glVertex3f(0, 0, 0)

        #Círculo que diminui gradualmente
        for angle in range(0, 361, 10):
            x = math.cos(math.radians(angle)) * portal_raio
            y = math.sin(math.radians(angle)) * portal_raio
            glColor4f(0.2, 0.6, 1.0, 0.2)  # Cor nas bordas
            glVertex3f(x, y, 0)

        glEnd()
        glDisable(GL_BLEND)
        glPopMatrix()

        if posicao_nave_z <= -50:  # Começa a fechar quando a nave está longe o suficiente
            portal_raio -= 0.3  # Ajustar o valor para sincronizar
            if portal_raio <= 0:  # Quando o portal fecha completamente
                portal_raio = 0  # Mantém o portal fechado

# Reiniciar o portal
def reiniciar_simulacao():
    global rotacao_x, rotacao_y, posicao_nave_x, posicao_nave_y, posicao_nave_z
    global velocidade_warp, buraco_negro_ativo, tempo_para_dobra, luz_dobra_ativa
    global intensidade_luz, velocidade_x, velocidade_y, portal_raio

    # Reinicie todas as variáveis para seus valores iniciais
    rotacao_x = 0
    rotacao_y = 0
    posicao_nave_x = -3
    posicao_nave_y = -2
    posicao_nave_z = 10
    velocidade_warp = False
    buraco_negro_ativo = False
    tempo_para_dobra = 0
    luz_dobra_ativa = False
    intensidade_luz = 0
    portal_raio = 10  # Reinicia o raio do portal
    velocidade_x = 0
    velocidade_y = 0
    print("Simulação reiniciada")  # Depuração






# Inicialização do OpenGL
def inicializar():
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (1300 / 700), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -15)


    #Chamada de funções
    configurar_iluminacao()
    configurar_material()
    configurar_luz_dobra()




#Variáveis de estrelas e planetas

posicoes_estrelas = [(random.uniform(-20, 20), random.uniform(-20, 20), random.uniform(-30, 30)) for _ in range(600)]

posicoes_planetas = [
    (-30, 20, -70),  # Planeta 1
    (30, 20, -70),  # Planeta 2
    (30, -10, -40),    # Planeta 3
    (10, -12, -20), # Planeta 4
    (-30, -10, -30)    # Planeta 5
]

cores_planetas = [
    (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)) for _ in range(5)
]

def desenhar_estrelas():
    global velocidade_warp, posicoes_estrelas
    glPointSize(3)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)  # Cor estrelas
    for i, (x, y, z) in enumerate(posicoes_estrelas):
        if velocidade_warp:
            # Movimenta as estrelas para criar o efeito de "velocidade estelar"
            z += 0.5
            if z > 0:
                z = random.uniform(-30, -100)
            posicoes_estrelas[i] = (x, y, z)
        glVertex3f(x, y, z)
    glEnd()

def desenhar_planetas():
    for (x, y, z), color in zip(posicoes_planetas, cores_planetas):
        glPushMatrix()
        glTranslatef(x, y, z)  # Posição dos planetas
        glColor3f(*color)
        gluSphere(gluNewQuadric(), 4, 32, 32)  # Desenha o planeta
        glPopMatrix()

def desenhar_buraco_negro():
    # Defina os ângulos de rotação para a inclinação
    rotation_angle_x = 30  # Ângulo de rotação no eixo X
    rotation_angle_y = 45  # Ângulo de rotação no eixo Y

    # Singularidade do Buraco Negro (Esfera Negra)
    glPushMatrix()
    glTranslatef(0, 8, -70)
    glRotatef(rotation_angle_x, 1, 0, 0)
    glRotatef(rotation_angle_y, 0, 1, 0)
    glColor3f(0.1, 0.1, 0.1)  # Cor preta
    gluSphere(gluNewQuadric(), 5, 64, 64)  # Uma esfera
    glPopMatrix()

    # Disco de Acreção
    glPushMatrix()
    glTranslatef(0, 7, -60)
    glRotatef(rotation_angle_x, 0, 1, 0)
    glRotatef(rotation_angle_y, 1, 0, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_TRIANGLE_STRIP)
    for angle in range(0, 361, 5):
        # Efeito de gradiente para o disco de acreção
        glColor4f(1.0, 0.5, 0.0, 0.6)  # Cor alaranjada
        x_inner = math.cos(math.radians(angle)) * 6
        y_inner = math.sin(math.radians(angle)) * 6
        glVertex3f(x_inner, y_inner, 0)

        glColor4f(0.3, 0.0, 0.0, 0.1)
        x_outer = math.cos(math.radians(angle)) * 15
        y_outer = math.sin(math.radians(angle)) * 15
        glVertex3f(x_outer, y_outer, 0)
    glEnd()
    glDisable(GL_BLEND)
    glPopMatrix()

# Função para animar a nave
def animar_nave():
    global posicao_nave_z, velocidade_warp, intensidade_luz

    if posicao_nave_z > -20 and not velocidade_warp:  # Fase inicial
        posicao_nave_z -= 0.1
        intensidade_luz = max(0, intensidade_luz - 0.01)
    elif posicao_nave_z <= -10 and not velocidade_warp:
        velocidade_warp = True
        intensidade_luz = 1.0
    if velocidade_warp:
        posicao_nave_z -= 2
        intensidade_luz = min(1.5, intensidade_luz + 0.05)

        if posicao_nave_z < -90:  # Quando a nave se aproxima do fim
            intensidade_luz = max(0, intensidade_luz - 0.1)
            if posicao_nave_z < -120:
                velocidade_warp = False
                posicao_nave_z = -120
                intensidade_luz = 0  # Desliga a luz



def lidar_com_entrada():
    global posicao_nave_x, posicao_nave_y, velocidade_x, velocidade_y

    keys = pygame.key.get_pressed()

    # Aceleração teclas
    if keys[K_a]:
        velocidade_x -= aceleracao
    if keys[K_d]:
        velocidade_x += aceleracao
    if keys[K_w]:
        velocidade_y += aceleracao
    if keys[K_s]:
        velocidade_y -= aceleracao

    velocidade_x = max(min(velocidade_x, velocidade_max), -velocidade_max)
    velocidade_y = max(min(velocidade_y, velocidade_max), -velocidade_max)

    velocidade_x *= desaceleracao
    velocidade_y *= desaceleracao

    posicao_nave_x += velocidade_x
    posicao_nave_y += velocidade_y


def escalar_nave():
    global posicao_nave_z
    escala_base = 0.3
    escala_maxima = 1.0
    fator_suavidade = 0.05

    escala_atual = escala_base + (escala_maxima - escala_base) * (1 - math.exp(-fator_suavidade * (posicao_nave_z + 15)))
    escala_atual = max(escala_base, min(escala_atual, escala_maxima))  # Limita a escala entre os valores mínimo e máximo

    glScalef(escala_atual, escala_atual, escala_atual)


def desenhar_texto(text, position, font_size=30):
    glPushMatrix()
    glColor3f(1, 1, 1)  # Cor branca para o texto
    glRasterPos2f(position[0], position[1])
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glPopMatrix()

#Funções das formas geométricas.

def desenhar_detalhes_do_corpo():

    # Linha central no corpo da nave
    glColor3f(0.2, 0.2, 0.2)  # Cor cinza escuro para contraste
    glBegin(GL_LINES)
    glVertex3f(-1.0, 0.0, -2.5)
    glVertex3f(1.0, 0.0, -2.5)
    glEnd()

    # Painéis laterais
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-1.8, 0.5, -2.0)  # Painel esquerdo
    glVertex3f(-1.6, 0.5, -2.0)
    glVertex3f(-1.6, -0.5, -2.0)
    glVertex3f(-1.8, -0.5, -2.0)

    glVertex3f(1.6, 0.5, -2.0)  # Painel direito
    glVertex3f(1.8, 0.5, -2.0)
    glVertex3f(1.8, -0.5, -2.0)
    glVertex3f(1.6, -0.5, -2.0)
    glEnd()

    # Placas horizontais na parte superior
    glColor3f(0.6, 0.6, 0.6)  # Cor metálica clara
    glBegin(GL_QUADS)
    glVertex3f(-0.5, 1.0, -1.0)
    glVertex3f(0.5, 1.0, -1.0)
    glVertex3f(0.5, 1.0, -0.5)
    glVertex3f(-0.5, 1.0, -0.5)

    glVertex3f(-0.5, 1.0, -2.0)
    glVertex3f(0.5, 1.0, -2.0)
    glVertex3f(0.5, 1.0, -1.5)
    glVertex3f(-0.5, 1.0, -1.5)
    glEnd()

    # Reforços na traseira
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_LINES)
    glVertex3f(-1.5, -0.8, -3.5)  # Esquerda
    glVertex3f(-1.2, -0.6, -3.0)
    glVertex3f(1.5, -0.8, -3.5)   # Direita
    glVertex3f(1.2, -0.6, -3.0)
    glEnd()


def desenhar_detalhes_dos_motores():

    glColor3f(0.5, 0.5, 0.5)  # Cinza metálico
    glBegin(GL_QUADS)

    # Aleta esquerda
    glVertex3f(-2.8, -0.5, 3.0)
    glVertex3f(-2.4, -0.5, 3.0)
    glVertex3f(-2.4, -0.5, 2.5)
    glVertex3f(-2.8, -0.5, 2.5)

    # Aleta direita
    glVertex3f(2.8, -0.5, 3.0)
    glVertex3f(2.4, -0.5, 3.0)
    glVertex3f(2.4, -0.5, 2.5)
    glVertex3f(2.8, -0.5, 2.5)

    glEnd()

    # Padrões na lateral dos motores
    glColor3f(0.2, 0.2, 0.2)  # Cinza escuro
    glBegin(GL_LINES)

    # Motor esquerdo
    for offset in [0.1, 0.3, 0.5]:
        glVertex3f(-2.5, -1.0 + offset, 2.8)
        glVertex3f(-2.5, -1.0 + offset, 2.5)

    # Motor direito
    for offset in [0.1, 0.3, 0.5]:
        glVertex3f(2.5, -1.0 + offset, 2.8)
        glVertex3f(2.5, -1.0 + offset, 2.5)

    glEnd()

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.0, 0.6, 1.0, 0.8)  # Azul brilhante
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(-2.5, -1.0, 2.0)  # Centro da luz do motor esquerdo
    for angle in range(0, 361, 10):
        x = math.cos(math.radians(angle)) * 0.3 - 2.5
        y = math.sin(math.radians(angle)) * 0.3 - 1.0
        glVertex3f(x, y, 2.0)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(2.5, -1.0, 2.0)  # Centro da luz do motor direito
    for angle in range(0, 361, 10):
        x = math.cos(math.radians(angle)) * 0.3 + 2.5
        y = math.sin(math.radians(angle)) * 0.3 - 1.0
        glVertex3f(x, y, 2.0)
    glEnd()

    glDisable(GL_BLEND)


def desenhar_detalhes_das_asas():

    # Painéis na asa esquerda
    glPushMatrix()
    glTranslatef(-1.3, -0.4, 0)  # Posição base da asa esquerda
    glRotatef(15, 0, 0, 1)
    glColor3f(0.4, 0.4, 0.4)  # Cor dos painéis
    glBegin(GL_QUADS)

    # Painel 1
    glVertex3f(-0.5, -0.1, 0.2)
    glVertex3f(0.5, -0.1, 0.2)
    glVertex3f(0.5, 0.1, 0.2)
    glVertex3f(-0.5, 0.1, 0.2)

    # Painel 2
    glVertex3f(-0.3, -0.1, -0.5)
    glVertex3f(0.3, -0.1, -0.5)
    glVertex3f(0.3, 0.1, -0.5)
    glVertex3f(-0.3, 0.1, -0.5)

    glEnd()
    glPopMatrix()

    # Painéis na asa direita
    glPushMatrix()
    glTranslatef(1.3, -0.4, 0)  # Posição base da asa direita
    glRotatef(-15, 0, 0, 1)
    glColor3f(0.4, 0.4, 0.4)  # Cor dos painéis
    glBegin(GL_QUADS)

    # Painel 1
    glVertex3f(-0.5, -0.1, 0.2)
    glVertex3f(0.5, -0.1, 0.2)
    glVertex3f(0.5, 0.1, 0.2)
    glVertex3f(-0.5, 0.1, 0.2)

    # Painel 2
    glVertex3f(-0.3, -0.1, -0.5)
    glVertex3f(0.3, -0.1, -0.5)
    glVertex3f(0.3, 0.1, -0.5)
    glVertex3f(-0.3, 0.1, -0.5)

    glEnd()
    glPopMatrix()

    # Reforços estruturais
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)  # Cinza claro para reforços

    # Asa esquerda
    glBegin(GL_LINES)
    glVertex3f(-1.8, -0.4, 0.2)
    glVertex3f(-1.3, -0.4, -0.8)
    glEnd()

    # Asa direita
    glBegin(GL_LINES)
    glVertex3f(1.8, -0.4, 0.2)
    glVertex3f(1.3, -0.4, -0.8)
    glEnd()

    glPopMatrix()

def desenhar_detalhes_da_cabine():

    # Janelas superiores da cabine
    glPushMatrix()
    glTranslatef(0, 1, 3.5)  # Posição das janelas superiores
    glColor3f(0.2, 0.2, 0.2)  # Cor cinza escuro para contraste
    glBegin(GL_QUADS)

    # Janela principal
    glVertex3f(-0.5, 0.2, 0.1)
    glVertex3f(0.5, 0.2, 0.1)
    glVertex3f(0.4, 0.5, -0.1)
    glVertex3f(-0.4, 0.5, -0.1)

    # Janela lateral esquerda
    glVertex3f(-0.5, 0.2, 0.1)
    glVertex3f(-0.7, 0.2, -0.2)
    glVertex3f(-0.6, 0.4, -0.3)
    glVertex3f(-0.4, 0.5, -0.1)

    # Janela lateral direita
    glVertex3f(0.5, 0.2, 0.1)
    glVertex3f(0.7, 0.2, -0.2)
    glVertex3f(0.6, 0.4, -0.3)
    glVertex3f(0.4, 0.5, -0.1)

    glEnd()
    glPopMatrix()

    # Luzes frontais
    glPushMatrix()
    glTranslatef(0, 0.6, 4.5)  # Posição da luz frontal
    glColor3f(1.0, 1.0, 0.8)  # Amarelo claro
    glBegin(GL_TRIANGLES)

    # Luz principal
    glVertex3f(-0.2, -0.1, 0.1)
    glVertex3f(0.2, -0.1, 0.1)
    glVertex3f(0, 0.1, 0.3)

    glEnd()
    glPopMatrix()

    # Adicionar contornos à cabine
    glPushMatrix()
    glTranslatef(0, 0.8, 3.2)  # Base do contorno
    glColor3f(0.5, 0.5, 0.5)  # Cinza metálico
    glBegin(GL_LINE_LOOP)

    # Contorno frontal
    glVertex3f(-0.6, 0.0, 0.5)
    glVertex3f(0.6, 0.0, 0.5)
    glVertex3f(0.4, 0.3, 0.3)
    glVertex3f(-0.4, 0.3, 0.3)

    glEnd()
    glPopMatrix()


def desenhar_asa_curva(radius, width, depth):
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_TRIANGLE_STRIP)

    # Criar a curvatura usando um meio-círculo
    for angle in range(0, 181, 10):
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))

        # Ajustar o tamanho da asa
        glVertex3f(x * width, y, depth / 1)  # Vértice superior
        glVertex3f(x * width, y, -depth / 1)  # Vértice inferior

    glEnd()


def desenhar_meia_base_piramide():

    glBegin(GL_QUADS)
    glColor3f(0.5, 0.1, 0)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.0)  # Corta a base
    glEnd()


def desenhar_cilindro_solido(x, y, z, base_radius, top_radius, height, color):
    glPushMatrix()
    glColor3f(*color)
    glTranslatef(x, y, z)

    # Criando o objeto para o cilindro e os discos
    quadric = gluNewQuadric()

    # Desenhando o cilindro
    gluCylinder(quadric, base_radius, top_radius, height, 32, 32)

    # Desenhando as tampas para tornar o cilindro sólido
    glPushMatrix()
    glRotatef(180, 1, 0, 0)
    gluDisk(quadric, 0, base_radius, 32, 1)
    glPopMatrix()

    glTranslatef(0, 0, height)
    gluDisk(quadric, 0, top_radius, 32, 1)

    glPopMatrix()


def desenhar_cuboide(width, height, depth, color):
    w, h, d = width / 2, height / 2, depth / 2
    glColor3f(*color)
    glBegin(GL_QUADS)

    glVertex3f(-w, -h, d)  # Inferior esquerdo
    glVertex3f(w, -h, d)  # Inferior direito
    glVertex3f(w, h, d)  # Superior direito
    glVertex3f(-w, h, d)  # Superior esquerdo

    # Trás (z = -d)
    glVertex3f(-w, -h, -d)  # Inferior esquerdo
    glVertex3f(w, -h, -d)  # Inferior direito
    glVertex3f(w, h, -d)  # Superior direito
    glVertex3f(-w, h, -d)  # Superior esquerdo

    # Direita (x = +w)
    glVertex3f(w, -h, -d)  # Inferior esquerdo
    glVertex3f(w, h, -d)  # Superior esquerdo
    glVertex3f(w, h, d)  # Superior direito
    glVertex3f(w, -h, d)  # Inferior direito

    # Esquerda (x = -w)
    glVertex3f(-w, -h, -d)  # Inferior direito
    glVertex3f(-w, h, -d)  # Superior direito
    glVertex3f(-w, h, d)  # Superior esquerdo
    glVertex3f(-w, -h, d)  # Inferior esquerdo

    # Topo (y = +h)
    glVertex3f(-w, h, -d)  # Traseiro esquerdo
    glVertex3f(w, h, -d)  # Traseiro direito
    glVertex3f(w, h, d)  # Frontal direito
    glVertex3f(-w, h, d)  # Frontal esquerdo

    # Fundo (y = -h)
    glVertex3f(-w, -h, -d)  # Traseiro esquerdo
    glVertex3f(w, -h, -d)  # Traseiro direito
    glVertex3f(w, -h, d)  # Frontal direito
    glVertex3f(-w, -h, d)  # Frontal esquerdo

    glEnd()

    # Face frontal (amarela)
    glColor3f(1, 1, 0)
    glVertex3f(-0.5, 1.0, 0.5)  # Vértice superior esquerdo
    glVertex3f(0.5, 1.0, 0.5)  # Vértice superior direito
    glVertex3f(0.5, 0.0, 0.5)  # Vértice inferior direito
    glVertex3f(-0.5, 0.0, 0.5)  # Vértice inferior esquerdo

    # Face direita (laranja)
    glColor3f(1, 0.5, 0)
    glVertex3f(0.5, 1.0, 0.5)  # Vértice superior esquerdo
    glVertex3f(0.5, 1.0, -0.5)  # Vértice superior direito
    glVertex3f(0.5, 0.0, -0.5)  # Vértice inferior direito
    glVertex3f(0.5, 0.0, 0.5)  # Vértice inferior esquerdo

    # Face frontal (amarela)
    glColor3f(1, 1, 0)
    glVertex3f(-0.5, 1.0, 0.5)  # Vértice superior esquerdo
    glVertex3f(0.5, 1.0, 0.5)  # Vértice superior direito
    glVertex3f(0.5, 0.0, 0.5)  # Vértice inferior direito
    glVertex3f(-0.5, 0.0, 0.5)  # Vértice inferior esquerdo

    # Face direita (laranja)
    glColor3f(1, 0.5, 0)
    glVertex3f(0.5, 1.0, 0.5)  # Vértice superior esquerdo
    glVertex3f(0.5, 1.0, -0.5)  # Vértice superior direito
    glVertex3f(0.5, 0.0, -0.5)  # Vértice inferior direito
    glVertex3f(0.5, 0.0, 0.5)  # Vértice inferior esquerdo


def desenhar_circulo(radius, segments):
    glBegin(GL_TRIANGLE_FAN)
    # Centro do círculo
    glVertex2f(0, 0)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()


def desenhar_retangulo_janela(width, height, depth, color):
    glColor3f(*color)  # Define a cor
    glBegin(GL_QUADS)

    # Frente da janela
    glVertex3f(-width / 2, height / 2, depth)  # Superior esquerdo
    glVertex3f(width / 2, height / 2, depth)  # Superior direito
    glVertex3f(width / 2, -height / 2, depth)  # Inferior direito
    glVertex3f(-width / 2, -height / 2, depth)  # Inferior esquerdo

    # Traseira da janela
    glVertex3f(-width / 2, height / 2, 0)  # Superior esquerdo
    glVertex3f(width / 2, height / 2, 0)  # Superior direito
    glVertex3f(width / 2, -height / 2, 0)  # Inferior direito
    glVertex3f(-width / 2, -height / 2, 0)  # Inferior esquerdo

    # Lados da janela
    glVertex3f(-width / 2, height / 2, depth)  # Superior esquerdo
    glVertex3f(-width / 2, height / 2, 0)  # Superior esquerdo traseiro
    glVertex3f(-width / 2, -height / 2, 0)  # Inferior esquerdo traseiro
    glVertex3f(-width / 2, -height / 2, depth)  # Inferior esquerdo

    glVertex3f(width / 2, height / 2, depth)  # Superior direito
    glVertex3f(width / 2, height / 2, 0)  # Superior direito traseiro
    glVertex3f(width / 2, -height / 2, 0)  # Inferior direito traseiro
    glVertex3f(width / 2, -height / 2, depth)  # Inferior direito

    glEnd()



def desenhar_nave():
    # Corpo Principal da Nave
    glPushMatrix()
    glTranslatef(0, 0, 0)  # Posição
    desenhar_cuboide(2, 2, 5, (1, 1, 1))
    desenhar_detalhes_do_corpo()  # Adicionar os detalhes ao corpo principal
    glPopMatrix()

    # Declinação frontal, cabine
    glPushMatrix()
    glTranslatef(0, 0.3, 3.2)  # Posição
    glRotatef(15, 1, 0, 0)  # Inclinação
    desenhar_cuboide(1.7, 0.7, 3.4, (1, 1, 1))
    glPopMatrix()

    # Declinação frontal, cabine inferior
    glPushMatrix()
    glTranslatef(0, -0.4, 3.2)  # Posição
    glRotatef(-15, 1, 0, 0)  # Inclinação
    desenhar_cuboide(1.7, 0.7, 3.4, (1, 1, 1))
    glPopMatrix()

    # Adiciona detalhes à cabine
    desenhar_detalhes_da_cabine()

    # Corte da nave

    glPushMatrix()
    glTranslatef(0, 0.9, 2.7)  # Posição
    glRotatef(180, 1, 1, 0)
    desenhar_retangulo_janela(0.1, 1.7, 0.1, (0, 0, 0))
    glPopMatrix()

    # Suporte das janelas
    glPushMatrix()
    glTranslatef(0, 0.55, 4)  # Posição
    glRotatef(15, 1, 0, 0)
    desenhar_cuboide(1.5, 0.15, 1.8, (0.96, 0.87, 0.70))
    glPopMatrix()

    # Janelas

    glPushMatrix()
    glTranslatef(0.4, 0.65, 4)  # Posição
    glRotatef(105, 1, 0, 0)
    desenhar_retangulo_janela(0.5, 1, 0.1, (0, 0, 0.2))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.4, 0.65, 4)  # Posição
    glRotatef(105, 1, 0, 0)
    desenhar_retangulo_janela(0.5, 1, 0.1, (0, 0, 0.2))
    glPopMatrix()

    # Circulo de cima

    glPushMatrix()
    glTranslatef(0, 1.1, 0.8)  # Posição
    glColor3f(0, 0, 0.1)
    glRotatef(90, 1, 0, 0)
    desenhar_circulo(0.5, 32)  # Raio
    glPopMatrix()


    glPushMatrix()
    glTranslatef(0, 1.15, 0.8)  # Posição
    glColor3f(0, 0, 0.4)
    glRotatef(90, 1, 0, 0)
    desenhar_circulo(0.2, 32)  # Raio
    glPopMatrix()


    # Suporte das janelas
    glPushMatrix()
    glTranslatef(0, 1, 0.8)  # Posição
    glRotatef(180, 1, 0, 0)
    desenhar_cuboide(2, 0.15, 3, (0.96, 0.87, 0.70))
    glPopMatrix()


    # TURBINAS EM FORMATO DE PIRÂMIDE.

    glPushMatrix()
    glTranslatef(-1.5, -0.3, 1)
    glScalef(-1, -1.3, 1.5)
    glRotatef(180, 0, -6, 6)
    desenhar_meia_base_piramide()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.5, -0.3, 1)
    glScalef(1, -1.3, 1.5)
    glRotatef(180, 0, -6, 6)
    desenhar_meia_base_piramide()
    glPopMatrix()

    # suporte das Nacelas

    glPushMatrix()
    glTranslatef(-2.5, -0.9, 0)  # Posição
    desenhar_cuboide(0.5, 0.5, 5, (1, 1, 1))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2.5, -0.9, 0)  # Posição
    desenhar_cuboide(0.5, 0.5, 5, (1, 1, 1))
    glPopMatrix()

    # Nacela esquerda sólida
    desenhar_cilindro_solido(-2.5, -0.9, 2.5, 0.3, 0.3, 0.5, (0.2, 0.0, 0.0))

    # Nacela direita sólida
    desenhar_cilindro_solido(2.5, -0.9, 2.5, 0.3, 0.3, 0.5, (0.2, 0.0, 0.0))

    # Detalhes aos motores
    desenhar_detalhes_dos_motores()

    # Asa esquerda inclinada
    glPushMatrix()
    glTranslatef(-1.3, -0.4, 0)  # Posição
    glRotatef(15, 0, 0, 1)
    desenhar_asa_curva(1, 1.5, 2)  # Curvatura
    glPopMatrix()

    # Asa direita inclinada
    glPushMatrix()
    glTranslatef(1.3, -0.4, 0)  # Posição
    glRotatef(-15, 0, 0, 1)
    desenhar_asa_curva(1, -1.5, 2)  # Curvatura
    glPopMatrix()

    # Adiciona detalhes às asas
    desenhar_detalhes_das_asas()

    # Base do módulo superior
    glPushMatrix()
    glTranslatef(0, 1.2, -1.8)  # Posição
    desenhar_cuboide(1.5, 0.3, 1.5, (0.3, 0.2, 0.0))
    glPopMatrix()

    # ventilação do módulo superior
    glPushMatrix()
    glTranslatef(0, 1.2, -1)  # Posição
    desenhar_cuboide(1, 0.3, 0.1, (0, 0, 0.0))
    glPopMatrix()

    # Conectores do módulo superior

    glPushMatrix()
    glTranslatef(1, 1.1, -1.5)  # Posição
    glRotatef(25, 0, 0, -5)
    desenhar_cuboide(0.65, 0.2, 0.1, (0.9, 0.9, 0.9))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1, 1.1, -1.5)  # Posição do módulo superior no topo da nave
    glRotatef(25, 0, 0, 5)
    desenhar_cuboide(0.65, 0.2, 0.1, (0.9, 0.9, 0.9))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.2, 0.8, -1.5)  # Posição
    glRotatef(120, 0, 0, -5)
    desenhar_cuboide(0.5, 0.2, 0.1, (0.9, 0.9, 0.9))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.2, 0.8, -1.5)  # Posição
    glRotatef(120, 0, 0, 5)
    desenhar_cuboide(0.5, 0.2, 0.1, (0.9, 0.9, 0.9))
    glPopMatrix()

    # Detalhes Traseiros plataforma reta
    glPushMatrix()
    glTranslatef(0, 0.1, -2.5)  # Posição
    desenhar_cuboide(2.3, 0.1, 1.5, (0.1, 0.1, 0.1))
    glPopMatrix()

    # Parte 7: Declinação Traseira
    glPushMatrix()
    glTranslatef(0, -0.2, -3)  # Posição
    glRotatef(40, 1, 0, 0)
    desenhar_cuboide(2.3, 0.1, 1.5, (1, 1, 1))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0.1, -3)  # Posição
    glRotatef(0, 0, 0, 1)
    desenhar_asa_curva(1, -0.5, 1)  # Curvatura
    glPopMatrix()

    # Parte 8: Luzes Frontais
    # Canhão frontal direita
    glPushMatrix()
    glTranslatef(0.9, 0.15, 2.7)  # Posição
    glRotatef(0, 0, 0, 1)
    desenhar_cuboide(0.2, 0.2, 4.1, (0, 0, 0))
    glPopMatrix()

    # Canhão frontal esquerda
    glPushMatrix()
    glTranslatef(-0.9, 0.15, 2.7)  # Posição
    glRotatef(0, 0, 0, 1)
    desenhar_cuboide(0.2, 0.2, 4.1, (0, 0, 0))
    glPopMatrix()




# Função principal
def main():
    global rotacao_x, rotacao_y
    inicializar()
    running = True
    # Loop principal
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_LEFT:
                    rotacao_y -= 5
                elif event.key == K_RIGHT:
                    rotacao_y += 5
                elif event.key == K_UP:
                    rotacao_x -= 5
                elif event.key == K_DOWN:
                    rotacao_x += 5

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        lidar_com_entrada()  # Teclado
        configurar_luz_dobra()

        desenhar_buraco_negro()

        # Renderização do ambiente
        desenhar_estrelas()
        desenhar_planetas()
        animar_ponto_dobra()

        # Renderização da nave
        glPushMatrix()
        glTranslatef(posicao_nave_x, posicao_nave_y, posicao_nave_z)
        glRotatef(180, 0, 1, 0)  # Rotaciona a nave 180 graus
        glRotatef(-15, 0, 1, 0)  # Inclina a nave
        glRotatef(rotacao_x, 1, 0, 0)  # Aplica rotação no eixo X
        glRotatef(rotacao_y, 0, 1, 0)  # Aplica rotação no eixo Y
        escalar_nave()
        desenhar_nave()
        glPopMatrix()

        animar_nave()

        pygame.display.flip()
        clock.tick(60)

        # Reinicia a simulação
        if velocidade_warp and posicao_nave_z < -100:
            time.sleep(2)
            reiniciar_simulacao()
main()