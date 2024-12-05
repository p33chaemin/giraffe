from tkinter import *
from tkinter import filedialog, colorchooser, simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw

# 전역 변수 정의
start_x = None
start_y = None
shape_mode = False
text_mode = False
current_shape = None
brush_mode = True
actions = []
color_palette = None
canvas_img = None

# 마우스 이벤트 콜백 함수
def paint(event):
    global start_x, start_y
    brush_size = brush_slider.get()
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)
    if eraser_on.get():
        canvas.create_oval(x1, y1, x2, y2, fill='white', outline='white')
    elif shape_mode:
        if current_shape == "Rectangle":
            canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=color.get())
        elif current_shape == "Oval":
            canvas.create_oval(start_x, start_y, event.x, event.y, outline=color.get())
    elif text_mode:
        add_text(event)
    else:
        canvas.create_oval(x1, y1, x2, y2, fill=color.get(), outline=color.get())

# 텍스트 삽입 함수
def add_text(event):
    text = simpledialog.askstring("텍스트 입력", "추가할 텍스트를 입력하세요:")
    if text:
        canvas.create_text(event.x, event.y, text=text, fill=color.get(), font=('Helvetica', 16))

# 그림판 초기화 함수
def initialize_paint():
    global canvas, brush_slider, color, eraser_on, image, draw

    # 기존 창 숨기기
    pp.withdraw()

    paint_window = Toplevel(pp)
    paint_window.title("그림판")

    canvas = Canvas(paint_window, width=800, height=500, bg='white')
    canvas.pack()

    # 버튼
    brush_slider = Scale(paint_window, from_=1, to=50, orient=HORIZONTAL, label='브러시 크기')
    brush_slider.pack(side=LEFT)
    brush_slider.set(5)

    eraser_on = BooleanVar()
    eraser_button = Checkbutton(paint_window, text="지우개", variable=eraser_on)
    eraser_button.pack(side=LEFT)

    Button(paint_window, text="색 선택", command=choose_color).pack(side=LEFT)
    Button(paint_window, text="텍스트 추가", command=lambda: activate_mode("text")).pack(side=LEFT)
    Button(paint_window, text="도형 (사각형)", command=lambda: activate_mode("rectangle")).pack(side=LEFT)
    Button(paint_window, text="도형 (타원)", command=lambda: activate_mode("oval")).pack(side=LEFT)

    Button(paint_window, text="저장", command=save_file).pack(side=RIGHT)
    Button(paint_window, text="불러오기", command=load_file).pack(side=RIGHT)

    canvas.bind("<B1-Motion>", paint)
    canvas.bind("<Button-1>", lambda event: set_start(event))

# 색상 선택 함수
def choose_color():
    new_color = colorchooser.askcolor(color=color.get())[1]
    if new_color:
        color.set(new_color)

# 모드 활성화
def activate_mode(mode):
    global text_mode, shape_mode, current_shape
    text_mode = mode == "text"
    shape_mode = mode in ["rectangle", "oval"]
    current_shape = mode

# 마우스 시작 좌표 설정
def set_start(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

# 파일 저장 함수
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
    if file_path:
        print(f"저장: {file_path}")

# 파일 불러오기 함수
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[('PNG files', '*.png')])
    if file_path:
        print(f"불러오기: {file_path}")

# 초기화 함수
def initialize():
    global pp

    # Tkinter 창 생성
    pp = Tk()
    pp.title("P.P 시작 화면")
    pp.geometry("800x600")
    pp.configure(bg="lightblue")  # 배경색 설정

    # 시작 버튼
    start_button = Button(pp, text="그림판 시작", command=initialize_paint, bg="white", fg="black", font=("Helvetica", 16))
    start_button.place(x=320, y=250, width=160, height=50)

    # 종료 버튼
    quit_button = Button(pp, text="종료", command=pp.quit, bg="white", fg="black", font=("Helvetica", 16))
    quit_button.place(x=320, y=320, width=160, height=50)

    pp.mainloop()

if __name__ == "__main__":
    initialize()
