import pygame
pygame.init()#초기화(필수)
#화면의 크기
screen_height=640
screen_width=480
screen=pygame.display.set_mode((screen_width,screen_height))

#화면 제목
pygame.display.set_caption("Made by kkh")
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


#이벤트 루프
running=True#게임이 돌아가는 지의 여부
while running:
    for event_trigger in pygame.event.get():#어떤 이벤트가 진행?
        if event_trigger.type==pygame.QUIT:#창이 닫히는 조건
            running=False
        if event_trigger.type==pygame.KEYDOWN:#키가 눌렀는지의 유무
            if event_trigger.key==pygame.K_LEFT: #왼쪽으로 옮길때 
                to_x-=5 #
            elif event_trigger.key==pygame.K_UP: #위로 옮길때
                to_y-=5
            elif event_trigger.key==pygame.K_RIGHT: #오른쪽으로 옮길때
                to_x+=5
            elif event_trigger.key==pygame.K_DOWN: #아래로 옮길때
                to_y+=5
        if event_trigger.type==pygame.KEYUP: #키가 때졌는지의 유무 
            if event_trigger.key==pygame.K_LEFT or event_trigger.key==pygame.K_RIGHT:
                to_x=0
            elif event_trigger.key==pygame.K_UP or event_trigger.key==pygame.K_DOWN:
                to_y=0
    character_x_pos+=to_x
    character_y_pos+=to_y
    #가로 경계값 처리
    
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos=screen_width-character_width
    if character_y_pos<0:
        character_y_pos=0
    elif character_y_pos>screen_height-character_height:
        character_y_pos=screen_height-character_height

    screen.blit(background,(0,0))#배경 그리기와 위치 지정
    screen.blit(character,(character_x_pos,character_y_pos))
    pygame.display.update()#배경을 지속적으로 유지
#pygame 종료
pygame.quit()

