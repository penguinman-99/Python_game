import os
import pygame
#기본 초기화
pygame.init()

#화면 크기
screen_width=640
screen_height=480
screen=pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("공산당 척결")

#FPS 설정
clock=pygame.time.Clock()

#현재 파일의 위치를 반환
current_path=os.path.dirname(__file__)
image_path=os.path.join(current_path,"img")
#배경만들기 
background=pygame.image.load(os.path.join(image_path,"background.png"))
#스테이지
stage=pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size=stage.get_rect().size

stage_height=stage_size[1] 
#캐릭
character=pygame.image.load(os.path.join(image_path,"character.png"))
character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]

character_x_pos=(screen_width/2)-(character_width/2)
character_y_pos=screen_height-character_height-stage_height

running=True

while running:
    dt=clock.tick(30)
    #이벤트 처리
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    #게임 캐릭터의 위치 정의

    #충돌 처리

    #화면 나타내기

    screen.blit(background,(0,0))
    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))
    pygame.display.update()

pygame.quit()

