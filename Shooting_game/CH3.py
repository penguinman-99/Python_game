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
#캐릭터
character=pygame.image.load(os.path.join(image_path,"character.png"))
character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]
character_x_pos=(screen_width/2)-(character_width/2)
character_y_pos=screen_height-character_height-stage_height
#캐릭터 이동방향
character_to_x=0
#캐릭터 이동속도
character_speed=5

# 무기 제작 
weapon=pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size=weapon.get_rect().size
weapon_width=weapon_size[0]

weapons=[]

#무기 속도

weapon_speed=10

#공만들기
ball_images=[
    pygame.image.load(os.path.join(image_path,"balloon1.png")),
    pygame.image.load(os.path.join(image_path,"balloon2.png")),
    pygame.image.load(os.path.join(image_path,"balloon3.png")),
    pygame.image.load(os.path.join(image_path,"balloon4.png")),

]

#공 크기별 스피드
ball_speed_y=[
    -18,-15,-12,-9
]

balls=[]
balls.append({
    "pos_x":50,#공의 xy좌표
    "pos_y":50,
    "img_idx":0, 
    "to_x":3,
    "to_y":-6,
    "init_spd_y":ball_speed_y[0] #y 최초속도


})


running=True

while running:
    dt=clock.tick(30)
    #이벤트 처리
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                character_to_x-=character_speed
            elif event.key==pygame.K_RIGHT:
                character_to_x+=character_speed
            elif event.key==pygame.K_SPACE:
                weapon_x_pos=character_x_pos+character_width/2-weapon_width/2
                weapon_y_pos=character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                character_to_x=0



    #게임 캐릭터의 위치 정의
    character_x_pos+=character_to_x
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos=screen_width-character_width

    #무기의 위치 조정
    #y의 위치만 지속적으로 변경 
    weapons=[[w[0],w[1]-weapon_speed] for w in weapons]

    #천장에 닿을시 소멸
    weapons=[[w[0],w[1]] for w in weapons if w[1]>0]

    for ball_idx,ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        ball_size=ball_images[ball_img_idx].get_rect().size
        ball_width=ball_size[0]
        ball_height=ball_size[1]
        if ball_pos_x<0 or ball_pos_x>screen_width-ball_width:
            ball_val["to_x"]=ball_val["to_x"]*-1
            #튕겨올라가는 처리 
        if ball_pos_y>=screen_height-stage_height-ball_height:
            ball_val["to_y"]=ball_val["init_spd_y"]
        else: #속도 증가(올라갔다 내려갔다)
            ball_val["to_y"]+=0.5
        ball_val["pos_x"]+=ball_val["to_x"]
        
        ball_val["pos_y"]+=ball_val["to_y"]
    #충돌 처리

    #화면 나타내기

    screen.blit(background,(0,0))
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
    for idx,val in enumerate(balls):
        ball_pos_x=val["pos_x"]
        ball_pos_y=val["pos_y"]
        ball_img_idx=val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_pos_x,ball_pos_y))
    screen.blit(character,(character_x_pos,character_y_pos))
    screen.blit(stage,(0,screen_height-stage_height))
    
    pygame.display.update()

pygame.quit()

