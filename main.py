import pygame
import pygame_menu
import random
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_word(surface, font, word_display):
    text = font.render('Mot à deviner ', True, (255, 255, 255))
    text_deux = font.render(' ' + ' '.join(word_display), True, (255, 255, 255))
    surface.blit(text, (width // 2.6, 100))
    surface.blit(text_deux, (width // 3, 200))

def start_game(surface, font):
    with open('mots.txt', 'r') as file:
        words = file.read().splitlines()
    chosen_word = random.choice(words)
    print('Jouer au pendu avec le mot :', chosen_word)
    word_display = ['_ '] * len(chosen_word)
    print('Mot à deviner :', ' '.join(word_display))
    clock = pygame.time.Clock()
    game_over = False
    victory_message_displayed = False
    hangman_parts_color = BLACK
    head_position = (223, 115)
    head_radius = 20
    errors = 0

    while not game_over:
        surface.fill((73, 184, 174))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key)
                    if letter.lower() in chosen_word.lower():
                        for i in range(len(chosen_word)):
                            if chosen_word[i].lower() == letter.lower():
                                word_display[i] = chosen_word[i].upper() if letter.isupper() else chosen_word[i]
                        draw_word(surface, font, word_display)
                        pygame.display.flip()

                        if all(char.isalpha() or char.isspace() for char in word_display) and not victory_message_displayed:
                            print('Félicitations, vous avez deviné le mot :', chosen_word)
                            victory_message_displayed = True
                            show_victory_menu(surface)
                    else: 
                        errors += 1            

        draw_word(surface, font, word_display)

        # Dessinez les parties du pendu en fonction des erreurs
        if errors >= 1:
            pygame.draw.rect(surface, hangman_parts_color, (50, 350, 150, 10))  # Base
            pygame.draw.rect(surface, hangman_parts_color, (120, 50, 10, 300))  # Poteau
            pygame.draw.rect(surface, hangman_parts_color, (120, 50, 100, 10))  # Haut de la potence
            pygame.draw.rect(surface, hangman_parts_color, (220, 50, 5, 50))    # Corde
        if errors >= 2:
            pygame.draw.circle(surface, hangman_parts_color, head_position, head_radius) # Tête
        if errors >= 3:
            pygame.draw.rect(surface, hangman_parts_color, (212, 135, 20, 80)) # Corps
        if errors >= 4:
            rotate_arm(surface, (175, 135, 10, 40), 45, (175, 135), (10, 40))  # Bras gauche
        if errors >= 5:
            rotate_arm(surface, (250, 160, 10, 40), -45, (233, 135), (10, 40))  # Bras droit
        if errors >= 6:
            rotate_leg(surface, (190, 220, 10, 40), 45, (225, 210), (10, 40))  # Jambe gauche
        if errors >= 7:
            rotate_leg(surface, (210, 200, 10, 40), -45, (180, 210), (10, 40))  # Jambe droite

        pygame.display.flip()
        clock.tick(30)

        if errors >= 7:
            print('Désolé, vous avez perdu. Le mot était :', chosen_word)
            game_over = True
            start_ticks = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_ticks < 1000:  # Pause de 1 seconde
                pygame.time.delay(100)
            show_loose_menu(surface, chosen_word)

def rotate_arm(surface, color, angle, position, size):
    rotated_arm = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(rotated_arm, BLACK, (0, 0, *size))
    rotated_arm = pygame.transform.rotate(rotated_arm, angle)
    surface.blit(rotated_arm, position)

def rotate_leg(surface, color, angle, position, size):
    rotated_leg = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(rotated_leg, BLACK, (0, 0, *size))
    rotated_leg = pygame.transform.rotate(rotated_leg, angle)
    surface.blit(rotated_leg, position)

def play_game():
    start_game(surface, font)

def show_victory_menu(surface):
    felicitation = pygame_menu.Menu('Bravo', 800, 600, theme=pygame_menu.themes.THEME_DARK)
    felicitation.add.button('Félicitations, vous avez gagné !', pygame_menu.events.NONE)
    felicitation.add.button('Retourner au menu', main_menu)
    felicitation.mainloop(surface)

def show_loose_menu(surface, chosen_word):
    loose = pygame_menu.Menu('Désolé', 800, 600, theme=pygame_menu.themes.THEME_DARK)
    loose.add.button(f'Désolé, vous avez perdu. Le mot était : {chosen_word}', pygame_menu.events.NONE)
    loose.add.button('Retourner au menu', main_menu)
    loose.mainloop(surface)

def add_word_menu():
    add_word_menu = pygame_menu.Menu('Ajouter un Mot', 800, 600, theme=pygame_menu.themes.THEME_DARK)
    add_word_menu.add.text_input('Mot : ', onchange=onchange_add_word)
    add_word_menu.add.button('Ajouter', add_word)
    add_word_menu.add.button('Retourner au menu', main_menu)
    add_word_menu.mainloop(surface)

def onchange_add_word(text) -> None:
    global new_word
    new_word = text

def add_word() -> None:
    with open('mots.txt', 'a') as file:
        file.write(new_word + '\n')
    main_menu()


def main_menu():
    menu = pygame_menu.Menu('Menu', 800, 600, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Jouer au pendu', play_game)
    menu.add.button('Ajouter un mot', add_word_menu)
    menu.add.button('Quitter', pygame_menu.events.EXIT)
    menu.mainloop(surface)

width, height = 800, 600
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Jeu du Pendu')

font = pygame.font.Font(None, 36)

main_menu()

pygame.quit()
sys.exit()
