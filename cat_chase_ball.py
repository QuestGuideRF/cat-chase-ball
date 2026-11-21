import warnings
warnings .filterwarnings ("ignore",category =UserWarning )
import pygame
import random
import math
from pygame .math import Vector2
WIDTH ,HEIGHT =800 ,600
FPS =60
BG_COLOR =(230 ,240 ,255 )
CAT_COLOR =(255 ,165 ,0 )
EYE_COLOR =(255 ,255 ,255 )
PUPIL_COLOR =(0 ,0 ,0 )
MOUSE_COLOR =(30 ,144 ,255 )
MAX_SPEED =200.0
ACCELERATION =600.0
FRICTION =0.90
CATCH_DISTANCE =30
pygame .init ()
screen =pygame .display .set_mode ((WIDTH ,HEIGHT ))
pygame .display .set_caption ("Кот гонится за мышью")
clock =pygame .time .Clock ()
font =pygame .font .SysFont (None ,24 )
cat_pos =Vector2 (WIDTH /2 ,HEIGHT /2 )
cat_vel =Vector2 (0 ,0 )
mouse_target =Vector2 (pygame .mouse .get_pos ())
caught_timer =0.0
def draw_cat (surface ,pos ,angle ,size =48 ):
    x ,y =int (pos .x ),int (pos .y )
    body_rect =pygame .Rect (0 ,0 ,int (size *1.2 ),size )
    body_rect .center =(x ,y )
    pygame .draw .ellipse (surface ,CAT_COLOR ,body_rect )
    head_offset =Vector2 (math .cos (angle ),math .sin (angle ))*(size *0.6 )
    head_pos =Vector2 (x ,y )+head_offset
    pygame .draw .circle (surface ,CAT_COLOR ,(int (head_pos .x ),int (head_pos .y )),int (size *0.45 ))
    ear1 =[
    (head_pos .x -size *0.25 ,head_pos .y -size *0.30 ),
    (head_pos .x -size *0.05 ,head_pos .y -size *0.60 ),
    (head_pos .x +size *0.10 ,head_pos .y -size *0.20 ),
    ]
    ear2 =[
    (head_pos .x +size *0.25 ,head_pos .y -size *0.30 ),
    (head_pos .x +size *0.05 ,head_pos .y -size *0.60 ),
    (head_pos .x -size *0.10 ,head_pos .y -size *0.20 ),
    ]
    pygame .draw .polygon (surface ,CAT_COLOR ,ear1 )
    pygame .draw .polygon (surface ,CAT_COLOR ,ear2 )
    eye_offset =Vector2 (math .cos (angle +0.15 ),math .sin (angle +0.15 ))*(size *0.15 )
    sep =size *0.10
    left_eye =head_pos +eye_offset .rotate (20 )+Vector2 (-sep ,0 )
    right_eye =head_pos +eye_offset .rotate (-20 )+Vector2 (sep ,0 )
    pygame .draw .circle (surface ,EYE_COLOR ,(int (left_eye .x ),int (left_eye .y )),int (size *0.08 ))
    pygame .draw .circle (surface ,EYE_COLOR ,(int (right_eye .x ),int (right_eye .y )),int (size *0.08 ))
    look =Vector2 (math .cos (angle ),math .sin (angle ))*(size *0.03 )
    pygame .draw .circle (surface ,PUPIL_COLOR ,(int (left_eye .x +look .x ),int (left_eye .y +look .y )),int (size *0.04 ))
    pygame .draw .circle (surface ,PUPIL_COLOR ,(int (right_eye .x +look .x ),int (right_eye .y +look .y )),int (size *0.04 ))
    tail_start =Vector2 (x ,y )+Vector2 (-size *0.5 ,size *0.05 )
    tail_end =tail_start +Vector2 (math .cos (angle -1.4 ),math .sin (angle -1.4 ))*(size *0.9 )
    pygame .draw .lines (surface ,CAT_COLOR ,False ,[(tail_start .x ,tail_start .y ),(tail_end .x ,tail_end .y )],max (2 ,int (size *0.09 )))
running =True
while running :
    dt =clock .tick (FPS )/1000.0
    for event in pygame .event .get ():
        if event .type ==pygame .QUIT :
            running =False
        elif event .type ==pygame .KEYDOWN :
            if event .key ==pygame .K_ESCAPE :
                running =False
        elif event .type ==pygame .MOUSEBUTTONDOWN :
            if event .button ==1 :
                mouse_target =Vector2 (random .uniform (50 ,WIDTH -50 ),random .uniform (50 ,HEIGHT -50 ))
    mx ,my =pygame .mouse .get_pos ()
    mx =max (0 ,min (WIDTH ,mx ))
    my =max (0 ,min (HEIGHT ,my ))
    mouse_target =Vector2 (mx ,my )
    dir_vec =(mouse_target -cat_pos )
    dist =dir_vec .length ()
    if dist >0.001 :
        desired =dir_vec .normalize ()*MAX_SPEED
    else :
        desired =Vector2 (0 ,0 )
    steer =(desired -cat_vel )
    if steer .length ()>0 :
        steer_limit =ACCELERATION *dt
        if steer .length ()>steer_limit :
            steer .scale_to_length (steer_limit )
        cat_vel +=steer
    cat_vel *=FRICTION
    if cat_vel .length ()>MAX_SPEED :
        cat_vel .scale_to_length (MAX_SPEED )
    cat_pos +=cat_vel *dt
    if (cat_pos -mouse_target ).length ()<=CATCH_DISTANCE :
        if caught_timer <=0.0 :
            caught_timer =0.9
        mouse_target +=Vector2 (random .choice ([-1 ,1 ]),random .choice ([-1 ,1 ]))*40
    screen .fill (BG_COLOR )
    MOUSE_RADIUS =12
    pygame .draw .circle (screen ,MOUSE_COLOR ,(int (mouse_target .x ),int (mouse_target .y )),MOUSE_RADIUS )
    angle =math .atan2 (mouse_target .y -cat_pos .y ,mouse_target .x -cat_pos .x )
    draw_cat (screen ,cat_pos ,angle ,size =64 )
    txt =font .render ("Переместите мышь внутри окна",True ,(20 ,20 ,20 ))
    screen .blit (txt ,(14 ,10 ))
    speed_txt =font .render (f"Cat speed: {int (cat_vel .length ())} px/s   Distance: {int ((cat_pos -mouse_target ).length ())} px",True ,(30 ,30 ,30 ))
    screen .blit (speed_txt ,(14 ,36 ))
    if caught_timer >0.0 :
        caught_surf =font .render ("Caught",True ,(200 ,30 ,30 ))
        screen .blit (caught_surf ,(WIDTH //2 -20 ,20 ))
        caught_timer -=dt
    pygame .display .flip ()
pygame .quit ()