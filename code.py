import pykit_explorer
from lcd_display import LCDDisplay
from imu_sensor import IMUSensor
from digital_io import DigitalInput




imu = IMUSensor()
lcd = LCDDisplay()
btn = DigitalInput(board.D3)
lcd.backlight_on()
group, palette = lcd.make_group(0x000000)




# variables
start = False
radius = 7



levels = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
level = 0
level_change = False
level_selected = False
level_running = True

#level 1
level1_objects = []
key = lcd.draw_rect(195, 5, 40, 40, fill=0x00FF00, outline=0x00FF00, stroke=2)
goal = lcd.draw_rect(5, 85, 45, 45, fill=None, outline=0xFFAAAA)
level1_enemies = []
enemyFish1 = lcd.draw_circle(100, 25, 10, fill=0x00FFFF, outline=0xFF0000)
enemyFish2 = lcd.draw_circle(100, 55, 10, fill=0x00FFFF, outline=0xFF0000)
enemyFish3 = lcd.draw_circle(150, 85, 10, fill=0x00FFFF, outline=0xFF0000)
enemyFish4 = lcd.draw_circle(150, 115, 10, fill=0x00FFFF, outline=0xFF0000)
enemyFish1_velocity = 5
enemyFish2_velocity = 5
enemyFish3_velocity = -5
enemyFish4_velocity = -5
key_collected = False
gameWin = False



#level 2
level2_objects = []
# Ball starting position(initially off the screen)








title_label = lcd.add_label(group, "Marble Game", 120, 30, color = 0xFFFFFF, scale = 3)
start_label = lcd.add_label(group, "Press Button to Start", 120, 80, color = 0xFFFFFF, scale = 1)




level_label = lcd.add_label(group, "", 120, 40, color = 0x0000FF, scale = 4)
circle = lcd.draw_circle(1000, 1000, radius, fill=0xFFFFFF, outline=0x000000)
group.append(circle)










def level1():
    global level1_objects
    global level1_enemies
    global key
    global goal
    circle.x = 23
    circle.y = 100
    circle.fill = 0xFFFF00
    border = lcd.draw_rect(0, 0, 240, 135, fill=None, outline=0xFF0000, stroke=5)
    staticWall1 = lcd.draw_rect(50, 50, 10, 85, fill=0xFF0000, outline=0xFF0000, stroke=2)
    staticWall2 = lcd.draw_rect(185, 0, 10, 85, fill=0xFF0000, outline=0xFF0000, stroke=2)
    

    level1_enemies = [enemyFish1, enemyFish2, enemyFish3, enemyFish4]
    for enemy in level1_enemies:
        group.append(enemy)

    level1_objects = [border, staticWall1, staticWall2, key, goal]
    for obj in level1_objects:
        group.append(obj)

def level1_enemies_gameplay():
    global level_running
    global level1_objects
    global level1_enemies
    global enemyFish1_velocity
    global enemyFish2_velocity
    global enemyFish3_velocity
    global enemyFish4_velocity
    enemyFish_radius = 10
    
    def circleCapture():
        def collided(enemy):
            dx = (circle.x+radius) - (enemy.x+enemyFish_radius)
            dy = (circle.y+radius) - (enemy.y+enemyFish_radius)
            total_radius = radius + enemyFish_radius
            return dx * dx + dy * dy <= total_radius * total_radius

        for enemy in level1_enemies:
            if collided(enemy):
                return True
        return False


    if(circleCapture()):
        level_running = False
        print("Game Over")

    if(enemyFish1.x + enemyFish_radius == 80  or enemyFish1.x + enemyFish_radius == 170):
        enemyFish1_velocity = -enemyFish1_velocity
    if(enemyFish2.x + enemyFish_radius == 80  or enemyFish2.x + enemyFish_radius == 170):
        enemyFish2_velocity = -enemyFish2_velocity
    if(enemyFish3.x + enemyFish_radius == 80  or enemyFish3.x + enemyFish_radius == 170):
        enemyFish3_velocity = -enemyFish3_velocity
    if(enemyFish4.x + enemyFish_radius == 80  or enemyFish4.x + enemyFish_radius == 170):
        enemyFish4_velocity = -enemyFish4_velocity
    enemyFish1.x += enemyFish1_velocity
    enemyFish2.x += enemyFish2_velocity
    enemyFish3.x += enemyFish3_velocity
    enemyFish4.x += enemyFish4_velocity
    circleCapture()
    time.sleep(0.1)
    
