import tkinter as tk
from PIL import Image
import numpy as np
import cv2
import win32gui
import win32con
import win32ui
from ultralytics import YOLO
import time
import win32api
import threading
import math
# 加载训练好的模型
x1, y1, x2, y2,width,height=[0,0,0,0,0,0]
center=[0,0]
ddx=153#向右变小
#ddy=149#向上变大
ddy=143#usp
model = YOLO(r'D:\drones\runs\detect\train6\weights\best.pt')

def find_window_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    return hwnd

def capture_window(hwnd):
    global width,height
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    # BitBlt to capture the window
    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
    
    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)

    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    # Cleanup
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return img, width, height

def update_image():
    global x1, y1, x2, y2
    hwnd = find_window_by_title(window_title)
    if hwnd:
        captured_image, width, height = capture_window(hwnd)
        
        # Convert PIL image to OpenCV format
        captured_image_cv = cv2.cvtColor(np.array(captured_image), cv2.COLOR_RGB2BGR)
        
        # Use the model to make predictions
        results = model(captured_image_cv)

        max_conf = 0  # Initialize maximum confidence
        best_distance=99999999
        best_box = None  # Initialize best bounding box

        # Parse detection results, find the highest confidence
        if len(results) > 0 and len(results[0].boxes) > 0:
            for result in results:
                boxes = result.boxes
                if len(boxes) > 0:
                    for box in boxes:
                        data = box.data
                        for d in data:
                            conf = d[4].item()
                            if(conf>=0.65):
                                tx1, ty1, tx2, ty2 = int(d[0].item()), int(d[1].item()), int(d[2].item()), int(d[3].item())
                                position=[(tx1+tx2)/2-center[0]-160,(ty1+ty2)/2-center[1]-100]
                                #print('pppp:',position)
                                distance=position[0]**2+position[1]**2
                                if distance < best_distance:  #选出距离最近的box
                                    best_distance = distance
                                    best_box = d
                                    x1,y1,x2,y2=tx1,ty1,tx2,ty2
        else:
                x1=center[0]+2*ddx
                x2=center[0]
                y1=center[1]+2*ddy
                y2=center[1]

        canvas.delete("all")  # Clear previous drawings

        if best_box is not None :  # Only draw bounding boxes with confidence >= 0.7
            #x1, y1, x2, y2 = int(best_box[0].item()), int(best_box[1].item()), int(best_box[2].item()), int(best_box[3].item())
            cls = int(best_box[5].item())
            label_text = f"{model.names[cls]} {max_conf:.2f}"

            # Draw bounding box and label on canvas
            canvas.create_rectangle(x1-165, y1-135, x2-165, y2-135, outline='green', width=2)
            #canvas.create_text(x1-170, y1, text=label_text, fill='green', anchor='nw')
            # Draw a line from the top center of the window to the top center of the rectangle
            line_start_x = width // 2
            line_start_y = 0
            line_end_x = (x1 + x2) // 2-165
            line_end_y = y1-135
            canvas.create_line(line_start_x, line_start_y, line_end_x, line_end_y, fill='red', width=2)
        else:
            x1=center[0]+2*ddx
            x2=center[0]
            y1=center[1]+2*ddy
            y2=center[1]
    
    root.after(15, update_image)  # Update every 0.01 seconds



def is_left_mouse_button_pressed():
    # Get the state of the left mouse button (0x01 for left button)
    return win32api.GetKeyState(0x02) < 0

def is_ctrl_l_pressed():
    # Get the state of the Ctrl key (0x11 for left Ctrl) and L key (0x4C for L key)
    return win32api.GetKeyState(0x11) < 0 and win32api.GetKeyState(0x4C) < 0
clicking = False
def click_mouse():
    global clicking
    while clicking:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        #time.sleep(random.uniform(0.12, 0.125))  # 100ms 间隔
        time.sleep(0.122)  # 大部分枪
        #time.sleep(0.147)  # usp



def check_mouse():
    global clicking
    while True:
        # 检查右键是否按下
        if win32api.GetKeyState(win32con.VK_RBUTTON) < 0:
            if not clicking:
                clicking = True
                # 启动点击线程
                threading.Thread(target=click_mouse).start()
        else:
            clicking = False
        if is_ctrl_l_pressed():
                print("Ctrl + L pressed, exiting program.")
                break
        time.sleep(0.01)  # 防止占用过多 CPU

def move_mouse():
    global x1, y1, x2, y2
    global width,height
    
    try:
        while True:
            print(1)
            if is_left_mouse_button_pressed() :
                print(12322535)
                xy = [(x1+x2)/2, (y1+y2)/2] 
                dx = xy[0] - center[0]-ddx
                dy = xy[1] - center[1]-ddy
                print('dx:',dx,dy)
                distance = math.sqrt(dx**2+dy**2)

                
                if(distance<100):#如果快瞄准了
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx/15), int(dy/15))
                elif(distance<200):
                    direction_x = dx / distance
                    direction_y = dy / distance
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(direction_x*20), int(direction_y*20))
                elif(distance<500):
                    direction_x = dx / distance
                    direction_y = dy / distance
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(direction_x*35), int(direction_y*35))
                else:
                    direction_x = dx / distance
                    direction_y = dy / distance
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(direction_x*50), int(direction_y*50))
            if is_ctrl_l_pressed():
                print("Ctrl + L pressed, exiting program.")
                break
            
            time.sleep(0.02)  # Sleep for 10 milliseconds
    except KeyboardInterrupt:
        print("Program exited.")


if __name__ == "__main__":
    #window_title = "SK助手 2.0.0.9"
    window_title = "腾讯手游助手(64位)"

    # Initialize Tkinter window
    root = tk.Tk()
    
    # Set the window to be transparent and full-size
    hwnd = find_window_by_title(window_title)
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
    else:
        width, height = 800, 600
    center=[width/2,height/2]
    root.geometry(f"{width}x{height}+{left}+{top}")
    root.attributes("-transparentcolor", "white")
    root.attributes("-topmost", True)
    #root.overrideredirect(True)  # Remove window decorations
    root.configure(bg='white')

    # Create a canvas for drawing
    canvas = tk.Canvas(root, width=width, height=height, bg='white', bd=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Start updating the image
    update_image()

    # Run the Tkinter main loop
    mouse_thread = threading.Thread(target=move_mouse)
    mouse_thread.start()   
    mouse_thread1 = threading.Thread(target=check_mouse)
    mouse_thread1.start()   

    root.mainloop()
    
             
