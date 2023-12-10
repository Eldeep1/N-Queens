import tkinter as tk
from tkinter import ttk, LEFT
import numpy as np
import threading
import Genetic_Algo as GA
import random
from queue import PriorityQueue
import copy
import random
import timeit

n = 4
size_of_each_cell = 40
root = tk.Tk()
root.geometry('800x500')
root.title("N-Queens")
iteration_number = 0
genetic_queue = []
temp_individual = []
temp_individual_best_first = []
temp_current_list = []
hill_climbing_list = []
best_first_list=[]
first_back_track=True
should_show=[]
x_axis=[]
y_axis=[]
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
    def print_solution(queue_index=0,):
        global first_back_track
        if not first_back_track:
            for i in range(n):
                for j in range(n):
                    remove_queen(chessboard_frame, i, j)
        if queue_index<len(x_axis):
            if should_show[queue_index]:
                showing_queen(chessboard_frame, x_axis[queue_index], y_axis[queue_index])
            else:
                remove_queen(chessboard_frame, x_axis[queue_index], y_axis[queue_index])

            root.after(1000, print_solution,
                           queue_index + 1)  # Schedule the next update after 1000 milliseconds (1 second)

    def isSafe(board, row, col):
        for i in range(row):
            if board[i][col] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, N)):
            if board[i][j] == 1:
                return False

        return True

    def solver(board, row, first):

        global should_show
        global x_axis
        global y_axis

        if row >= N:
            return True

        if row == 0:
            if first:
                while True:
                    first = False
                    random_col = random.randint(0, N - 1)
                    if board[row][random_col] == 0:
                        board[row][random_col] = 1
                        print("Queen placed at row {}, column {}".format(row, random_col))
                        should_show.append(True)
                        x_axis.append(row)
                        y_axis.append(random_col)
                        if solver(board, row + 1, first):
                            return True
                        board[row][random_col] = 0
                        print("Queen removed from row {}, column {}".format(row, random_col))
                        should_show.append(False)
                        x_axis.append(row)
                        y_axis.append(random_col)
                        break
            if not first:
                while True:
                    first = False
                    random_col = (random_col + 1) % N
                    if board[row][random_col] == 0:
                        board[row][random_col] = 1
                        print("Queen placed at row {}, column {}".format(row, random_col))
                        should_show.append(True)
                        x_axis.append(row)
                        y_axis.append(random_col)
                        if solver(board, row + 1, first):
                            return True
                        board[row][random_col] = 0
                        print("Queen removed from row {}, column {}".format(row, random_col))
                        should_show.append(False)
                        x_axis.append(row)
                        y_axis.append(random_col)
                        break

        for col in range(N):
            if isSafe(board, row, col):
                board[row][col] = 1
                print("Queen placed at row {}, column {}".format(row, col))
                should_show.append(True)
                x_axis.append(row)
                y_axis.append(col)
                if solver(board, row + 1, False):
                    return True
                board[row][col] = 0
                print("Queen removed from row {}, column {}".format(row, col))
                should_show.append(False)
                x_axis.append(row)
                y_axis.append(col)
        return False

    def solveNQ():
        global N
        print('----------')
        print(len(should_show))
        if len(should_show) :
            for i in range(len(should_show)):
                remove_queen(chessboard_frame, x_axis[i], y_axis[i])
                print(i)
                print(should_show[i])
        should_show.clear()
        x_axis.clear()
        y_axis.clear()

        print(len(should_show))
        print('ssssssssssssss')
        N = n
        board = []
        first = True

        while True:
            for i in range(N):
                row = [0 for j in range(N)]
                board.append(row)

            if solver(board, 0, first):
                print("Solution found:")
                # printSolution(board)
                print('this is x axis')
                for i in range(len(x_axis)):
                    print(x_axis[i])
                print('this is y axis')
                for i in range(len(y_axis)):
                    print(y_axis[i])

                print_solution()

                return True
            else:
                board = []
                print("No solution exists")
                print_solution(should_show, x_axis, y_axis)

                return True

    # hill climbing algorithm:
    def print_hill_climbing(queue_index=0):
        if queue_index < len(hill_climbing_list):
            current_list = hill_climbing_list[queue_index]
            print(current_list)
            global temp_current_list

            if len(temp_current_list):
                if not np.array_equal(current_list, temp_current_list):
                    for i in range(n):
                        remove_queen(second_chessboard_frame, i, temp_current_list[i])
                        showing_queen(second_chessboard_frame, i, current_list[i])
            else:
                for i in range(n):
                    showing_queen(second_chessboard_frame, i, current_list[i])

            temp_current_list = current_list
            root.after(1000, print_hill_climbing,
                       queue_index + 1)  # Schedule the next update after 1000 milliseconds (1 second)

    def calculate_attacks(board, n):
        attacks = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    attacks += 1
        return attacks

    def hill_climbing(n):
        hill_climbing_list.clear()
        global temp_current_list
        if len(temp_current_list):
            for i in range(len(temp_current_list)):
                remove_queen(second_chessboard_frame, i, temp_current_list[i])
        temp_current_list = []
        current_solution = [random.randint(0, n - 1) for _ in range(n)]
        current_attacks = calculate_attacks(current_solution, n)
        counter = 0
        i = 0
        while current_attacks > 0 and i < n:
            j = 0
            while j < n:
                row_to_change = i
                value_to_change = j
                next_solution = current_solution.copy()
                next_solution[row_to_change] = value_to_change

                next_attacks = calculate_attacks(next_solution, n)

                if next_attacks < current_attacks:
                    hill_climbing_list.append(next_solution)
                    current_solution = next_solution
                    current_attacks = next_attacks
                counter += 1
                j += 1
            i += 1

        print("number of attacks: ", current_attacks)
        print("counter: ", counter)
        print_hill_climbing()

        return current_solution

    # best first search algorithm:
    class Node:
        def __init__(self, state, heuristic):
            self.state = state
            self.cost = heuristic

        def __lt__(self, other):
            if isinstance(other, Node):
                return self.cost < other.cost
            return NotImplemented

    def get_successor_states(state):  # return all children of initial state(node)
        n = len(state)
        children = []
        for i in range(n):
            if state[i] == 0:
                copy_state = copy.deepcopy(state)
                copy_state[i] = 1
                children.append(copy_state)
            elif state[i] == n - 1:
                copy_state = copy.deepcopy(state)
                copy_state[i] = n - 2
                children.append(copy_state)
            else:
                copy_state1 = copy.deepcopy(state)
                copy_state2 = copy.deepcopy(state)
                copy_state1[i] += 1
                copy_state2[i] -= 1
                children.append(copy_state1)
                children.append(copy_state2)
        return children

    def heuristic_function(state):
        # Simple heuristic: counts conflicts in the same row, column, and diagonals.
        conflicts = 0
        n = len(state)
        for i in range(n):
            for j in range(i + 1, n):
                # if list=(item1,item2,item3,item4) and item1 = item2 then they are in the same column
                # for each item in list compare it with the all next items for example item1 with item2,item3,item4
                # and when i=1 compare item2 with item3,item4 and so on
                # and if they satisfay these conditions increase the conflict by one
                if state[i] == state[j] or \
                        state[i] - i == state[j] - j or \
                        state[i] + i == state[j] + j:
                    conflicts += 1
        return conflicts

    def best_first_search(initial_state, heuristic_function):  # heursitic here is the num of attacks
        priority_queue = PriorityQueue()
        visited = []  # to put the visited state to this list
        best_first_list.clear()
        global temp_individual_best_first
        if len(temp_individual_best_first):
            for i in range(len(temp_individual_best_first)):
                remove_queen(third_chessboard_frame, i, temp_individual_best_first[i])
        temp_individual_best_first = []
        initial_node = Node(initial_state, heuristic_function(initial_state))
        priority_queue.put((heuristic_function(initial_state), initial_node))  # (heuristic,state)
        while not priority_queue.empty():
            _, current_node = priority_queue.get()  # _, means i don't need the priority get the state which have minimum heuristic
            if heuristic_function(current_node.state) == 0:  # goal state here is the node.heuristic ==0
                best_first_list.append(current_node.state)
                print(current_node.state)
                print(len(best_first_list))
                return current_node.state  # Goal reached

            visited.append(current_node.state)
            childs = get_successor_states(current_node.state)  # get the childs of initial state
            for child in childs:
                if child not in visited:  # check each child of initial state
                    successor_node = Node(child, heuristic_function(child))
                    if len(best_first_list) > 0 :
                        if current_node.state != best_first_list[-1]:
                        # Your code here
                            best_first_list.append(current_node.state)
                            print(current_node.state)
                    else :
                        best_first_list.append(current_node.state)

                    print(successor_node.state)
                    print(len(best_first_list))

                    priority_queue.put(
                        (successor_node.cost, successor_node))  # add childs to the priority queue as nodes
        print('--------------')
        # print(priority_queue)
        return None  # No solution found

    def plot_queens_board(queue_index=0):
        if queue_index < len(best_first_list):
            individual = best_first_list[queue_index]
            print(individual)
            global temp_individual_best_first

            if len(temp_individual_best_first):
                if not np.array_equal(individual, temp_individual_best_first):
                    for i in range(n):
                        remove_queen(third_chessboard_frame, i, temp_individual_best_first[i])
                        showing_queen(third_chessboard_frame, i, individual[i])
            else:
                for i in range(n):
                    showing_queen(third_chessboard_frame, i, individual[i])

            temp_individual_best_first = individual
            root.after(1000, plot_queens_board,
                       queue_index + 1)  # Schedule the next update after 1000 milliseconds (1 second)

    def make_random_itial_state(n):  # Shffling the inithial places of queens
        initial_state = list(range(0, n))
        random.shuffle(initial_state)
        return initial_state

    def get_solution_and_drow(n):
        initial_state = make_random_itial_state(n)
        solution = best_first_search(initial_state, heuristic_function)
        if solution:
            print("Solution found :", solution)
            plot_queens_board()
        else:
            print("No solution found.")  # never achieve with best first algorithm

    # genetic algorithm:

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
        temp_individual = []
        population = GA.init_pop(pop_size, board_size)
        best_fitness_overall = None
        for generation in range(max_generations):
            fitness_vals = GA.calc_fitness(population, board_size)
            best_i = fitness_vals.argmax()
            best_fitness = fitness_vals[best_i]

            if best_fitness_overall is None or best_fitness > best_fitness_overall:
                best_fitness_overall = best_fitness
                best_solution = population[best_i]
                print("we've just appended", best_solution)

                genetic_queue.append(best_solution)

                print('the best solution is above')

            print(f'\rgen={generation + 1:05} -Fitness={-best_fitness:02}', end='')
            if best_fitness == 0:
                # print_board(best_solution)

                # print('the best solution is above')
                break

            # genetic_queue.append(best_solution)
            # print(best_solution)
            selected_pop = GA.selection(population, fitness_vals)
            population = GA.crossover_mutation(board_size, selected_pop, pc, pm)
        print_board()

    # n_queen_genetic(n, pop_size=100, max_generations=10000, pc=0.7, pm=0.05)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(fourth_chessboard_frame, width=size_of_each_cell, height=size_of_each_cell,
                                    bg=color)
            square_frame.grid(row=i, column=j)

            back_track = tk.Button(second_frame, text='Show Back Tracking Algorithm', pady=20,
                                   command=lambda: solveNQ())

            back_track.place(rely=0.0, relx=0.0, )

            hill_climb = tk.Button(second_frame, text='Show Hill Climbing Algorithm', pady=20,
                                   command=lambda: hill_climbing(n))

            hill_climb.place(x=0, y=n * 40 + 40)

            best_first = tk.Button(second_frame, text='Show Best First Search Algorithm', pady=20,command=lambda :get_solution_and_drow(n))

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