def level1_gameplay():
    global level_running
    global level1_objects
    global level1_enemies
    global key
    global goal
    global key_collected
    global radius
    global gameWin
    walls = [[50, 50, 10, 85], [185, 0, 10, 85]]
    step = 4

    def circle_rect_collision(cx, cy, r, rx, ry, rw, rh):
        closest_x = rx if cx < rx else (rx + rw if cx > rx + rw else cx)
        closest_y = ry if cy < ry else (ry + rh if cy > ry + rh else cy)
        dx = cx - closest_x
        dy = cy - closest_y
        return dx * dx + dy * dy <= r * r

    def can_move_to(x, y):
        if x - radius < 0 or x + radius > 240 or y - radius < 0 or y + radius > 135:
            return False
        for wall in walls:
            if circle_rect_collision(x+radius, y+radius, radius, wall[0], wall[1], wall[2], wall[3]):
                return False
        return True

    target_x = circle.x
    target_y = circle.y
    if imu.tilt_angle_x > 5:
        target_y -= step
    if imu.tilt_angle_y > 5:
        target_x += step
    if imu.tilt_angle_x < -5:
        target_y += step
    if imu.tilt_angle_y < -5:
        target_x -= step

    if can_move_to(target_x, target_y):
        circle.x = target_x
        circle.y = target_y
    else:
        if can_move_to(target_x, circle.y):
            circle.x = target_x
        elif can_move_to(circle.x, target_y):
            circle.y = target_y

    if(circle.x >= 195 and circle.y <= 45):
        key.fill = None
        goal.fill = 0x00FF00
        key_collected = True
        print("Key Collected")

    print(circle.x, circle.y)
    if(key_collected and circle.x < 50 and circle.y >= 85):
        level_running = False
        print("Level Complete")
        gameWin = True
        print(gameWin)




def level2():
    global level2_objects
    circle.x= 12
    circle.y = 107
    circle.fill = 0xFF0000
    border = lcd.draw_rect(0, 0, 240, 135, fill=None, outline=0xFF0000, stroke=5)
    wall1 = lcd.draw_rect(35, 35, 5, 100, fill=0xFF0000, outline=0xFF0000, stroke=2)
    wall2 = lcd.draw_rect(110, 0, 5, 40, fill=0xFF0000, outline=0xFF0000, stroke=2)
    wall3 = lcd.draw_rect(160, 40, 80, 5, fill=0xFF0000, outline=0xFF0000, stroke=2)
    wall4 = lcd.draw_rect(75, 70, 5, 35, fill=0xFF0000, outline=0xFF0000, stroke=2)
    wall5 = lcd.draw_rect(75, 90, 40, 5, fill=0xFF0000, outline=0xFF0000, stroke=2)
    wall6 = lcd.draw_rect(160, 90, 5, 45, fill=0xFF0000, outline=0xFF0000, stroke=2)
    goal = lcd.draw_rect(200, 5, 35, 35, fill=0x00FF00, outline=0x00FF00, stroke=2)
    level2_objects = [border, wall1, wall2, wall3, wall4, wall5, wall6, goal]
    for obj in level2_objects:
        group.append(obj)

