import tkinter as tk
import random
from PIL import ImageTk
import time

class FightManager():
    
  def __init__(self):
    self.dialog = tk.Frame(width=820, height=434)
    self.dialog.place(x=10, y=10)
    self.canvas = tk.Canvas(self.dialog, width=820, height=434)
    self.canvas.place(x=0, y=0)
    self.canvas.create_rectangle(0, 0, 620, 434, fill="black")

    self.fbutton = tk.Button(self.dialog, text="攻撃")
    self.fbutton.place(x=180, y=340)
    self.fbutton["command"] = self.click_fight
    self.rbutton = tk.Button(self.dialog, text="力をためる")
    self.rbutton.place(x=320, y=340)
    self.rbutton["command"] = self.click_reserve

    self.images = [
      ImageTk.PhotoImage(file=""),
      ImageTk.PhotoImage(file="")]

    
    self.label = tk.Label(self.dialog, text="ラベル", fg="white", bg="black", justify="left")
    self.label.place(x=400, y=10)


    self.dialog.place_forget()
  
  def fight_start(self, mapdata, x, y, brave):
    self.dialog.place(x=10, y=10)
    self.map_data = mapdata
    self.brave_x = x
    self.brave_y = y
    self.brave = brave

    p = self.map_data[y][x]
    self.canvas.delete("all")
    self.canvas.create_rectangle(0, 0, 620, 434, fill="black")
    self.canvas.create_image(280, 180, image=self.images[p-5])
    
    if p == 5:
      self.monster = Monster1()
    elif p == 6:
      self.monster = Monster2()
    self.label["text"] = self.monster.name + "が現れた"

  def click_fight(self):
    self.fbutton["state"] = "disabled"
    self.rbutton["state"] = "disabled"
    self.do_turn(Brave().get_atk())

  def click_reserve(self):
    self.fbutton["state"] = "disabled"
    self.rbutton["state"] = "disabled"
    Brave().reserve()
    self.do_turn(-1)

  def do_turn(self, brave_atk):
    monster_dfs = self.monster.get_dfs()
    if brave_atk < 0:
      labeltext = "勇者は力をためた"
    else:
      labeltext = "勇者は攻撃した"
      self.label["text"] = labeltext
      self.dialog.update()
      time.sleep(1)
      dmg = brave_atk - monster_dfs
      self.monster.culc_hp(brave_atk, monster_dfs)
      if dmg <= 0:
        labeltext = labeltext + "\n防がれた"
      else:
        labeltext = labeltext + "\n" + str(dmg) + "のダメージを与えた"

    self.label["text"] = labeltext
    self.dialog.update()
    time.sleep(1)
    labeltext = labeltext + "\nモンスターの残り体力は" + str(self.monster.hp)
    self.label["text"] =labeltext
    self.dialog.update()
    if self.monster.hp < 1:
      time.sleep(1)
      self.fbutton["state"] = "normal"
      self.rbutton["state"] = "normal"
      self.fight_win()
      return

    time.sleep(1)
    brave_dfs = Brave().get_dfs()
    #self.braveじゃない
    if random.random() < 0.2:
      labeltext = labeltext + "\n\nモンスターは力をためた"
      self.monster.reserve()
    else:
      labeltext = labeltext + "\n\nモンスターの攻撃"
      self.label["text"] = labeltext
      self.dialog.update()
      time.sleep(1)
      monster_atk = self.monster.get_atk()
      dmg = monster_atk - brave_dfs
      Brave().culc_hp(monster_atk, brave_dfs)
      #braveじゃない
      if dmg <= 0:
        labeltext = labeltext + "\n防いだ"
      else:
        labeltext = labeltext + "\n" + str(dmg) + "のダメージを与えた"
    self.label["text"] = labeltext
    self.dialog.update()
    time.sleep(1)
    labeltext = labeltext + "\n勇者の残り体力は" + str(Brave().hp)
    self.label["text"] = labeltext
    self.dialog.update()
    if Brave().hp < 1:
      time.sleep(1)
      self.fight_lose()
    else:
      self.fbutton["state"] = "normal"
      self.rbutton["state"] = "normal"

  def fight_win(self):
    self.map_data[self.brave_y][self.brave_x] = 0
    self.dialog.place_forget()

  def fight_lose(self):
    canvas = tk.Canvas(self.dialog, width=820, height=434)
    canvas.place(x=0, y=0)
    canvas.create_rectangle(0, 0, 620,434, fill="red")
    canvas.create_text(300, 200, fill="white", font=("MS ゴシック", 15),
                       text="""勇者は負けてしまった...

    最初からやり直してくれ。""")

class Character():
  def __new__(cls):
    obj = super().__new__(cls)
    obj.rsv = 1
    return obj

  def get_atk(self):
    return random.randint(1, self.atk)
    #rに倍率をコピーしている
    r = self.rsv
    #コピーしてあるので=1してもrには影響しない
    self.rsv = 1
    return random.randint(1, self.atk*r)

  def get_dfs(self):
    return random.randint(1, self.dfs)

  def culc_hp(self, atk, dfs):
    dmg = atk - dfs
    if dmg < 1:
      return self.hp
    self.hp = self.hp - dmg
    if self.hp < 1:
      self.hp = 0
    return self.hp

  def reserve(self):
    self.rsv = self.rsv + 1


class Brave(Character):
  def __init__(self):
    self.name = "勇者"
    self.hp = 30
    self.atk = 15
    self.dfs = 10

class Monster1(Character):
  def __init__(self):
    self.name = "モンスター１"
    self.hp = 20
    self.atk = 15
    self.dfs = 5

class Monster2(Character):
  def __init__(self):
    self.name = "モンスター２"
    self.hp = 10
    self.atk = 8
    self.dfs = 5





