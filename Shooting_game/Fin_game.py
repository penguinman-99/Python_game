#TODO: 공 다 없애면 겜 끝 
#시간 초과시 게임 종료

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

#사라질 무기, 공 정보 저장 
weapon_to_remove=-1
ball_to_remove=-1


#Font 정의
game_font=pygame.font.Font(None,40)
total_time=100
start_ticks=pygame.time.get_ticks()#시작 시간을 정의 

#겜 종료 메시지 
game_result="Game over"


character_to_x_LEFT=0
character_to_x_RIGHT=0


running=True

while running:
    dt=clock.tick(30)
    #이벤트 처리
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                character_to_x_LEFT-=character_speed
            elif event.key==pygame.K_RIGHT:
                character_to_x_RIGHT=character_speed
            elif event.key==pygame.K_SPACE:
                weapon_x_pos=character_x_pos+character_width/2-weapon_width/2
                weapon_y_pos=character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                character_to_x_LEFT=0
            elif event.key==pygame.K_RIGHT:
                character_to_x_RIGHT=0
    character_x_pos+=character_to_x_LEFT+character_to_x_RIGHT



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
    #rect 정보 저장
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    for ball_idx,ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        #공의 rect 정보 업데이트 
        ball_rect=ball_images[ball_img_idx].get_rect()
        ball_rect.left=ball_pos_x
        ball_rect.top=ball_pos_y

        #공 캐릭터 충돌처리 
        if character_rect.colliderect(ball_rect):
            running=False
            break
        #공, 무기 충돌처리
        for weapon_idx,weapon_val in enumerate(weapons):
            weapon_pos_x=weapon_val[0]
            weapon_pos_y=weapon_val[1]
            #무기 rect 
            weapon_rect=weapon.get_rect()
            weapon_rect.left=weapon_pos_x
            weapon_rect.top=weapon_pos_y

            #충돌확인 
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove=weapon_idx
                ball_to_remove=ball_idx
                #가장 작은 공이 아니면 두개로 쪼갠다
                if ball_img_idx<3:
                    #현재 공 크기 정보를 갖고오기
                    ball_width=ball_rect.size[0]
                    ball_height=ball_rect.size[1]
                    #나눠진 공 정보
                    small_ball_rect=ball_images[ball_img_idx+1].get_rect()
                    small_ball_width=small_ball_rect.size[0]
                    small_ball_height=small_ball_rect.size[1]
                    balls.append({
                        "pos_x":ball_pos_x+ball_width/2-small_ball_width/2,#공의 xy좌표
                        "pos_y":ball_pos_y+ball_height/2-small_ball_height/2,
                        "img_idx":ball_img_idx+1, 
                        "to_x":-3,
                        "to_y":-6,
                        "init_spd_y":ball_speed_y[ball_img_idx+1] #y 최초속도


})
                    balls.append({
                        "pos_x":ball_pos_x+ball_width/2-small_ball_width/2,#공의 xy좌표
                        "pos_y":ball_pos_y+ball_height/2-small_ball_height/2,
                        "img_idx":ball_img_idx+1, 
                        "to_x":3,
                        "to_y":-6,
                        "init_spd_y":ball_speed_y[ball_img_idx+1] #y 최초속도


})
                break
        else:
            continue
        break   
    #충돌한 공, 무기 없애기
    if ball_to_remove>-1:
        del balls[ball_to_remove]
        ball_to_remove=-1
    if weapon_to_remove>-1:
        del weapons[weapon_to_remove]
        weapon_to_remove=-1
    #모든 공을 없앤 경우 종료

    if len(balls)==0:
        game_result="Mission Complete"
        running=False



    

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
    #경과 시간 계산 

    elapsed_time=(pygame.time.get_ticks()-start_ticks)/1000
    timer=game_font.render("Time: {}".format(int(total_time-elapsed_time)),True, (255,255,255))
    screen.blit(timer,(10,10))
    #시간 초과시 
    if total_time-elapsed_time<=0:
        game_result="Time over"
        running=False

    pygame.display.update()

msg=game_font.render(game_result,True,(255,255,0))
msg_rect=msg.get_rect(center=(int(screen_width/2,screen_height/2)))
screen.blit(msg,msg_rect)
pygame.display.update()
pygame.time.delay(2000)
  
pygame.quit()

