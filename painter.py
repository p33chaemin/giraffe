from tkinter import *
from tkinter import filedialog, colorchooser, simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter

# 전역 변수 정의
start_x = None
start_y = None
shape_mode = False
text_mode = False
line_mode = False
current_shape = None
brush_mode = True
actions = []
color_palette = None
image = None
canvas_img = None


# 마우스 이벤트 콜백 함수
def paint(event):
    global start_x, start_y
    brush_size = brush_slider.get()
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)

    if eraser_on.get():
        canvas.create_oval(x1, y1, x2, y2, fill='white', outline='white')
        draw.ellipse([x1, y1, x2, y2], fill='white', outline='white')
        actions.append(('oval', (x1, y1, x2, y2), 'white'))
    elif shape_mode:
        if current_shape == "Rectangle":
            canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=color.get())
            draw.rectangle([start_x, start_y, event.x, event.y], outline=color.get())
            actions.append(('rectangle', (start_x, start_y, event.x, event.y), color.get()))
        elif current_shape == "Oval":
            canvas.create_oval(start_x, start_y, event.x, event.y, outline=color.get())
            draw.ellipse([start_x, start_y, event.x, event.y], outline=color.get())
            actions.append(('oval', (start_x, start_y, event.x, event.y), color.get()))
    elif text_mode:
        add_text(event)
    elif brush_mode:
        canvas.create_oval(x1, y1, x2, y2, fill=color.get(), outline=color.get())
        draw.ellipse([x1, y1, x2, y2], fill=color.get(), outline=color.get())
        actions.append(('oval', (x1, y1, x2, y2), color.get()))
    elif line_mode:
        if start_x is not None and start_y is not None:
            canvas.create_line(start_x, start_y, event.x, event.y, fill=color.get(), width=brush_size)
            draw.line([start_x, start_y, event.x, event.y], fill=color.get(), width=brush_size)
            actions.append(('line', (start_x, start_y, event.x, event.y), color.get(), brush_size))
        start_x, start_y = event.x, event.y


# 텍스트 삽입 함수
def add_text(event):
    text = simpledialog.askstring("텍스트 입력", "추가할 텍스트를 입력하세요:")
    if text:
        x, y = event.x, event.y
        canvas.create_text(x, y, text=text, fill=color.get(), font=('Helvetica', 16))
        draw.text((x, y), text, fill=color.get())
        actions.append(('text', (x, y), text, color.get()))


