from cell import Cell
from PIL import Image, ImageDraw

class Board:

    def __init__(self, filename):
        self.board = self.read_file(filename)
        self.set_adjacents()
        self.goal_coords
        self.start_cell

    def read_file(self, filename):
        path = "boards/" + filename
        f = open(path, "r")
        result = []
        for l in f:
            l = l.replace("\n", "")
            linelist = []          
            for c in l:
                cell = Cell(c, len(linelist), len(result))
                linelist.append(cell)
                if c == "B":
                    self.goal_coords = (linelist.index(cell), len(result))
                elif c == "A":
                    self.start_cell = cell
            result.append(linelist)
        return result
    
    def set_adjacents(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                cell = self.board[i][j]
                adj = []
                adj.append(self.try_coords(i-1,j))
                adj.append(self.try_coords(i,j-1))
                adj.append(self.try_coords(i+1,j))
                adj.append(self.try_coords(i,j+1))
                for k in range(4):
                    if not adj[k] == 0:
                        cell.add_adjacent(adj[k])

    def try_coords(self,i,j):
        if i < 0 or j < 0 or i > len(self.board)-1 or j > len(self.board[0])-1:
            return 0
        return self.board[i][j]
   
    def __str__(self):
        res = ""
        for line in self.board:
            for c in line:
                res += str(c)
            res += "\n"
        return res

    def boardToImage(self):
        xc = len(self.board[0])
        yc = len(self.board)
        img = Image.new("RGB",(xc,yc),(255,255,255))
        for x in range(xc):
            for y in range(yc):
                cell = self.board[y][x]
                img.putpixel((x,y),cell.get_color(cell.c))
        img.show()

    def board_image(self, path):
        xp = len(self.board[0])
        yp = len(self.board)
        width = 100 * xp
        height = 100 * yp
        img = Image.new("RGB", size=(width, height), color=255)
        draw = ImageDraw.Draw(img)
        xstep = width/xp
        ystep = height/yp
        x = 0
        y = 0
        for row in self.board:
            for cell in row:
                if type(cell) is str:
                    color = "yellow"
                else:
                    color = cell.color
                if cell in path:
                    color = "yellow"
                draw.rectangle((x*xstep, y*ystep, xstep*(x+1), ystep*(y+1)), color)
                x = (x+1)%len(self.board[0])
                if x == 0:
                    y += 1
        del draw
        img.show()
        
    
    def path_repr(self, closed):
        b = self.board
        for c in closed:
            coo = c.coords
            b[coo[1]][coo[0]] = "*"
        s = ""
        for line in b:
            for c in line:
                s += str(c)
            s+="\n"
        return s
                
        