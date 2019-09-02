import random
GameBoard = [
"BRBRB    ",
"RRRRRR   ",
"BRBRBRB  ",
"RRRRRRRR ",
"BRBRBRBRB",
" RRRRRRRR",
"  BRBRBRB",
"   RRRRRR",
"    BRBRB",
]
##DestroyBridge = random.randint(1,36)
##rownum = 0
##colnum = 0
##score = 0
##print DestroyBridge
##for row in GameBoard:
##    for col in row:
##        if col == "R":
##            score += 1
##            if score == DestroyBridge:
##                GameBoard[rownum] = (GameBoard[rownum])[:colnum]+" "+(GameBoard[rownum])[-(len(row)-colnum-1):]
##        colnum += 1
##    colnum = 0
##    rownum += 1
##print GameBoard
##print (GameBoard[0])[:3]
##print (GameBoard[0])[-(9-3-1):]
#print (GameBoard[0])[:3]
print (GameBoard[2])[:2]+"T"+(GameBoard[2])[3:]