# 그림판 초기화 함수( 메인 그림판 화면)
def initialize_paint():
    global canvas, brush_slider, color, eraser_on, image, draw, shape_button, start_x, start_y, text_button, color_palette

    # 기존 창 숨기기
    ggp.withdraw()
    ggp.resizable(False, False)  # 창 크기 조절 불가

    paint_window = Toplevel(ggp)
    paint_window.title("잘그린기린그림 그림판")

    canvas = Canvas(paint_window, width=800, height=500, bg='white')
    canvas.pack()

    # 버튼
    brush_slider = Scale(paint_window, from_=1, to=50, orient=HORIZONTAL, label='브러시 크기')
    brush_slider.pack(side=LEFT)
    brush_slider.set(5)

    eraser_on = BooleanVar()
    eraser_button = Checkbutton(paint_window, text="지우개", variable=eraser_on)
    eraser_button.pack(side=LEFT)

    brush_button = Menubutton(paint_window, text="브러시 선택", relief=RAISED)
    brush_menu = Menu(brush_button, tearoff=0)
    brush_menu.add_radiobutton(label="점", command=activate_brush_mode)
    brush_menu.add_radiobutton(label="선", command=activate_line_mode)
    brush_button.pack(side=LEFT)
    brush_button.config(menu=brush_menu)

    color = StringVar()
    color.set('black')
    color_button = Button(paint_window, text="색 선택", command=choose_color)
    color_button.pack(side=LEFT)
    # 색상 팔레트 표시
    color_palette = Label(paint_window, text="●", fg=color.get(), font=('Helvetica', 24))
    color_palette.pack(side=LEFT)

    load_button = Button(paint_window, text="불러오기", command=load_file)
    load_button.pack(side=RIGHT)

    save_button = Button(paint_window, text="저장", command=save_file)
    save_button.pack(side=RIGHT)

    reset_button = Button(paint_window, text="리셋", command=reset_canvas)
    reset_button.pack(side=RIGHT)

    undo_button = Button(paint_window, text="뒤로 가기", command=undo)
    undo_button.pack(side=LEFT)

    shape_button = Menubutton(paint_window, text="도형 선택", relief=RAISED)
    shape_menu = Menu(shape_button, tearoff=0)
    shape_menu.add_radiobutton(label="Rectangle", command=lambda: set_shape_mode("Rectangle"))
    shape_menu.add_radiobutton(label="Oval", command=lambda: set_shape_mode("Oval"))
    shape_button.pack(side=LEFT)
    shape_button.config(menu=shape_menu)

    text_button = Button(paint_window, text="텍스트 추가", command=activate_text_mode)
    text_button.pack(side=LEFT)

    filter_button = Menubutton(paint_window, text="필터 선택", relief=RAISED)
    filter_menu = Menu(filter_button, tearoff=0)
    filter_menu.add_command(label="흑백", command=apply_grayscale_filter)
    filter_menu.add_command(label="블러", command=apply_blur_filter)
    filter_menu.add_command(label="경계 강조", command=apply_edge_filter)
    filter_button.pack(side=LEFT)
    filter_button.config(menu=filter_menu)


    image = Image.new("RGB", (800, 500), 'white')
    draw = ImageDraw.Draw(image)
    # 바인딩
    canvas.bind("<B1-Motion>", paint)
    canvas.bind("<Button-1>", start)

    # 단축키 바인딩
    paint_window.bind("<Control-z>", lambda event: undo())
    paint_window.bind("<Control-s>", lambda event: save_file())
    paint_window.bind("<Control-o>", lambda event: load_file())


def start(event):
    global start_x, start_y, shape_mode
    start_x, start_y = event.x, event.y
    if shape_mode:
        canvas.bind("<B1-Motion>", draw_shape)


# 색상 선택 함수
def choose_color():
    new_color = colorchooser.askcolor(color=color.get())[1]
    if new_color:
        color.set(new_color)
        color_palette.config(fg=new_color)


# 뒤로 가기 함수
def undo():
    if actions:
        last_action = actions.pop()
        image.paste(Image.new("RGB", (800, 500), 'white'), (0, 0))
        draw = ImageDraw.Draw(image)
        canvas.delete("all")
        for action in actions:
            if action[0] == 'oval':
                canvas.create_oval(action[1], fill=action[2], outline=action[2])
                draw.ellipse(action[1], fill=action[2], outline=action[2])
            elif action[0] == 'rectangle':
                canvas.create_rectangle(action[1], outline=action[2])
                draw.rectangle(action[1], outline=action[2])
            elif action[0] == 'text':
                canvas.create_text(action[1], text=action[2], fill=action[3], font=('Helvetica', 16))
                draw.text(action[1], action[2], fill=action[3])
            elif action[0] == 'line':
                canvas.create_line(action[1], fill=action[2], width=action[3])
                draw.line(action[1], fill=action[2], width=action[3])


# 텍스트 모드 함수
def activate_text_mode():
    global text_mode, shape_mode, brush_mode, line_mode
    text_mode = True
    shape_mode = False
    brush_mode = False
    line_mode = False


# 도형 그리기 함수
def set_shape_mode(shape):
    global shape_mode, text_mode, brush_mode, line_mode, current_shape
    shape_mode = True
    text_mode = False
    brush_mode = False
    line_mode = False
    current_shape = shape  # 전달받은 인자를 current_shape에 저장


# 브러시 점  모드 함수
def activate_brush_mode():
    global shape_mode, text_mode, brush_mode, line_mode
    shape_mode = False
    text_mode = False
    brush_mode = True
    line_mode = False


# 브러시 선 모드 함수
def activate_line_mode():
    global shape_mode, text_mode, brush_mode, line_mode
    shape_mode = False
    text_mode = False
    brush_mode = False
    line_mode = True

 # filter 함수
def apply_grayscale_filter():
    global image, canvas
    # 흑백 필터 적용
    filtered_image = image.convert("L").convert("RGB")
    update_canvas(filtered_image)

