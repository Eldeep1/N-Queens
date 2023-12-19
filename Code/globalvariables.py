import tkinter as tk

size_of_each_cell = 40
root = tk.Tk()
root.geometry('800x500')
root.title("N-Queens")
# global variables needed for drawing genetic algorithm
global genetic_queue
genetic_queue=[]
global temp_individual 
temp_individual = []

# global variables needed for drawing best_first_search algorithm
global temp_individual_best_first
temp_individual_best_first = []
global est_first_list
best_first_list = []

# global variables needed for drawing hill_climb algorithm
global temp_current_list
temp_current_list = []
global hill_climbing_list
hill_climbing_list = []
# global variables needed for drawing back_tracking algorithm
global first_back_track 
first_back_track = True
global should_show 
should_show = []
global x_axis
x_axis = []
global y_axis
y_axis = []



# global variables needed to track if the total number of trials and the succeeded trials
number_of_trials = [0, 0, 0, 0]
number_of_success_trials = [0, 0, 0, 0]
number_of_trials_back_track = tk.StringVar()
number_of_trials_success_back_track = tk.StringVar()

number_of_trials_hill_climb = tk.StringVar()
number_of_trials_success_hill_climb = tk.StringVar()

number_of_trials_best_first = tk.StringVar()
number_of_trials_success_best_first = tk.StringVar()

number_of_trials_genetic = tk.StringVar()
number_of_trials_success_genetic = tk.StringVar()

# variables to track if we found solution or not
solution_found_genetic = tk.StringVar()
solution_found_back_track = tk.StringVar()
solution_found_best_first = tk.StringVar()
solution_found_hill_climb = tk.StringVar()