def level2_gameplay():    
    global level_running
    global radius
    isMoving = False
    direction = ""

    walls = [[35, 35, 5, 100], [110, 0, 5, 40], [160, 40, 80, 5], [75, 70, 5, 35], [75, 90, 40, 5], [160, 90, 5, 45]]
    step = 2

    def circle_rect_collision(cx, cy, r, rx, ry, rw, rh):
        # Clamp circle center to closest point on rectangle
        if cx < rx:
            closest_x = rx
        elif cx > rx + rw:
            closest_x = rx + rw
        else:
            closest_x = cx
        
        if cy < ry:
            closest_y = ry
        elif cy > ry + rh:
            closest_y = ry + rh
        else:
            closest_y = cy
        
        dx = cx - closest_x
        dy = cy - closest_y
        return (dx * dx + dy * dy) <= (r * r)

    def will_collide_at(x, y):
        cx = x + radius
        cy = y + radius
        for w in walls:
            if circle_rect_collision(cx, cy, radius, w[0], w[1], w[2], w[3]):
                return True
        return False

    # Up
    if imu.tilt_angle_x > 5:
        if not isMoving:
            isMoving = True
            direction = "up"
        while isMoving and circle.y > 10 and direction == "up":
            next_y = circle.y - step
            if will_collide_at(circle.x, next_y):
                isMoving = False
                direction = ""
                break
            circle.y = next_y
            time.sleep(0.01)

    # Down
    if imu.tilt_angle_x < -5:
        if not isMoving:
            isMoving = True
            direction = "down"
        while isMoving and circle.y < 111 and direction == "down":
            next_y = circle.y + step
            if will_collide_at(circle.x, next_y):
                isMoving = False
                direction = ""
                break
            circle.y = next_y
            time.sleep(0.01)

    # Left
    if imu.tilt_angle_y < -5:
        if not isMoving:
            isMoving = True
            direction = "left"
        while isMoving and circle.x > 10 and direction == "left":
            next_x = circle.x - step
            if will_collide_at(next_x, circle.y):
                isMoving = False
                direction = ""
                break
            circle.x = next_x
            time.sleep(0.01)

    # Right
    if imu.tilt_angle_y > 5:
        if not isMoving:
            isMoving = True
            direction = "right"
        while isMoving and circle.x < 216 and direction == "right":
            next_x = circle.x + step
            if will_collide_at(next_x, circle.y):
                isMoving = False
                direction = ""
                break
            circle.x = next_x
            time.sleep(0.01)
    if(circle.x >= 200 and circle.y <= 40):
        level_running = False
    time.sleep(0.1)




def update_levelColor():
    if(level == 0):
        level_label.color = (0x0000FF)
    elif(level == 1):
        level_label.color = (0x00FFFF)
    elif(level == 2):
        level_label.color = (0x00FF00)
    elif(level == 3):
        level_label.color = (0xFFFF00)
    elif(level == 4):
        level_label.color = (0xFF0000)





while True:
    if(btn.is_pressed()):
        start = True
        title_label.text = ""
        start_label.text = "Starting..."
        time.sleep(1)
        start_label.text = ""
        level_label.text = (levels[level])
    while start:
        #Level Selection
        if(imu.tilt_angle_y > 15 and level_change == False) and (level_selected == False):
            if(level < 4):    
                level +=1
            else:
                level = 0
       
            level_label.text = (levels[level])
            level_change = True




        if(imu.tilt_angle_y < -15 and level_change == False) and (level_selected == False):
            if(level > 0):
                level -=1
            else:
                level = 4
            level_label.text = (levels[level])
            level_change = True
        if(-15 <= imu.tilt_angle_y <= 15):
            level_change = False
        update_levelColor()
        if(btn.is_pressed()):
            level_selected = True
            level_label.text = ("")
            if(level == 0):
                palette[0] = (0x0000FF)
                level_running = True
                level1()
                while(level_running):
                    level1_enemies_gameplay()
                    level1_gameplay()
                for obj in level1_objects:
                    group.remove(obj)
                level1_objects.clear()
                for enemy in level1_enemies:
                    group.remove(enemy)
                level1_enemies.clear()
                palette[0] = (0x000000)
                level_selected = False
                key_collected = False
                key.fill = (0x00FF00)
                goal.fill = None
                circle.x = 1000
                circle.y = 1000
                if(gameWin):    
                    start_label.text = ("Level 1 Complete")
                else:
                    start_label.text = ("Level 1 Failed")
                gameWin = False
                time.sleep(1)
                start_label.text = ("")
                level_label.text = ("Level 1")
            
            elif(level == 1):
                palette[0] = (0x00FFFF)
                level_running = True
                level2()
                while(level_running):
                    level2_gameplay()
                for obj in level2_objects:
                    group.remove(obj)
                level2_objects.clear()
                palette[0] = (0x000000)
                level_selected = False
                start_label.text = ("Level 2 Complete")
                time.sleep(1)
                start_label.text = ("")
                level_label.text = ("Level 2")
                circle.x = 1000
                circle.y = 1000
                
            elif(level == 2):
                palette[0] = (0x00FF00)
            elif(level == 3):
                palette[0] = (0xFFFF00)
            elif(level == 4):
                palette[0] = (0xFF0000)








