from ursina import *
from solve_2d_cube import *
import cv2
import random


app = Ursina(title='MY RUBIK CUBE',icon='assets/textures/favicon.ico')
class RubikCube(Entity):
    # thuộc tính phần mềm
    def __init__(self, **kwargs):
        super().__init__()
        sky = Sky(texture='sky_sunset')
        window.borderless = False
        EditorCamera()
        camera.world_position = (0,0,-20)

        self.solution = ""
        self.speed_up_move = 0
        self.normal_move = 0.5
        self.delay_move = 0.08
        self.step = 0
        self.firstCall = True
        self.myvalues = ""
        self.re_conv = {
            # "F" : "F'",
            # "F'" : "F",
            # "F2" : "F2",
            # "R" : "R'",
            # "R2" : "R2",
            # "R'" : "R",
            # "B" : "B'",
            # "B2" : "B2",
            # "B'" : "B",
            # "L" : "L'",
            # "L2" : "L2",
            # "L'" : "L",
            # "U" : "U'",
            # "U2" : "U2",
            # "U'" : "U",
            # "D" : "D'",
            # "D2" : "D2",
            # "D'" : "D",
            "F": "f'",
            "F'": "f",
            "F2": "f2",
            "R": "r'",
            "R2": "r2",
            "R'": "r",
            "B": "b'",
            "B2": "b2",
            "B'": "b",
            "L": "l'",
            "L2": "l2",
            "L'": "l",
            "U": "u'",
            "U2": "u2",
            "U'": "u",
            "D": "d'",
            "D2": "d2",
            "D'": "d",
        }
        self.state = {
            'up': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
            'right': ['white', 'white', 'white', 'white', 'red', 'white', 'white', 'white', 'white', ],
            'front': ['white', 'white', 'white', 'white', 'green', 'white', 'white', 'white', 'white', ],
            'down': ['white', 'white', 'white', 'white', 'yellow', 'white', 'white', 'white', 'white', ],
            'left': ['white', 'white', 'white', 'white', 'orange', 'white', 'white', 'white', 'white', ],
            'back': ['white', 'white', 'white', 'white', 'blue', 'white', 'white', 'white', 'white', ]
        }
        self.origin_state = {
            'up': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
            'right': ['red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', ],
            'front': ['green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', ],
            'down': ['yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', ],
            'left': ['orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', ],
            'back': ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', ]
        }
        self.stickers = {
            'main': [
                [200, 120], [300, 120], [400, 120],
                [200, 220], [300, 220], [400, 220],
                [200, 320], [300, 320], [400, 320]
            ],
            'current': [
                [20, 20], [54, 20], [88, 20],
                [20, 54], [54, 54], [88, 54],
                [20, 88], [54, 88], [88, 88]
            ],
            'preview': [
                [20, 130], [54, 130], [88, 130],
                [20, 164], [54, 164], [88, 164],
                [20, 198], [54, 198], [88, 198]
            ],
            'left': [
                [50, 280], [94, 280], [138, 280],
                [50, 324], [94, 324], [138, 324],
                [50, 368], [94, 368], [138, 368]
            ],
            'front': [
                [188, 280], [232, 280], [276, 280],
                [188, 324], [232, 324], [276, 324],
                [188, 368], [232, 368], [276, 368]
            ],
            'right': [
                [326, 280], [370, 280], [414, 280],
                [326, 324], [370, 324], [414, 324],
                [326, 368], [370, 368], [414, 368]
            ],
            'up': [
                [188, 128], [232, 128], [276, 128],
                [188, 172], [232, 172], [276, 172],
                [188, 216], [232, 216], [276, 216]
            ],
            'down': [
                [188, 434], [232, 434], [276, 434],
                [188, 478], [232, 478], [276, 478],
                [188, 522], [232, 522], [276, 522]
            ],
            'back': [
                [464, 280], [508, 280], [552, 280],
                [464, 324], [508, 324], [552, 324],
                [464, 368], [508, 368], [552, 368]
            ],
        }
        self.check_state = []
        self.solved = False

        self.load_game()

    # setup phần mềm
    def load_game(self):

        self.create_cube_positions()
        self.CUBES = [Entity(model='models/custom_cube', texture= 'textures/my_rubik_texture', position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity(model = 'models/custom_cube', texture = 'textures/dirt', position = (0,0,0))
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'UP': 'y', 'DOWN': 'y', 'FRONT': 'z', 'BACK': 'z'}
        self.cubes_side_positons = {'LEFT': self.LEFT, 'DOWN': self.DOWN, 'RIGHT': self.RIGHT, 'FRONT': self.FRONT,
                                    'BACK': self.BACK, 'UP': self.UP}
        #self.test_cube = Entity(model = 'cube', position = (-.5,0,0), color = rgb(1,0.5,0), scale = (.1,.95,.95), parent = self.CUBES[0])
        # self.test_cube.parent = self.CUBES[0]
        self.animation_time = 0.2
        self.action_trigger = True
        self.set_color_cube()
        self.my_ui()


        #self.test_cube = Entity(model = 'cube', position = (2,0,0), color = rgb(0,0,0), collider = 'box')

    # giao diện
    def my_ui(self):
        self.my_step_ui = Text(origin=(0, -15), scale_override = 3)
        self.my_solution_ui = Text(origin=(0, -13), scale_override = 2)
        camera_ui = Text(origin = (-0.5,0.5), color = rgb(0,0,0), position = (-0.83,0.15))
        message_ui = Text(origin=(0,13))
        step_solve_ui = Text()

        message_ui.text = dedent("Sử dụng URFLDB để di chuyển khối rubik  ").strip()
        camera_ui.text = dedent("E: trở lại khối rubik hoàn chỉnh\n\n\nO: mở camera\n\n\nI: giải từng bước\n\n\nS: xáo").strip()
        self.my_step_ui.text = dedent("Hi!")
        camera_ui.create_background(color= rgb(1,1,1))
        camera_ui.align()

    # mã hóa khối rubik
    def set_color_cube(self):
        for cube in self.CUBES:
            # for understand kociemba
            # if cube.position == Vec3(-1, 0, -1):
            #     Entity(model='cube', position = (0,0,-0.5), color = rgb(0,0,0), scale = (.7,.7,.1), parent = cube)
            #     print('find it')
            # if cube.position == Vec3(1, 0, -1):
            #     Entity(model='cube', position = (0,0,-0.5), color = rgb(0,0,0), scale = (.7,.7,.1), parent = cube)
            # if cube.position == Vec3(1,0,1):
            #     Entity(model='cube', position = (0,0,0.5), color = rgb(0,0,0), scale = (.7,.7,.1), parent = cube)
            # if cube.position == Vec3(-1,0,1):
            #     Entity(model='cube', position = (0,0,0.5), color = rgb(0,0,0), scale = (.7,.7,.1), parent = cube)
            # Entity(model='cube', position = (0, 0.5, 0), color = rgb(0,0,0), scale = (.7,.1,.7), parent = cube)
            # Entity(model='cube', position = (0, -0.5, 0), color = rgb(0,0,0), scale = (.7,.1,.7), parent = cube)



            Entity(model='cube', position=(-.5, 0, 0), color=rgb(1, 0.5, 0), scale=(.02, .9, .9),
                                    parent=cube, collider = 'box')
            Entity(model='cube', position=(.5, 0, 0), color=rgb(1, 0, 0), scale=(.02, .9, .9),
                                    parent=cube, collider = 'box')
            Entity(model='cube', position=(0, 0, -0.5), color=rgb(0, 1, 0), scale=(.9, .9, .02),
                                    parent=cube, collider = 'box')
            Entity(model='cube', position=(0, 0, 0.5), color=rgb(0, 0, 1), scale=(.9, .9, .02),
                                    parent=cube, collider = 'box')
            Entity(model='cube', position=(0, 0.5, 0), color=rgb(1, 1, 1), scale=(.9, .02, .9),
                                    parent=cube, collider = 'box')
            Entity(model='cube', position=(0, -0.5, 0), color=rgb(1, 1, 0), scale=(.9, .02, .9),
                                    parent=cube, collider = 'box')
            print(cube.position)
    def read_cube_up(self):
        z=1
        st = 0
        while z >= -1:
            for x in range(-1,2):
                hit = raycast(origin=(x,3,z), direction=(0,-1,0), distance=3, debug=False)
                if(hit.entity.color == rgb(1,0,0)):
                    self.state['up'][st] = 'red'
                if (hit.entity.color == rgb(1, 1, 1)):
                    self.state['up'][st] = 'white'
                if(hit.entity.color == rgb(0,0,1)):
                    self.state['up'][st] = 'blue'
                if(hit.entity.color == rgb(0,1,0)):
                    self.state['up'][st] = 'green'
                if(hit.entity.color == rgb(1,1,0)):
                    self.state['up'][st] = 'yellow'
                if(hit.entity.color == rgb(1,0.5,0)):
                    self.state['up'][st] = 'orange'
                st += 1
            z -= 1
    def read_cube_down(self):
        z=-1
        st = 0
        while z <= 1:
            for x in range(-1,2):
                hit = raycast(origin=(x,-3,z), direction=(0,1,0), distance=3, debug=False)
                if(hit.entity.color == rgb(1,0,0)):
                    self.state['down'][st] = 'red'
                if (hit.entity.color == rgb(1, 1, 1)):
                    self.state['down'][st] = 'white'
                if(hit.entity.color == rgb(0,0,1)):
                    self.state['down'][st] = 'blue'
                if(hit.entity.color == rgb(0,1,0)):
                    self.state['down'][st] = 'green'
                if(hit.entity.color == rgb(1,1,0)):
                    self.state['down'][st] = 'yellow'
                if(hit.entity.color == rgb(1,0.5,0)):
                    self.state['down'][st] = 'orange'
                st += 1
            z += 1
    def read_cube_front(self):
        y=1
        st = 0
        while y >= -1:
            for x in range(-1,2):
                hit = raycast(origin=(x,y,-3), direction=(0,0,1), distance=3, debug=False)
                if(hit.entity.color == rgb(1,0,0)):
                    self.state['front'][st] = 'red'
                if (hit.entity.color == rgb(1, 1, 1)):
                    self.state['front'][st] = 'white'
                if(hit.entity.color == rgb(0,0,1)):
                    self.state['front'][st] = 'blue'
                if(hit.entity.color == rgb(0,1,0)):
                    self.state['front'][st] = 'green'
                if(hit.entity.color == rgb(1,1,0)):
                    self.state['front'][st] = 'yellow'
                if(hit.entity.color == rgb(1,0.5,0)):
                    self.state['front'][st] = 'orange'
                st += 1
            y -= 1
    def read_cube_back(self):
        y=1
        st = 0
        while y >= -1:
            x = 1
            while x >= -1:
                hit = raycast(origin=(x,y,3), direction=(0,0,-1), distance=3, debug=False)
                if(hit.entity.color == rgb(1,0,0)):
                    self.state['back'][st] = 'red'
                if (hit.entity.color == rgb(1, 1, 1)):
                    self.state['back'][st] = 'white'
                if(hit.entity.color == rgb(0,0,1)):
                    self.state['back'][st] = 'blue'
                if(hit.entity.color == rgb(0,1,0)):
                    self.state['back'][st] = 'green'
                if(hit.entity.color == rgb(1,1,0)):
                    self.state['back'][st] = 'yellow'
                if(hit.entity.color == rgb(1,0.5,0)):
                    self.state['back'][st] = 'orange'
                x -= 1
                st += 1
            y -= 1
    def read_cube_left(self):
        y=1
        st = 0
        while y >= -1:
            z = 1
            while z >= -1:
                hit = raycast(origin=(-3,y,z), direction=(1,0,0), distance=3, debug=False)
                if(hit.entity.color == rgb(1,0,0)):
                    self.state['left'][st] = 'red'
                if (hit.entity.color == rgb(1, 1, 1)):
                    self.state['left'][st] = 'white'
                if(hit.entity.color == rgb(0,0,1)):
                    self.state['left'][st] = 'blue'
                if(hit.entity.color == rgb(0,1,0)):
                    self.state['left'][st] = 'green'
                if(hit.entity.color == rgb(1,1,0)):
                    self.state['left'][st] = 'yellow'
                if(hit.entity.color == rgb(1,0.5,0)):
                    self.state['left'][st] = 'orange'
                z -= 1
                st += 1
            y -= 1
    def read_cube_right(self):
        y=1
        st = 0
        while y >= -1:
            for z in range(-1,2):
                hit = raycast(origin=(3,y,z), direction=(-1,0,0), distance=3, debug=False)
                if(hit.entity.color == rgb(1,0,0)):
                    self.state['right'][st] = 'red'
                if (hit.entity.color == rgb(1, 1, 1)):
                    self.state['right'][st] = 'white'
                if(hit.entity.color == rgb(0,0,1)):
                    self.state['right'][st] = 'blue'
                if(hit.entity.color == rgb(0,1,0)):
                    self.state['right'][st] = 'green'
                if(hit.entity.color == rgb(1,1,0)):
                    self.state['right'][st] = 'yellow'
                if(hit.entity.color == rgb(1,0.5,0)):
                    self.state['right'][st] = 'orange'
                st += 1
            y -= 1

    # đọc khối rubik
    def take_state(self):
        self.read_cube_up()
        self.read_cube_down()
        self.read_cube_front()
        self.read_cube_back()
        self.read_cube_left()
        self.read_cube_right()

        #self.solution = detect_solve(self.state)
        #print(self.solution)

    # phá đập đi xây lại các khối rubik
    def reset_cube(self):
        for cube in self.CUBES:
            destroy(cube)
        self.CUBES = [Entity(model='models/custom_cube', texture= 'textures/my_rubik_texture', position=pos) for pos in self.SIDE_POSITIONS]
        self.set_color_cube()
        print("Cube reset!")

    # tạo vị trí và xoay khối rubik
    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger
    def rotate_side(self, side_name, degree):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(degree, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + self.delay_move)
    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0
    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.DOWN = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FRONT = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.UP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.DOWN | self.FRONT | self.BACK | self.RIGHT | self.UP
    # ngẫu nhiên 25 bước để xáo khối rubik
    def scramble(self):
        possible_move = ['l','r','u','d','b','f']
        self.speed_up_move = 0
        for i in range(25):
            self.move(random.choice(possible_move))
        self.speed_up_move = self.normal_move

    # sử dụng camera để nhận diện khối rubik
    def rubik_detect(self):
        print("Hi im rubik detect")
        print("Wait a second")

        my_warning = "Khoi rubik quet sai, vui long thu lai!"


        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3) 
        while True:
            hsv=[]
            current_state=[]
            ret,img=cap.read()
            #img=cv2.flip(img,1)
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = np.zeros(frame.shape, dtype=np.uint8)

            draw_stickers(img,self.stickers,'main')
            draw_stickers(img,self.stickers,'current')
            draw_preview_stickers(preview,self.stickers)
            fill_stickers(preview,self.stickers,self.state)
            texton_preview_stickers(preview,self.stickers)
            for i in range(9):
                hsv.append(frame[self.stickers['main'][i][1]+10][self.stickers['main'][i][0]+10])


            a=0
            for x,y in self.stickers['current']:
                color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
                cv2.rectangle(img,(x,y),(x+30,y+30),color[color_name],-1)
                a+=1
                current_state.append(color_name)

            k = cv2.waitKey(5) & 0xFF
            if k == ord('q'):
                break
            elif k ==ord('u'):
                self.state['up']=current_state
                self.check_state.append('u')
            elif k ==ord('r'):
                self.check_state.append('r')
                self.state['right']=current_state
            elif k ==ord('l'):
                self.check_state.append('l')
                self.state['left']=current_state
            elif k ==ord('d'):
                self.check_state.append('d')
                self.state['down']=current_state
            elif k ==ord('f'):
                self.check_state.append('f')
                self.state['front']=current_state
            elif k ==ord('b'):
                self.check_state.append('b')
                self.state['back']=current_state
            elif k == ord('\r'):
                # process(["R","R'"])
                if len(set(self.check_state))==6:
                    #Scan xong, lưu kết quả vào biến state
                    print("hi")
                    #lay cong thuc giai, dao nguoc va cho khoi rubik chay
                    try:
                        values = detect_solve(self.state)
                        #self.solution = values
                        #self.solution = list(values.split(" "))
                        values = list(values.split(" "))
                        values.reverse()
                        print(values)
                        self.delay_move = 0
                        self.speed_up_move = 0
                        for value in values:
                            value = self.re_conv[value]
                            lis_value = list(value)
                            if lis_value[-1] == '2':
                                lis_value.pop(-1)
                                value = ''.join(lis_value)
                                self.move(value)
                                self.move(value)
                                print('moving ' + value)
                            else:
                                self.move(value)
                                print('moving ' + value)
                        self.delay_move = 0.08
                        self.my_step_ui.text = dedent("Quét thành công, ấn I để bắt đầu giải")
                        break

                    except:
                        print("rubik error, scan again!")
                        cv2.putText(preview, my_warning, (10, 650), font, 1, (0,0,255), 1, cv2.LINE_AA)
                else:
                    #Chưa scan xong, thiếu mặt cần scan
                    print("")
                    print("left to scan:",6-len(set(self.check_state)))
                    cv2.putText(preview, my_warning, (10, 650), font, 1, (0,0,255), 1, cv2.LINE_AA)

            cv2.imshow('preview',preview)
            cv2.imshow('frame',img[0:500,0:500])
        cv2.destroyAllWindows()

    # giải từng bước
    def step_solve(self):
        # Check if the cube already solved
        self.take_state()
        if self.state == self.origin_state:
            self.my_solution_ui.text = dedent("Khối Rubik đã được giải")
            print("This cube is solved")
            return
        # if not, start the solve loop
        if self.firstCall:
            self.take_state()
            self.myvalues = detect_solve(self.state)
            self.my_solution_ui.text = dedent("Solution is: " + self.myvalues)
            print("solution is: " + self.myvalues)
            self.myvalues = list(self.myvalues.split(" "))
            self.step = 0
            self.firstCall = False
        if self.action_trigger:
            self.speed_up_move = self.normal_move + 0.5
            self.delay_move = 0.05
            self.move(self.myvalues[self.step].lower())
            print('moving ' + self.myvalues[self.step])
            self.step += 1

        if self.step == len(self.myvalues):
            self.step = 0
            self.firstCall = True
            self.delay_move = 0.08
            self.myvalues = ""


        # for value in values:
        #     lis_value = list(value)
        #     if lis_value[-1] == '2':
        #         lis_value.pop(-1)
        #         value = ''.join(lis_value)
        #         self.move(value)
        #         self.move(value)
        #         print('moving ' + value)
        #     else:
        #         self.move(value)
        #         print('moving ' + value)


    # hàm chuyển động khối rubik
    def move(self, value):
        if value == 'l' :
            self.animation_time = self.speed_up_move
            self.rotate_side('LEFT',-90)
        if value == 'd':
            self.animation_time = self.speed_up_move
            self.rotate_side('DOWN',-90)
        if value == 'r':
            self.animation_time = self.speed_up_move
            self.rotate_side('RIGHT',90)
        if value == 'f':
            self.animation_time = self.speed_up_move
            self.rotate_side('FRONT',90)
        if value == 'b':
            self.animation_time = self.speed_up_move
            self.rotate_side('BACK',-90)
        if value == 'u':
            self.animation_time = self.speed_up_move
            self.rotate_side('UP',90)

        if value == "l'" :
            self.animation_time = self.speed_up_move
            self.rotate_side('LEFT',90)
        if value == "d'":
            self.animation_time = self.speed_up_move
            self.rotate_side('DOWN',90)
        if value == "r'":
            self.animation_time = self.speed_up_move
            self.rotate_side('RIGHT',-90)
        if value == "f'":
            self.animation_time = self.speed_up_move
            self.rotate_side('FRONT',-90)
        if value == "b'":
            self.animation_time = self.speed_up_move
            self.rotate_side('BACK',90)
        if value == "u'":
            self.animation_time = self.speed_up_move
            self.rotate_side('UP',-90)

        if value == 'l2' :
            self.animation_time = self.speed_up_move
            self.rotate_side('LEFT',-180)
        if value == 'd2':
            self.animation_time = self.speed_up_move
            self.rotate_side('DOWN',-180)
        if value == 'r2':
            self.animation_time = self.speed_up_move
            self.rotate_side('RIGHT',180)
        if value == 'f2':
            self.animation_time = self.speed_up_move
            self.rotate_side('FRONT',180)
        if value == 'b2':
            self.animation_time = self.speed_up_move
            self.rotate_side('BACK',-180)
        if value == 'u2':
            self.animation_time = self.speed_up_move
            self.rotate_side('UP',180)

        self.my_step_ui.text = dedent(value.upper())

        # self.my_step.text = dedent(value.upper()).strip()


    # nhận diện phím bấm từ người dùng
    def input(self, key):
        if key == 't':
            print("test key")

        if key == 'e':
            self.reset_cube()
            self.my_step_ui.text = dedent("Đã giải!")
            self.firstCall = True
        if key == 'o':
            self.reset_cube()
            self.my_step_ui.text = dedent("Đang mở camera,...")
            print("opening camera...")
            self.rubik_detect()
            self.firstCall = True
        if key == 's' and self.action_trigger:
            self.scramble()
            self.my_step_ui.text = dedent("Đã xáo!")
            self.firstCall = True
        if key == 'i' and self.action_trigger:
            self.animation_time = self.normal_move
            self.step_solve()


        if key == 'l' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('LEFT',-90)
            self.my_step_ui.text = dedent("L")
            self.firstCall = True

        if key == 'd' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('DOWN',-90)
            self.my_step_ui.text = dedent("D")
            self.firstCall = True

        if key == 'r' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('RIGHT',90)
            self.my_step_ui.text = dedent("R")
            self.firstCall = True

        if key == 'f' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('FRONT',90)
            self.my_step_ui.text = dedent("F")
            self.firstCall = True

        if key == 'b' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('BACK',-90)
            self.my_step_ui.text = dedent("B")
            self.firstCall = True

        if key == 'u' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('UP',90)
            self.my_step_ui.text = dedent("U")
            self.firstCall = True


rubik = RubikCube()
app.run()