def apply_blur_filter():
    global image, canvas
    # 블러 필터 적용
    filtered_image = image.filter(ImageFilter.BLUR)
    update_canvas(filtered_image)

def apply_edge_filter():
    global image, canvas
    # 경계 강조 필터 적용
    filtered_image = image.filter(ImageFilter.FIND_EDGES)
    update_canvas(filtered_image)

#캔버스업데이트
def update_canvas(new_image):
    global image, canvas_img
    image.paste(new_image)
    canvas_img = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=canvas_img, anchor=NW)


# 리셋 함수
def reset_canvas():
    global actions, image, draw
    canvas.delete("all")
    actions = []
    image = Image.new("RGB", (800, 500), 'white')
    draw = ImageDraw.Draw(image)


# 도움말 표시 함수 (도움말 화면)
def show_help():
    help_window = Toplevel(ggp)
    help_window.title("잘그린기린 도움말")
    help_window.geometry("600x700")  # 창 크기 설정
    help_window.resizable(False, False)  # 창 크기 조절 불가

    # 도움말 이미지 로드
    help_image_path = r"C:\Project\giraffe\images\help.png"  # 도움말 이미지 경로를 설정
    help_image = Image.open(help_image_path)
    help_image = help_image.resize((600, 700), Image.LANCZOS)  # 이미지 크기 조절
    help_img = ImageTk.PhotoImage(help_image)

    # 이미지 라벨 생성 및 배치
    image_label = Label(help_window, image=help_img)
    image_label.image = help_img  # 이미지를 전역 변수로 유지
    image_label.pack(pady=10)


# 파일 저장 함수
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
    if file_path:
        image.save(file_path)


# 파일 불러오기 함수
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[('PNG files', '*.png')])
    if file_path:
        try:
            loaded_image = Image.open(file_path)
            image.paste(loaded_image)
            canvas_image = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, image=canvas_image, anchor=NW)
            # 저장하여 다시 사용할 수 있도록 전역 변수 설정
            global canvas_img
            canvas_img = canvas_image
        except Exception as e:
            print("파일을 열 수 없습니다:", e)


# 초기화 함수( 첫 화면)
def initialize():
    global ggp
    global bg_image
    global start_img, help_img

    # Tkinter 창 생성
    ggp = Tk()
    ggp.title("잘그린기린그림 시작 화면")
    ggp.geometry("800x600")  # 창 크기 설정
    ggp.resizable(False, False)  # 창 크기 조절 불가

    # 배경 이미지 로드
    bg_image_path = r"C:\Project\giraffe\images\ggp.png"  # 배경 이미지 경로를 설정
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)

    # 캔버스 생성 및 배경 이미지 표시
    canvas = Canvas(ggp, width=800, height=600)
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor=NW)

    # 시작 버튼 이미지 로드 및 크기 조절
    start_image_path = r"C:\Project\giraffe\images\start_button.png"  # 시작 버튼 이미지 경로를 설정
    start_image = Image.open(start_image_path)
    start_image = start_image.resize((199, 61), Image.LANCZOS)  # 버튼 크기 조절
    start_img = ImageTk.PhotoImage(start_image)

    # 도움말 버튼 이미지 로드 및 크기 조절
    help_image_path = r"C:\Project\giraffe\images\help_button.png"  # 도움말 버튼 이미지 경로를 설정
    help_image = Image.open(help_image_path)
    help_image = help_image.resize((199, 61), Image.LANCZOS)  # 버튼 크기 조절
    help_img = ImageTk.PhotoImage(help_image)

    # 시작 버튼 생성
    start_button = Button(ggp, image=start_img, command=initialize_paint, bd=0)
    start_button.image = start_img  # 이미지를 전역 변수로 유지
    start_button.place(x=300, y=440)  # 버튼 위치 설정

    # 도움말 버튼 생성
    help_button = Button(ggp, image=help_img, command=show_help, bd=0)
    help_button.image = help_img  # 이미지를 전역 변수로 유지
    help_button.place(x=300, y=510)  # 버튼 위치 설정

    # 루프 시작
    ggp.mainloop()


if __name__ == "__main__":
    initialize()
