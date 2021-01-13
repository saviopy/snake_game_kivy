from kivy.app import App

from kivy.uix.widget import Widget

from kivy.clock import Clock

from kivy.core.window import Window

from kivy.properties import NumericProperty

from random import randint



class SnakePart(Widget):
    pass


class GameScreen(Widget):
    speed_x = 0
    speed_y = 0
    step = 40
    snake_parts = []
    score = NumericProperty(0)
    

    def new_game(self):
        self.score = 0

        for part in self.snake_parts:
            self.remove_widget(part)

        self.snake_parts = []
        self.speed_x = 0
        self.speed_y = 0

        head = SnakePart()
        head.pos = (0,0)
        self.add_widget(head)
        self.snake_parts.append(head)


    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0] # original position
        dy = touch.y - touch.opos[1]

        if abs(dx) > abs(dy):
            # mover na horizontal
            self.speed_y = 0
            if dx > 0:
                self.speed_x = self.step
            else:
                self.speed_x = -self.step
        else:
            self.speed_x = 0
            if dy > 0:
                self.speed_y = self.step
            else:
                self.speed_y = -self.step
    

    def hasCollided(self, wid1, wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        
        return True
            
    

    def next_frame(self, *args):
        
        head = self.snake_parts[0]

        food = self.ids.food

        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y

        # movimento corpo
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue

            part.new_x = self.snake_parts[i-1].x
            part.new_y = self.snake_parts[i-1].y
        
        for part in self.snake_parts[1:]:
            part.x = part.new_x
            part.y = part.new_y

        # movimento da cabeça
        head.x += self.speed_x
        head.y += self.speed_y

        # detectando colisão
        # colisão com a parede
        if not self.hasCollided(head,self):
            self.new_game()

        # colisão com a comida
        if self.hasCollided(head, food):
            self.score += 1
            food.x = randint(0,Window.width - 40)
            food.y = randint(0,Window.height - 40)


            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.add_widget(new_part)
            self.snake_parts.append(new_part)


        for part in self.snake_parts[1:]:
            if self.hasCollided(part, head):
                self.new_game()
            




class SnakeGame(App):
    def build(self):
        Window.size = (800,600)
        self.load_kv('main.kv')
    
    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame,1/5)







if __name__ == '__main__':
    SnakeGame().run()

