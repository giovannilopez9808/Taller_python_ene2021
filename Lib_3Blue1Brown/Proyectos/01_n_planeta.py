# Elaborado por Jesus Loera
# 17/01/21
# Para Protofísico

#------------------------
# conda activate manim 
# python -m manim  01_n_planeta.py
#------------------------

from manimlib.imports import *

class Text_1(Scene):
    def construct(self):
        text_1 = TextMobject('  Astrónomos del Observatorio Europeo Austral con el Very Large \
                                Telescope han observado un denso disco de polvo y gas orbitando a \
                                una joven estrella llamada AB Aurigae ').scale(0.8)
        self.play(Write(text_1), run_time = 5 )
        self.wait(4)
        self.play(FadeOutAndShiftDown(text_1))

class Aurigae(Scene):
    def construct(self):
        star_map  = ImageMobject ( 'star_map.png ').scale(4)
        text_2    = TextMobject  ( ' AB Aurigae es una estrella blanca de tipo espectral A0Ve con \
                                  una luminosidad 31 veces mayor que la luminosidad del Sol ' ).scale(0.7)
        text_2.bg    = BackgroundRectangle( text_2, fill_opacity = 1 ) 
        text_2_group = VGroup(text_2.bg, text_2).move_to(2*DOWN)
        self.wait()
        self.play(FadeIn(star_map))
        self.play(FadeIn(text_2_group))
        self.wait(4)
        self.play(FadeOutAndShift(text_2_group))
        self.play(FadeOut(star_map))
        self.wait()

class Disco(Scene):
    def construct(self):
        disco  = ImageMobject ('disco.png').scale(4)
        text_3 = TextMobject  ('Los astrónomos saben que los planetas se forma de discos de \
                                gas y polvo').scale(0.8)
        text_4 = TextMobject  ('Sin embargo, no se conoce bien la transición en la cual pasa de \
                                ser "un disco gas y polvo" a ser un planeta').scale(0.8)
        self.wait()
        self.play(FadeIn(disco))
        self.wait(3)
        self.play(FadeOut(disco))
        self.wait()
        self.play(Write(text_3))
        self.wait(2.8)
        self.play(FadeOutAndShiftDown(text_3))
        self.play(Write(text_4))
        self.wait(3)
        self.play(FadeOutAndShiftDown(text_4))
        self.wait()

class Evidencias(Scene):
    def construct(self):
        disco_2    = ImageMobject ('disco_2.png   ').scale(4)
        comparados = ImageMobject ('comparados.png').scale(4)
        comparados_señalados = ImageMobject ('comparados_señalados.png').scale(4)
        text_5 = TextMobject  ('¿Cuándo se puede decir que un planeta oficialmente \
                                ha nacido?'  ).scale(0.8).move_to(UP)
        text_6 = TextMobject  ('Hay dos indicios que podrian \
                                determinarlo').scale(0.8).move_to(DOWN)
        text_7 = TextMobject  ('1. Una especie de giro predecido por modelos \
                                astronómicos presente en la formación \
                                del planeta' ).scale(0.8).move_to(UP)
        text_8 = TextMobject  ('2. Presencia de espirales en \
                                el disco ').scale(0.8).move_to(DOWN)
        text_9 = TextMobject  ('Ambos ya han sido observados en el VLT').scale(0.8)
        self.wait()
        self.play(FadeIn(disco_2))
        self.wait(3)
        self.play(FadeOut(disco_2))
        self.wait()
        self.play(Write(text_5))
        self.play(Write(text_6))
        self.wait(2.3)
        self.play(FadeOut(text_5))
        self.play(FadeOut(text_6))
        self.wait()
        self.play(FadeIn(comparados))
        self.wait(3)
        self.play(FadeOut(comparados))
        self.wait()
        self.play(Write(text_7))
        self.play(Write(text_8))
        self.wait(5)
        self.play(FadeOut(text_7))
        self.play(FadeOut(text_8))
        self.wait()
        self.play(Write(text_9))
        self.wait(2.5)
        self.play(FadeOutAndShiftDown(text_9))
        self.wait()
        self.play(FadeIn(comparados_señalados))
        self.wait(3)
        self.play(FadeOut(comparados_señalados))
        self.wait()

class Futuro(Scene):
    def construct(self):
        text_10 = TextMobject  ('¿Qué sigue ahora?').scale(0.8).move_to(2*UP)
        text_11 = TextMobject  ('Seguir observando el cielo en busca de evidencias \
                                más solidas. Estás son imágenes captadas de un sistema \
                                muy joven en formación y se espera seguir observando más \
                                fenómenos similares' ).scale(0.8)
        self.wait()
        self.play(Write(text_10))
        self.play(Write(text_11))
        self.wait(7.5)
        self.play(FadeOut(text_10))
        self.play(FadeOut(text_11))
        self.wait()

class Protofisico(Scene):
    def construct(self):
        text_12 = TextMobject  ('Protofísico en Facebook').move_to(UP)
        text_13 = TextMobject  ('@Protofisico en twitter').move_to(DOWN)
        self.wait()
        self.play(Write(text_12))
        self.play(Write(text_13))
        self.wait(3)
        self.play(FadeOut(text_12))
        self.play(FadeOut(text_13))
        self.wait()