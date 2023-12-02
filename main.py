import time
import tkinter as tk
from tkinter import ttk, LEFT

size_of_each_cell = 40
n = 4
root = tk.Tk()
root.geometry('800x500')
root.title("N-Queens")


# Create a frame for the chessboard

def page2(n):
    root.withdraw()
    second_root = tk.Toplevel()
    second_root.geometry('800x500')
    btn_back = tk.Button(second_root, text='back', command=lambda: back_clicking(root, second_root))
    btn_back.pack()
    btn_show = tk.Button(second_root, text='showing queen', command=lambda: showing_queen(chessboard_frame, 3, 3))
    btn_show.pack()
    btn_show = tk.Button(second_root, text='removing queen', command=lambda: remove_queen(chessboard_frame, 3, 3))
    btn_show.pack()
    my_canvas = tk.Canvas(second_root)
    my_canvas.pack(side=LEFT, fill=tk.BOTH, expand=1)

    # scrollbar
    my_scrollbar = tk.Scrollbar(second_root, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind(
        '<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
    )

    # scrollbar
    horizontal_scrollbar = tk.Scrollbar(second_root, orient=tk.HORIZONTAL, command=my_canvas.xview)
    horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, )

    my_canvas.configure(xscrollcommand=horizontal_scrollbar.set)
    my_canvas.bind(
        '<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
    )

    second_frame = tk.Frame(my_canvas, width=1000, height=100)

    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    chessboard_frame = tk.Frame(second_frame)
    chessboard_frame.pack(pady=20, anchor='nw', padx=200)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(chessboard_frame, width=size_of_each_cell, height=size_of_each_cell, bg=color)
            square_frame.grid(row=i, column=j)
    # Create a frame for the chessboard
    second_chessboard_frame = tk.Frame(second_frame)
    second_chessboard_frame.pack(pady=20, anchor='nw', padx=200)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(second_chessboard_frame, width=size_of_each_cell, height=size_of_each_cell,
                                    bg=color)
            square_frame.grid(row=i, column=j)

    third_chessboard_frame = tk.Frame(second_frame)
    third_chessboard_frame.pack(pady=20, anchor='nw', padx=200)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(third_chessboard_frame, width=size_of_each_cell, height=size_of_each_cell,
                                    bg=color)
            square_frame.grid(row=i, column=j)

    fourth_chessboard_frame = tk.Frame(second_frame)
    fourth_chessboard_frame.pack(pady=20, anchor='nw', padx=200)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(fourth_chessboard_frame, width=size_of_each_cell, height=size_of_each_cell,
                                    bg=color)
            square_frame.grid(row=i, column=j)

            back_track = tk.Label(second_frame, text='Back Tracking Algorithm', pady=20)

            back_track.place(rely=0.0, relx=0.0, )

            hill_climb = tk.Label(second_frame, text='Hill Climbing Algorithm', pady=20)

            hill_climb.place(x=0, y=n * 40 + 40)

            best_first = tk.Label(second_frame, text='Best First Search Algorithm', pady=20)

            best_first.place(x=0, y=n * 80 + 80)

            genetic = tk.Label(second_frame, text='Genetic  Algorithm', pady=20)

            genetic.place(x=0, y=n * 120 + 120)
    my_canvas.update_idletasks()

    # second_root.mainloop()
    second_root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, second_root))

    # you should put your algorithm here, after read that notes:
    # when you want to add a queen you can call showing_queen function
    # if you are implementing genetic , so call it like that : showing_queen(fourth_chessboard_frame,x,y)
    # while x and y stands for the position of the queen you want to show on the matrix
    # if you want to delete the queen you entered , you can call remove_queen function
    # if you are implementing backtracking , so call it like that : remove_queen(chessboard_frame,x,y)
    # got the difference yet ?
    # the first element you should pass while implementing the algorithms is :
    # back tracking:chessboard_frame
    # hill climbing:second_chessboard_frame
    # best first searh:third_chessboard_frame
    # genetic:fourth_chessboard_frame

    # backtracking algorithm:

    # hill climbing algorithm:

    # best first search algorithm:

    # genetic algorithm:
    second_root.mainloop()


def page1():
    entry = tk.Entry(root)
    entry.grid(row=0, column=0, padx=10, pady=10)
    submit_button = tk.Button(root, text="Submit", command=lambda: page2(int(entry.get())))
    entry.pack()
    submit_button.pack()


def on_closing(root, second_root):
    second_root.destroy()  # Close the Toplevel window
    root.destroy()


def back_clicking(root, second_root):
    second_root.withdraw()
    root.deiconify()


def showing_queen(chessboard_frame, x, y):
    queen_image = tk.PhotoImage(file='queen.png')  # Replace 'queen.png' with your image file
    queen_image_resized = queen_image.subsample(30, 30)
    queen_label = tk.Label(chessboard_frame, image=queen_image_resized)
    queen_label.image = queen_image_resized  # To prevent image from being garbage-collected
    queen_label.grid(row=x, column=y)  # chessboard_frame.after(1000, lambda: remove_queen(chessboard_frame, x, y))


def remove_queen(chessboard_frame, x, y):
    color = "white" if (x + y) % 2 == 0 else "black"
    square_frame = tk.Frame(chessboard_frame, width=size_of_each_cell, height=size_of_each_cell, bg=color)
    square_frame.grid(row=x, column=y)


page1()
# Create and place the label on the chessboard

# placing
# p1 = tk.Label(second_chessboard_frame, text='X')
# p1.grid(row=0, column=1)  # Adjust the row and column as needed
# # placing tany
# p2 = tk.Label(second_chessboard_frame, text='X')
# p2.grid(row=1, column=1)  # Adjust the row and column as needed


root.mainloop()
