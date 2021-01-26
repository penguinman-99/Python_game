import pygame
#####################################
#기본 초기화
pygame.init()#초기화(필수)

#화면의 크기
screen_height=640
screen_width=480
screen=pygame.display.set_mode((screen_width,screen_height))

#화면 제목 설정
pygame.display.set_caption("Made by kkh")
#FPS
clock=pygame.time.Clock()
######################################
#1. 사용자 게임 초기화(배경 화면, 좌표, 폰트, 게임이미지 등.)

#배경 이미지 불러오기
background=pygame.image.load("C:/Users/Administrator/Desktop/PythonWorkSpace/pygame_basic/background.png")
#스프라이트 불러오기(캐릭터)
character=pygame.image.load("C:/Users/Administrator/Desktop/PythonWorkSpace/pygame_basic/main_character.png")
character_size=character.get_rect().size#캐릭터 이미지 크기 구해오기
character_width=character_size[0] #캐릭터의 가로
character_height=character_size[1] #캐릭터의 세로
character_x_pos=screen_width/2-character_width/2#화면 가로 정중앙
character_y_pos=screen_height-character_height #화면 세로크기 아래

#이동할 좌표
to_x=0
to_y=0

#이동속도
character_speed=0.6

#적 캐릭터
enemy=pygame.image.load("C:/Users/Administrator/Desktop/PythonWorkSpace/pygame_basic/enemy.png")
enemy_size=enemy.get_rect().size#캐릭터 이미지 크기 구해오기
enemy_width=enemy_size[0] #캐릭터의 가로
enemy_height=enemy_size[1] #캐릭터의 세로
enemy_x_pos=screen_width/2-enemy_width/2#화면 가로 정중앙
enemy_y_pos=(screen_height/2)-(enemy_height/2) #화면 세로크기 아래
#폰트 정의
game_font=pygame.font.Font(None,40) #폰트 객체 생성

#총 시간
total_time=10
#시간 계산
start_ticks=pygame.time.get_ticks() #시작 tick 정보 받아오기
##################################

#이벤트 루프
running=True#게임이 돌아가는 지의 여부
while running:
    dt=clock.tick(60) #게임화면의 초당 프레임 설정
    # 2. 이벤트 처리(키보드, 마우스 등)
    for event_trigger in pygame.event.get():#어떤 이벤트가 진행?
        if event_trigger.type==pygame.QUIT:#창이 닫히는 조건
            running=False
        if event_trigger.type==pygame.KEYDOWN:#키가 눌렀는지의 유무
            if event_trigger.key==pygame.K_LEFT: #왼쪽으로 옮길때 
                to_x-=character_speed #
            elif event_trigger.key==pygame.K_UP: #위로 옮길때
                to_y-=character_speed
            elif event_trigger.key==pygame.K_RIGHT: #오른쪽으로 옮길때
                to_x+=character_speed
            elif event_trigger.key==pygame.K_DOWN: #아래로 옮길때
                to_y+=character_speed
        if event_trigger.type==pygame.KEYUP: #키가 때졌는지의 유무 
            if event_trigger.key==pygame.K_LEFT or event_trigger.key==pygame.K_RIGHT:
                to_x=0
            elif event_trigger.key==pygame.K_UP or event_trigger.key==pygame.K_DOWN:
                to_y=0
    #3. 게임 캐릭터 위치 정의
    character_x_pos+=to_x*dt
    character_y_pos+=to_y*dt
    #가로 경계값 처리
    
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos=screen_width-character_width
    if character_y_pos<0:
        character_y_pos=0
    elif character_y_pos>screen_height-character_height:
        character_y_pos=screen_height-character_height

    #4. 충돌 처리를 위한 정보 업데이트
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    enemy_rect=enemy.get_rect()
    enemy_rect.left=enemy_x_pos
    enemy_rect.top=enemy_y_pos

    #충돌의 유무 
    if character_rect.colliderect(enemy_rect):
        print("충돌이벤트 발생.")
        running=False #게임 이벤트 종료
    #5. 화면에 그리기 
    screen.blit(background,(0,0))#배경 그리기와 위치 지정
    screen.blit(character,(character_x_pos,character_y_pos))
    
    screen.blit(enemy,(enemy_x_pos,enemy_y_pos)) #적포지션
    #타이머 삽입 
    #경과 시간
    elapsed_time=(pygame.time.get_ticks()-start_ticks)/1000
    #1000으로 나누어 초단위로 표시.
    
    timer=game_font.render(str(int(total_time-elapsed_time)),True,(255,255,0)) #문자처리 
    #출력할 글자, True, 글자 색상
    screen.blit(timer,(0,0))
    if total_time-elapsed_time<=0:
        print("타임아웃")
        running=False
    
    pygame.display.update()#배경을 지속적으로 유지

pygame.time.delay(2000) #2초 대기

#pygame 종료
pygame.quit()

