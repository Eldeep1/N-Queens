# import needed libraries
import tkinter as tk
from tkinter import LEFT
import numpy as np
from tkinter import messagebox
from queue import PriorityQueue
import random
import globalvariables as GV
import Bestfirst as BF
import GeneticAlgorithm as GA
# from now on , we will start building the gui and the ALGORITHMS !
def page2(n):
    # closing the first page when entering the second one
    GV.root.withdraw()
    second_root = tk.Toplevel()
    second_root.geometry('800x500')
    # creating the back button so the user can enter a different size of the board again
    btn_back = tk.Button(second_root, text='back', command=lambda: back_clicking(GV.root, second_root))
    btn_back.pack()
    # creating two scroll bars ( horizontal and vertical ) so the user can navigate on the screen when the board size is huge
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

    # setting up the four chessboards !

    chessboard_frame = tk.Frame(second_frame)
    chessboard_frame.pack(pady=20, anchor='nw', padx=200)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(chessboard_frame, width=GV.size_of_each_cell, height=GV.size_of_each_cell, bg=color)
            square_frame.grid(row=i, column=j)
    # Create a frame for the chessboard
    second_chessboard_frame = tk.Frame(second_frame)
    second_chessboard_frame.pack(pady=20, anchor='nw', padx=200)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(second_chessboard_frame, width=GV.size_of_each_cell, height=GV.size_of_each_cell,
                                    bg=color)
            square_frame.grid(row=i, column=j)

    third_chessboard_frame = tk.Frame(second_frame)
    third_chessboard_frame.pack(pady=20, anchor='nw', padx=200)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(third_chessboard_frame, width=GV.size_of_each_cell, height=GV.size_of_each_cell,
                                    bg=color)
            square_frame.grid(row=i, column=j)

    fourth_chessboard_frame = tk.Frame(second_frame)
    fourth_chessboard_frame.pack(pady=20, anchor='nw', padx=200)

    # second_root.mainloop()
    second_root.protocol("WM_DELETE_WINDOW", lambda: on_closing(GV.root, second_root))

    # ALGORITHMS TIME  !!!!

    # backtracking algorithm:
    def print_solution(queue_index=0, ):
    
        if not GV.first_back_track:
            for i in range(n):
                for j in range(n):
                    remove_queen(chessboard_frame, i, j)
        if queue_index < len(GV.x_axis):
            if GV.should_show[queue_index]:
                showing_queen(chessboard_frame, GV.x_axis[queue_index], GV.y_axis[queue_index])
            else:
                remove_queen(chessboard_frame, GV.x_axis[queue_index], GV.y_axis[queue_index])

            GV.root.after(1000, print_solution,
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

    def solver(board, row, col, first, lim):
        flag = False

        if row >= N:
            return True

        if row == 0:
            if first:
                first = False
                board[row][col] = 1
                print("Queen placed at row {}, column {}".format(row, col))
                GV.number_of_trials[0] = GV.number_of_trials[0] + 1
                GV.should_show.append(True)
                GV.x_axis.append(row)
                GV.y_axis.append(col)
                if solver(board, row + 1, col, first, lim):
                    return True
                board[row][col] = 0
                print("Queen removed from row {}, column {}".format(row, col))
                GV.number_of_trials[0] = GV.number_of_trials[0] + 1

                GV.should_show.append(False)
                GV.x_axis.append(row)
                GV.y_axis.append(col)

            if not first:
                col = (col + 1) % N
                lim += 1

                board[row][col] = 1
                print("Queen placed at row {}, column {}".format(row, col))
                GV.number_of_trials[0] = GV.number_of_trials[0] + 1

                GV.should_show.append(True)
                GV.x_axis.append(row)
                GV.y_axis.append(col)
                if solver(board, row + 1, col, first, lim):
                    return True
                board[row][col] = 0
                print("Queen removed from row {}, column {}".format(row, col))
                GV.number_of_trials[0] = GV.number_of_trials[0] + 1

                GV.should_show.append(False)
                GV.x_axis.append(row)
                GV.y_axis.append(col)
                flag = True

        if lim == N - 1:
            return False
        if flag:
            solver(board, row, col, first, lim)
            return True

        if N > row > 0:
            for i in range(N):
                if isSafe(board, row, i):
                    board[row][i] = 1
                    print("Queen placed at row {}, column {}".format(row, i))
                    GV.number_of_trials[0] = GV.number_of_trials[0] + 1

                    GV.should_show.append(True)
                    GV.x_axis.append(row)
                    GV.y_axis.append(i)
                    if solver(board, row + 1, i, False, lim):
                        return True
                    board[row][i] = 0
                    print("Queen removed from row {}, column {}".format(row, i))
                    GV.number_of_trials[0] = GV.number_of_trials[0] + 1

                    GV.should_show.append(False)
                    GV.x_axis.append(row)
                    GV.y_axis.append(i)

        return False

    def solveNQ():
        GV.number_of_trials_success_back_track.set(n)
        GV.number_of_trials[0] = 0
        global N
        N = n
        if len(GV.should_show):
            for i in range(len(GV.should_show)):
                remove_queen(chessboard_frame, GV.x_axis[i], GV.y_axis[i])
                print(i)
                print(GV.should_show[i])
        GV.should_show.clear()
        GV.x_axis.clear()
        GV.y_axis.clear()

        board = []
        first = True
        col = random.randint(0, N - 1)
        lim = 0
        for i in range(N):
            row = [0 for j in range(N)]
            board.append(row)

        if solver(board, 0, col, first, lim):
            print("Solution found:")
            print_solution()
            GV.number_of_trials_back_track.set(GV.number_of_trials[0])
            GV.solution_found_back_track.set('no solution found !')
            GV.number_of_trials_success_back_track.set(0)
            return True
        else:
            board = []
            print("No solution exists")
            GV.solution_found_back_track.set('solution found !')

            return True

    # hill climbing algorithm:
    def print_hill_climbing(queue_index=0):
        if queue_index < len(GV.hill_climbing_list):
            current_list = GV.hill_climbing_list[queue_index]
            print(current_list)

            if len(GV.temp_current_list):
                if not np.array_equal(current_list, GV.temp_current_list):
                    for i in range(n):
                        remove_queen(second_chessboard_frame, i, GV.temp_current_list[i])
                        showing_queen(second_chessboard_frame, i, current_list[i])
            else:
                for i in range(n):
                    showing_queen(second_chessboard_frame, i, current_list[i])

            GV.temp_current_list = current_list
            GV.root.after(1000, print_hill_climbing,
                       queue_index + 1)  # Schedule the next update after 1000 milliseconds (1 second)

    def calculate_attacks(board, n):
        attacks = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    attacks += 1
        return attacks

    def hill_climbing(n):
        GV.number_of_success_trials[1] = 0
        GV.hill_climbing_list.clear()
        if len(GV.temp_current_list):
            for i in range(len(GV.temp_current_list)):
                remove_queen(second_chessboard_frame, i, GV.temp_current_list[i])
        GV.temp_current_list = []
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
                    GV.hill_climbing_list.append(next_solution)
                    GV.number_of_success_trials[1] = GV.number_of_success_trials[1] + 1
                    current_solution = next_solution
                    current_attacks = next_attacks
                counter += 1
                j += 1
            i += 1

        print("number of attacks: ", current_attacks)
        if (current_attacks == 0):
            GV.solution_found_hill_climb.set('solution found !')
        else:
            GV.solution_found_hill_climb.set('no solution found !')
        print("counter: ", counter)
        print_hill_climbing()
        GV.number_of_trials[1] = counter
        GV.number_of_trials_hill_climb.set(GV.number_of_trials[1])
        GV.number_of_trials_success_hill_climb.set(GV.number_of_success_trials[1])
        return current_solution

    # best first search algorithm:
    def best_first_search(initial_state, heuristic_function):  # heursitic here is the num of attacks
        priority_queue = PriorityQueue()
        visited = []  # to put the visited state to this list
        GV.number_of_trials[2] = 0
        GV.best_first_list.clear()
        if len(GV.temp_individual_best_first):
            for i in range(len(GV.temp_individual_best_first)):
                remove_queen(third_chessboard_frame, i, GV.temp_individual_best_first[i])
        GV.temp_individual_best_first = []
        initial_node = BF.Node(initial_state, heuristic_function(initial_state))
        priority_queue.put((heuristic_function(initial_state), initial_node))  # (heuristic,state)
        while not priority_queue.empty():
            # number_of_trials[2]=number_of_trials[2]+1

            _, current_node = priority_queue.get()  # _, means i don't need the priority get the state which have minimum heuristic
            if heuristic_function(current_node.state) == 0:  # goal state here is the node.heuristic ==0
                GV.best_first_list.append(current_node.state)
                print(current_node.state)
                print(len(GV.best_first_list))
                return current_node.state  # Goal reached
            visited.append(current_node.state)
            childs = BF.get_successor_states(current_node.state)  # get the childs of initial state
            for child in childs:
                if child not in visited:  # check each child of initial state
                    successor_node = BF.Node(child, heuristic_function(child))
                    if len(GV.best_first_list) > 0:
                        if current_node.state != GV.best_first_list[-1]:
                            # Your code here
                            GV.best_first_list.append(current_node.state)
                            print(current_node.state)
                    else:
                        GV.best_first_list.append(current_node.state)

                    print(successor_node.state)
                    print(len(GV.best_first_list))
                    GV.number_of_trials[2] = GV.number_of_trials[2] + 1

                    priority_queue.put(
                        (successor_node.cost, successor_node))  # add childs to the priority queue as nodes
        print('--------------')
        print(priority_queue)
        print(len(GV.best_first_list))
        return None  # No solution found

    def plot_queens_board(queue_index=0):
        if queue_index < len(GV.best_first_list):
            individual = GV.best_first_list[queue_index]
            print(individual)

            if len(GV.temp_individual_best_first):
                if not np.array_equal(individual, GV.temp_individual_best_first):
                    for i in range(n):
                        remove_queen(third_chessboard_frame, i, GV.temp_individual_best_first[i])
                        showing_queen(third_chessboard_frame, i, individual[i])
            else:
                for i in range(n):
                    showing_queen(third_chessboard_frame, i, individual[i])

            GV.temp_individual_best_first = individual
            GV.root.after(1000, plot_queens_board,
                       queue_index + 1)  # Schedule the next update after 1000 milliseconds (1 second)

    def get_solution_and_drow(n):
        initial_state = BF.make_random_itial_state(n)
        solution = best_first_search(initial_state, BF.heuristic_function)
        if solution:
            GV.solution_found_best_first.set('solution found !')

            print("Solution found :", solution)
            plot_queens_board()
            GV.number_of_trials_success_best_first.set(len(GV.best_first_list))
        else:
            GV.solution_found_best_first.set('no solution found !')

            print("No solution found.")  # never achieve with best first algorithm
        GV.number_of_trials_best_first.set(GV.number_of_trials[2])

    # genetic algorithm:

    def print_board(queue_index=0):
        if queue_index < len(GV.genetic_queue):
            individual = GV.genetic_queue[queue_index]
            print(individual)

            if len(GV.temp_individual):
                if not np.array_equal(individual, GV.temp_individual):
                    for i in range(n):
                        remove_queen(fourth_chessboard_frame, i, GV.temp_individual[i])
                        showing_queen(fourth_chessboard_frame, i, individual[i])
            else:
                for i in range(n):
                    showing_queen(fourth_chessboard_frame, i, individual[i])

            GV.temp_individual = individual
            GV.root.after(1000, print_board,
                       queue_index + 1)  # Schedule the next update after 1000 milliseconds (1 second)

    def n_queen_genetic(board_size, pop_size, max_generations, pc=0.7, pm=0.01):
        GV.number_of_success_trials[3] = 0
        GV.genetic_queue.clear()
        if len(GV.temp_individual):
            for i in range(len(GV.temp_individual)):
                remove_queen(fourth_chessboard_frame, i, GV.temp_individual[i])
        GV.temp_individual = []
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
                GV.number_of_success_trials[3] = GV.number_of_success_trials[3] + 1
                GV.genetic_queue.append(best_solution)

                print('the best solution is above')

            print(f'\rgen={generation + 1:05} -Fitness={-best_fitness:02}', end='')
            if best_fitness == 0:
                GV.solution_found_genetic.set('solution found !')
                break

            # genetic_queue.append(best_solution)
            # print(best_solution)
            selected_pop = GA.selection(population, fitness_vals)
            population = GA.crossover_mutation(board_size, selected_pop, pc, pm)
            if generation + 1 == max_generations:
                GV.solution_found_genetic.set('no solution found !')
                break

        GV.number_of_trials_success_genetic.set(GV.number_of_success_trials[3])
        GV.number_of_trials_genetic.set(generation + 1)
        print_board()

    # n_queen_genetic(n, pop_size=100, max_generations=10000, pc=0.7, pm=0.05)

    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "black"
            square_frame = tk.Frame(fourth_chessboard_frame, width=GV.size_of_each_cell, height=GV.size_of_each_cell,
                                    bg=color)
            square_frame.grid(row=i, column=j)

            # placing back track button and labels
            back_track = tk.Button(second_frame, text='Show Back Tracking Algorithm', pady=20,
                                   command=lambda: solveNQ())

            back_track_total = tk.Label(second_frame, text='number of trials : ')
            back_track_total2 = tk.Label(second_frame, textvariable=GV.number_of_trials_back_track)
            back_track_success_total = tk.Label(second_frame, text='number of success trials : ')
            back_track_success_total2 = tk.Label(second_frame, textvariable=GV.number_of_trials_success_back_track)
            back_track_solution = tk.Label(second_frame, textvariable=GV.solution_found_back_track)

            back_track.place(rely=0.0, relx=0.0, )
            back_track_total.place(rely=0.1, relx=0.0)
            back_track_total2.place(rely=0.1, x=90)
            back_track_success_total.place(rely=0.13, relx=0.0)
            back_track_success_total2.place(rely=0.13, x=155)
            back_track_solution.place(rely=.16, x=0)

            # placing hill climb button and labels
            hill_climb = tk.Button(second_frame, text='Show Hill Climbing Algorithm', pady=20,
                                   command=lambda: hill_climbing(n))

            hill_climb.place(x=0, y=n * 40 + 40)
            hill_climb_total = tk.Label(second_frame, text='number of trials : ')
            hill_climb_total2 = tk.Label(second_frame, textvariable=GV.number_of_trials_hill_climb)
            hill_climb_success_total = tk.Label(second_frame, text='number of success trials : ')
            hill_climb_success_total2 = tk.Label(second_frame, textvariable=GV.number_of_trials_success_hill_climb)
            hill_climb_solution = tk.Label(second_frame, textvariable=GV.solution_found_hill_climb)

            hill_climb_total.place(x=0, y=n * 40 + 120)
            hill_climb_total2.place(x=90, y=n * 40 + 120)
            hill_climb_success_total.place(x=0, y=n * 40 + 140)
            hill_climb_success_total2.place(x=140, y=n * 40 + 140)
            hill_climb_solution.place(x=0, y=n * 40 + 160)

            # placing best first searches button and labels
            best_first = tk.Button(second_frame, text='Show Best First Search Algorithm', pady=20,
                                   command=lambda: get_solution_and_drow(n))

            best_first.place(x=0, y=n * 80 + 80)

            best_first_total = tk.Label(second_frame, text='number of trials : ')
            best_first_total2 = tk.Label(second_frame, textvariable=GV.number_of_trials_best_first)
            best_first_success_total = tk.Label(second_frame, text='number of success trials : ')
            best_first_success_total2 = tk.Label(second_frame, textvariable=GV.number_of_trials_success_best_first)
            best_first_solution = tk.Label(second_frame, textvariable=GV.solution_found_best_first)

            best_first_total.place(x=0, y=n * 80 + 160)
            best_first_total2.place(x=90, y=n * 80 + 160)
            best_first_success_total.place(x=0, y=n * 80 + 180)
            best_first_success_total2.place(x=140, y=n * 80 + 180)
            best_first_solution.place(x=0, y=n * 80 + 200)

            # placing genetic button and labels
            genetic = tk.Button(second_frame, text='Show Genetic  Algorithm', pady=20, command=lambda:
            n_queen_genetic(n, pop_size=100, max_generations=10000, pc=0.7, pm=0.05))

            genetic.place(x=0, y=n * 120 + 120)

            genetic_total = tk.Label(second_frame, text='number of trials : ')
            genetic_total2 = tk.Label(second_frame, textvariable=GV.number_of_trials_genetic)
            genetic_success_total = tk.Label(second_frame, text='number of success trials : ')
            genetic_success_total2 = tk.Label(second_frame, textvariable=GV.number_of_trials_success_genetic)
            genetic_solution = tk.Label(second_frame, textvariable=GV.solution_found_genetic)

            genetic_total.place(x=0, y=n * 120 + 200)
            genetic_total2.place(x=90, y=n * 120 + 200)
            genetic_success_total.place(x=0, y=n * 120 + 220)
            genetic_success_total2.place(x=140, y=n * 120 + 220)
            genetic_solution.place(x=0, y=n * 120 + 240)
    my_canvas.update_idletasks()
    second_root.mainloop()


def page1():
    def submit_handler():
        try:
            n = int(entry.get())
            if n > 0:
                page2(n)
            else:
                # Show a message if n is not a positive integer
                messagebox.showinfo("Invalid Input", "Please enter a positive integer.")
        except ValueError:
            # Show a message if the input is not a valid integer
            messagebox.showinfo("Invalid Input", "Please enter a valid integer.")

    entry = tk.Entry(GV.root)
    entry.grid(row=0, column=0, padx=10, pady=10)
    submit_button = tk.Button(GV.root, text="Submit", command=submit_handler)
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
    square_frame = tk.Frame(chessboard_frame, width=GV.size_of_each_cell, height=GV.size_of_each_cell, bg=color)
    square_frame.grid(row=x, column=y)


page1()

GV.root.mainloop()
