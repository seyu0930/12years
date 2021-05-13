import tkinter as tk
from PIL import ImageTk
from PIL import Image
import chap7fight

#マップの作成
def draw_map():
#y方向のマップの大きさ
  for y in range(0, MAX_HEIGHT):
#x方向のマップの大きさ
    for x in range(0, MAX_WIDTH):
#map_dataのy番目のリストの中のx番目に書かれてある数字をpに代入
      p = map_data[y][x]
#pが5以上のものはp=5とする
      if p >= 5:
        p = 5
#指定した位置にimageのp番の画像を配置
#画像サイズが62×62外枠の白の余白が31px
      canvas.create_image(x*62+31, y*62+31, image=images[p])
#勇者の初期位置
  canvas.create_image(brave_x*62 + 31, brave_y*62+31, image=images[4], tag="brave")

def ending():
  canvas.delete("all")
  canvas.create_rectangle(0, 0, 620, 434, fill="black")
  canvas.create_text(300, 200, fill="white", font=("MS ゴシック", 15),
                    text="""ゴールおめでとう。
                    
だが、君の戦いはまだ始まったばかりだ。

                                             ……つづく？""")
  button_up["state"] = "disabled"
  button_down["state"] = "disabled"
  button_right["state"] = "disabled"
  button_left["state"] = "disabled"

def check_move(x, y):
  global brave_x, brave_y, flag_key
  if x>=0 and x<MAX_WIDTH and y>=0 and y<MAX_HEIGHT:
    p = map_data[y][x]
    if p == 1:
      return
    elif p == 3:
      flag_key = True
      map_data[y][x] = 0
      canvas.delete("all")
      draw_map()
    elif p == 2:
      if flag_key == True:
        ending()
        return
      else:
        return
    elif p >= 5:
      fightmanager.fight_start(map_data, x, y, "brave")
    brave_x = x
    brave_y = y
    draw_map()


def click_button_up():
  check_move(brave_x, brave_y-1)

def click_button_down():
  check_move(brave_x, brave_y+1)

def click_button_left():
  check_move(brave_x-1, brave_y)

def click_button_right():
  check_move(brave_x+1, brave_y)




root = tk.Tk()
root.title("ダンジョン＆パイソン")
root.minsize(840,454)
root.option_add("font", ["メイリオ", 14])

canvas = tk.Canvas(width=620, height=434)
canvas.place(x=10, y=10)
canvas.create_rectangle(0, 0, 620, 434, fill="gray")

button_up = tk.Button(text="↑")
button_up.place(x=720, y=150)
button_up["command"] = click_button_up

button_down = tk.Button(text="↓")
button_down.place(x=720, y=210)
button_down["command"] = click_button_down

button_left = tk.Button(text="←")
button_left.place(x=660, y=180)
button_left["command"] = click_button_left

button_right = tk.Button(text="→")
button_right.place(x=780, y=180)
button_right["command"] = click_button_right

images = [ImageTk.PhotoImage(file=""),
          ImageTk.PhotoImage(file=""),
          ImageTk.PhotoImage(file=""),
          ImageTk.PhotoImage(file=""),
          ImageTk.PhotoImage(file=""),
          ImageTk.PhotoImage(file="")]

MAX_WIDTH = 10
MAX_HEIGHT = 7
map_data = [[1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 2, 0, 6, 1, 3, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 5, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 6, 1],
            [1, 0, 6, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

brave_x = 1
brave_y = 0
flag_key = False
fightmanager = chap7fight.FightManager()
draw_map()
root.mainloop()