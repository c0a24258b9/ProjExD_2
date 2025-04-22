import os
import time
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650  #画面サイズ
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横、縦）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True #横　縦判定
    #横方向判定
    if rct.left < 0 or WIDTH < rct.right:  #画面外だったら
        yoko = False
    #縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom:  #画面外だったら
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に、半透明の黒い画面上に「Game Over」と表
    示し，泣いているこうかとん画像を貼り付ける関数
    """
    ko_img = pg.image.load("fig/8.png") 
    font = pg.font.SysFont(None, 100)
    gameover_text = font.render("Game Over", True, (255,255,255))
    screen_width, screen_height = screen.get_size()
    blackout = pg.Surface((screen_width, screen_height))
    blackout.set_alpha(180)
    text_rect = gameover_text.get_rect(center=(screen_width // 2, screen_height // 2))
    ko_rect = ko_img.get_rect(center=(screen_width // 2 +220, screen_height // 2))
    ko_rect2 = ko_img.get_rect(center=(screen_width // 2 -220, screen_height // 2))
    blackout.fill((0, 0, 0))
    screen.blit(blackout, (0, 0))
    screen.blit(ko_img, ko_rect)
    screen.blit(ko_img, ko_rect2)
    screen.blit(gameover_text, text_rect)

    pg.display.update()
    time.sleep(5)
    return
    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))

    vx, vy = (+5, +5) 

    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): #重なったとき
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #左右方向
                sum_mv[1] += mv[1]  #上下方向

        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #画面の外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #画面の中に戻す

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  #横にはみ出ていたら
            vx *= -1
        if not tate:  #縦にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  #爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
