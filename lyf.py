import numpy as np
import time
import pygame
import sys
bg=(0,0,0)
gridc=(40,40,40)
aliven=(196, 16, 43 )
text_col=(255,255,255)
W,H=800,800
def update(cells):
    update_cells=np.zeros(cells.shape)
    for row,col in np.ndindex(cells.shape):
        alive=np.sum(cells[row-1:row+2,col-1:col+2])-cells[row,col]
        if cells[row,col]==1:
            update_cells[row,col]=1 if 2<=alive<=3 else 0
        else:
            update_cells[row,col]=1 if alive==3 else 0
    return update_cells
def render(screen,cells,size,gen,font):
    screen.fill(gridc)
    for row,col in np.ndindex(cells.shape):
        color=aliven if cells[row,col]==1 else bg
        pygame.draw.rect(screen,color,pygame.Rect(col*size,row*size,size-1,size-1))
    label=font.render(f"generation {gen}",True,text_col)
    screen.blit(label,(8,8))
    pygame.display.update()
def main():
    pygame.init()
    screen=pygame.display.set_mode((W,H))
    pygame.display.set_caption("LYF")
    font=pygame.font.SysFont("Arial",13,bold=True)
    size=10
    grid_n=W//size
    cells=np.zeros((grid_n,grid_n))
    history=[cells.copy()]
    idx=0
    running=False
    render(screen,cells,size,0,font)
    while True:
        ctrl=pygame.key.get_mods()&pygame.KMOD_CTRL
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit();sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    running=not running
                elif event.key==pygame.K_r:
                    cells=np.zeros((grid_n,grid_n))
                    history=[cells.copy()]
                    idx=0
                    running=False
                    render(screen,cells,size,0,font)
                elif event.key in (pygame.K_EQUALS,pygame.K_PLUS) and ctrl:
                    size=min(size+1,40)
                    grid_n=W//size
                    cells=np.zeros((grid_n,grid_n))
                    history=[cells.copy()]
                    idx=0
                    running=False
                    render(screen,cells,size,0,font)
                elif event.key==pygame.K_MINUS and ctrl:
                    size=max(size-1,2)
                    grid_n=W//size
                    cells=np.zeros((grid_n,grid_n))
                    history=[cells.copy()]
                    idx=0
                    running=False
                    render(screen,cells,size,0,font)
                elif event.key==pygame.K_RIGHT:
                    running=False
                    if idx<len(history)-1:
                        idx+=1
                    else:
                        next_cells=update(cells)
                        history.append(next_cells.copy())
                        idx=len(history)-1
                    cells=history[idx].copy()
                    render(screen,cells,size,idx,font)
                elif event.key==pygame.K_LEFT:
                    running=False
                    if idx>0:
                        idx-=1
                    cells=history[idx].copy()
                    render(screen,cells,size,idx,font)
        if pygame.mouse.get_pressed()[0]:
            pos=pygame.mouse.get_pos()
            col,row=pos[0]//size,pos[1]//size
            if 0<=row<grid_n and 0<=col<grid_n:
                cells[row,col]=1
                history=history[:idx+1]
                history[idx]=cells.copy()
                render(screen,cells,size,idx,font)
        if pygame.mouse.get_pressed()[2]:
            pos=pygame.mouse.get_pos()
            col,row=pos[0]//size,pos[1]//size
            if 0<=row<grid_n and 0<=col<grid_n:
                cells[row,col]=0
                history=history[:idx+1]
                history[idx]=cells.copy()
                render(screen,cells,size,idx,font)
        if running:
            cells=update(cells)
            history=history[:idx+1]
            history.append(cells.copy())
            idx=len(history)-1
            render(screen,cells,size,idx,font)
            time.sleep(0.05)
if __name__=="__main__":
    main()
