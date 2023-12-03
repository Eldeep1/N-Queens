import time
import tkinter as tk
from tkinter import ttk, LEFT
import numpy as np
import queue
import threading

from random import randint

n = 4
size_of_each_cell = 40
root = tk.Tk()
root.geometry('800x500')
root.title("N-Queens")
iteration_number=0
genetic_queue = []
temp_individual = []


# Create a frame for the chessboard
def start_processing(x):
    thread = threading.Thread(target=x)
    thread.start()


def page2(n):
    # Create and pack four buttons in the same row

    root.withdraw()
    print(n)
    second_root = tk.Toplevel()
    second_root.geometry('800x500')

    #
    # button2 = tk.Button(second_root, text="show hill climbing", command=lambda: button_clicked(2))
    # button2.pack(anchor=tk.NW, side=tk.LEFT, padx=0)
    #
    # button3 = tk.Button(second_root, text="show best first search", command=lambda: button_clicked(3))
    # button3.pack(anchor=tk.NW, side=tk.LEFT, padx=0)
    #
    # button4 = tk.Button(second_root, text="show genetic", command=lambda: button_clicked(4))
    # button4.pack(anchor=tk.NW, side=tk.LEFT, padx=0)

    btn_back = tk.Button(second_root, text='back', command=lambda: back_clicking(root, second_root))
    btn_back.pack()

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
    def init_pop(pop_size, board_size):
        return np.random.randint(board_size, size=(pop_size, board_size))

    def calc_fitness(population, board_size):
        fitness_vals = []
        for x in population:
            penalty = 0
            for i in range(board_size):
                r = x[i]
                for j in range(board_size):
                    if i == j:
                        continue
                    d = abs(i - j)
                    if x[j] in [r, r - d, r + d]:
                        penalty += 1
            fitness_vals.append(penalty)
        return -1 * np.array(fitness_vals)

    def selection(population, fitness_vals):
        probs = fitness_vals.copy()
        probs += abs(probs.min()) + 1
        probs = probs / probs.sum()
        N = len(population)
        indices = np.arange(N)
        selected_indices = np.random.choice(indices, size=N, p=probs)
        selected_population = population[selected_indices]
        return selected_population

    def crossover(board_size, parent1, parent2, pc):
        r = np.random.random()
        if r < pc:
            m = np.random.randint(1, board_size)
            child1 = np.concatenate([parent1[:m], parent2[m:]])
            child2 = np.concatenate([parent2[:m], parent1[m:]])
        else:
            child1 = parent1.copy()
            child2 = parent2.copy()
        return child1, child2

    def mutation(board_size, individual, pm):
        r = np.random.random()
        if r < pm:
            m = np.random.randint(board_size)
            individual[m] = np.random.randint(board_size)
        return individual

    def crossover_mutation(board_size, selected_pop, pc, pm):
        N = len(selected_pop)
        new_pop = np.empty((N, board_size), dtype=int)
        for i in range(0, N, 2):
            parent1 = selected_pop[i]
            parent2 = selected_pop[i + 1]
            child1, child2 = crossover(board_size, parent1, parent2, pc)
            new_pop[i] = child1
            new_pop[i + 1] = child2
        for i in range(N):
            mutation(board_size, new_pop[i], pm)
        return new_pop

    def print_board(queue_index=0):
        if queue_index < len(genetic_queue):
            individual = genetic_queue[queue_index]
            print(individual)
            global temp_individual

            if len(temp_individual):
                if not np.array_equal(individual, temp_individual):
                    for i in range(n):
                        remove_queen(fourth_chessboard_frame, i, temp_individual[i])
                        showing_queen(fourth_chessboard_frame, i, individual[i])
            else:
                for i in range(n):
                    showing_queen(fourth_chessboard_frame, i, individual[i])

            temp_individual = individual
            root.after(1000, print_board,
                       queue_index + 1)  # Schedule the next update after 1000 milliseconds (1 second)

    def n_queen_genetic(board_size, pop_size, max_generations, pc=0.7, pm=0.01):
        genetic_queue.clear()
        global temp_individual
        if len(temp_individual):
            for i in range(len(temp_individual)):
                remove_queen(fourth_chessboard_frame, i, temp_individual[i])
        temp_individual=[]
        population = init_pop(pop_size, board_size)
        best_fitness_overall = None
        for generation in range(max_generations):
            fitness_vals = calc_fitness(population, board_size)
            best_i = fitness_vals.argmax()
            best_fitness = fitness_vals[best_i]

            if best_fitness_overall is None or best_fitness > best_fitness_overall:
                best_fitness_overall = best_fitness
                best_solution = population[best_i]
                print("we've just appended",best_solution)

                genetic_queue.append(best_solution)

                print('the best solution is above')

            print(f'\rgen={generation + 1:05} -Fitness={-best_fitness:02}', end='')
            if best_fitness == 0:

                # print_board(best_solution)

                # print('the best solution is above')
                break

            # genetic_queue.append(best_solution)
            # print(best_solution)
            selected_pop = selection(population, fitness_vals)
            population = crossover_mutation(board_size, selected_pop, pc, pm)
        print_board()

    # n_queen_genetic(n, pop_size=100, max_generations=10000, pc=0.7, pm=0.05)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(fourth_chessboard_frame, width=size_of_each_cell, height=size_of_each_cell,
                                    bg=color)
            square_frame.grid(row=i, column=j)

            back_track = tk.Button(second_frame, text='Show Back Tracking Algorithm', pady=20)

            back_track.place(rely=0.0, relx=0.0, )

            hill_climb = tk.Button(second_frame, text='Show Hill Climbing Algorithm', pady=20)

            hill_climb.place(x=0, y=n * 40 + 40)

            best_first = tk.Button(second_frame, text='Show Best First Search Algorithm', pady=20)

            best_first.place(x=0, y=n * 80 + 80)

            genetic = tk.Button(second_frame, text='Show Genetic  Algorithm', pady=20, command=lambda: start_processing(
                n_queen_genetic(n, pop_size=100, max_generations=10000, pc=0.7, pm=0.05)))

            genetic.place(x=0, y=n * 120 + 120)
    my_canvas.update_idletasks()
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
