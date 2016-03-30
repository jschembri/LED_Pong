import pygame, sys
from pygame.locals import *

#Frames per second
FPS = 200

WINDOWWIDTH = 10
WINDOWHEIGHT = 10
SCALING = 40
LINETHICKNESS = 1
PADDLESIZE = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

def drawArena(theColor):
	DISPLAYSURF.fill(theColor)

#draws the ball
def drawBall(ball, ballDirX, ballDirY):
	displayedBall = ball.copy()
	displayedBall.centerx = round_to(ball.centerx , SCALING) 
	displayedBall.centery = round_to(ball.centery , SCALING) 
	pygame.draw.rect(DISPLAYSURF, GREEN , displayedBall)

def drawPaddle(paddle, color):
	if paddle.bottom > SCALING*(WINDOWHEIGHT ):
		paddle.bottom = SCALING*(WINDOWHEIGHT )
	elif paddle.top < 0:
		paddle.top = 0
	pygame.draw.rect(DISPLAYSURF, color, paddle)	

def moveBall(ball, ballDirX, ballDirY):
	ball.x += ballDirX
	ball.y += ballDirY
	return ball

def checkEdgeCollision(ball, ballDirX, ballDirY):
	if ball.left == 0 or ball.right == (WINDOWWIDTH*SCALING):
		ballDirX = ballDirX * -1
	if ball.top == 0 or ball.bottom == (WINDOWHEIGHT*SCALING):
		ballDirY = ballDirY * -1
	return ballDirX, ballDirY 

def artificalIntelligence(ball, ballDirX, paddle2):
	if ballDirX == -1:
		if paddle2.centery < SCALING*WINDOWHEIGHT/2:
			paddle2.y += 1 
		elif paddle2.centery > SCALING*WINDOWHEIGHT/2:
			paddle2.y -= 1 
	elif ballDirX == 1:
		if paddle2.centery < ball.centery:
			paddle2.y += 1 
		else:
			paddle2.y -= 1 
	return paddle2

def checkHitBall(ball, paddle1, paddle2, ballDirX):
	if ballDirX == -1 and paddle1.right == ball.left and paddle1.top  < ball.bottom and paddle1.bottom > ball.top:
		return -1
	elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.bottom and paddle2.bottom > ball.top:
		return -1
	else:
		return 1

def checkPointsScored(ball, scorePlayer1, scorePlayer2, ballDirX):
	if ball.left == 0:
		scorePlayer2 += 1
	elif ball.right  == WINDOWWIDTH*SCALING:
		scorePlayer1 += 1
	return scorePlayer1, scorePlayer2
	
def displayScore(scorePlayer1, scorePlayer2):
	resultSurf = BASICFONT.render('%s : %s'  % (scorePlayer1, scorePlayer2), True, WHITE)
	resultRect = resultSurf.get_rect()
	resultRect.topleft = (SCALING*(WINDOWWIDTH*9/20), 0)
	DISPLAYSURF.blit(resultSurf, resultRect)

#main function
def main():
	pygame.init()
	global DISPLAYSURF

	global BASICFONT, BASICFONTSIZE
	BASICFONTSIZE = 20 
	BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH*SCALING, WINDOWHEIGHT*SCALING))
	pygame.display.set_caption("LED Pong")

	ballX = SCALING/2*(WINDOWWIDTH - LINETHICKNESS)
	ballY = SCALING/2*(WINDOWHEIGHT - LINETHICKNESS)
	ball = pygame.Rect(ballX, ballY, LINETHICKNESS*SCALING, LINETHICKNESS*SCALING)

	playerOnePosition = SCALING/2*(WINDOWHEIGHT - PADDLESIZE)
	paddle1 = pygame.Rect(0, playerOnePosition, LINETHICKNESS*SCALING, PADDLESIZE*SCALING)

	playerTwoPosition = SCALING/2*(WINDOWHEIGHT - PADDLESIZE)
	paddle2 = pygame.Rect(SCALING*(WINDOWWIDTH - LINETHICKNESS), playerTwoPosition, LINETHICKNESS*SCALING, PADDLESIZE*SCALING)

	scorePlayer1 = 0
	scorePlayer2 = 0

	ballDirX = -1 
 	ballDirY = -1

	#Drawing stuff
	drawArena(BLACK)
	drawBall(ball, ballDirX, ballDirY)
	drawPaddle(paddle1, RED)
	drawPaddle(paddle2, BLUE)

	pygame.mouse.set_visible(0)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			#elif event.type == MOUSEMOTION:
			#	mousex, mousey = event.pos
			#	paddle1.y = mousey
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					paddle1.y -= 1*SCALING
				if event.key == K_DOWN:
					paddle1.y += 1*SCALING

		drawArena( (scorePlayer1*10, 0, scorePlayer2*10))
		drawPaddle(paddle1, RED)
		drawPaddle(paddle2, BLUE)
		drawBall(ball, ballDirX, ballDirY)

		ball = moveBall(ball, ballDirX, ballDirY)
		ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
		ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
		paddle2 = artificalIntelligence(ball, ballDirX, paddle2)

		scorePlayer1, scorePlayer2 = checkPointsScored(ball, scorePlayer1, scorePlayer2, ballDirX)

		displayScore(scorePlayer1, scorePlayer2)

		pygame.display.update()
		FPSCLOCK.tick(FPS)


if __name__=="__main__":
	main()