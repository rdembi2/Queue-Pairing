from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/assignments')
def index1():
    return render_template('assignments.html')

@app.route('/assignments')
def index1():
    return render_template('assignments.html')

@app.route('/discussion_forum')
def index2():
    return render_template('discussion_forum.html')

@app.route('/grades')
def index2():
    return render_template('grades.html')

@app.route('/syllabus')
def index3():
    return render_template('syllabus.html')

@app.route('/login')
def index4():
    return render_template('login.html')

@app.route('/office_hours')
def index5():
    pair_system()
    return render_template('office_hours.html', posts=posts)

@app.route('/resources')
def index6():
    return render_template('resources.html')


def setArrays():
    # Harcoded data containing list of names of students (list)
    names = ["Rashi Dembi", "Ana Park", "Julia Harvey", "Mary Else","Vander Bilt","JJ","EP"]
    
    # Harcoded data containing all questions (list)
    questions = ["Q1", "Q2", "Q3", "Q4", "Q5","Q6","Q7"]
    
    # Harcoded data containing a question they understand (list)
    questions_understood = ["Q2","Q3","","Q4","Q1","Q5","Q6"]
    
    # Harcoded data containing a question they want help on (list)
    questions_help = ["Q1","Q4","Q5","Q2","Q3","Q1","Q7"]
    
    return names, questions, questions_understood, questions_help

def count_students(names):
    # Update the count of students based on the number of entries to the array
    
    student_count = len(names)
    
    if(student_count % 2 == 1):
        return student_count - 1
    return student_count


def not_paired_index(questions_understood):
    
    """"
        If there is one or more students who have not understood any questions, remove the last
        student to enter the queue who has not understood anything. If not, remove the last student who entered the queue.
        """
    
    index = len(questions_understood) - 1
    for i in questions_understood:
        if(not i):
            #print(i)
            index = questions_understood.index(i)

return index

def matching(q_help, q_understood, names):
    #print(names)
    names_j = names.copy()
    names_k = names.copy()
    pairs = []
    length_arr = int(len(names)/2)
    for i in range(length_arr):
        pairs.append("")
    #print(pairs)
    #print(length_arr)
    #print(q_help)
    #print(q_understood)
    index = 0
    temp_name_j = ""
    temp_name_k = ""
    done_names = []
    # Check for matching questions
    for j in q_help:
        for k in q_understood:
            if(index < len(pairs)):
                if ((j == k) and (j != "") and (k != "")):
                    pairs[index] = ((names_j[q_help.index(j)]) + " - "+ (names_j[q_understood.index(k)]))
                    if((len(names_j[q_help.index(j)])) > 1):
                        done_names.append(names_j[q_help.index(j)])
                        done_names.append(names_j[q_understood.index(k)])
                    names_j[q_help.index(j)] = "0"
                    names_j[q_understood.index(k)] = "0"
                    j = "0"
                    k = "0"
                    if (pairs[index] == "0 - 0"):
                        pairs[index] = None
                    index+=1
    index = 0
    names_j_2 = names.copy()
#print("Done:",done_names )
    
    # Randomly pair the people left to talk through problems with a buddy
    for j in q_help:
        for k in q_understood:
            if(index < len(pairs)):
                if (pairs[index] is not None):
                    #print(str(index) + "Not" )
                    index+=1
                elif(((names_j_2[q_help.index(j)]) not in done_names)
                     and (names_j_2[q_understood.index(k)] not in done_names)):
                    #print(index)
                    pairs[index] = ((names_j_2[q_help.index(j)]) + " - "+ names_j_2[q_understood.index(k)])
                    done_names.append(names_j_2[q_help.index(j)])
                    done_names.append(names_j_2[q_understood.index(k)])
                    names_j_2[q_help.index(j)] = "0"
                    names_j_2[q_understood.index(k)] = "0"
                    j = ""
                    k = ""
                    index+=1
#print("Done 2:", done_names)

    
    
    #print(names_j)
    #print(pairs)
    
    
#print(pairs)
    # Check for same question
    return pairs

def pair_system():
    
    #Set the names, questions, questions_understood, questions_help arrays
    names_arr = setArrays()[0]
    questions_arr = setArrays()[1]
    questions_understood_arr = setArrays()[2]
    questions_help_arr = setArrays()[3]
    
    # Retrieve the original student count
    student_count = len(names_arr)
    
    
    # Find which student should not be paired if odd number of students
    # If number of students is even, to_remove is False
    to_remove = False
    removal_index = student_count
    if (student_count % 2 == 1):
        to_remove = True
        removal_index = not_paired_index(questions_understood_arr)
    #print(removal_index)
    #print(names_arr)
    
    # Store the values before we remove them
    # They should be added to the queue when pair matching happens again ahead of the new people
    name_hold = ''
    questions_hold = ''
    questions_understood_hold = ''
    questions_help_hold = ''
    
    
    if(to_remove):
        name_hold = names_arr[removal_index]
        questions_hold = questions_arr[removal_index]
        questions_understood_hold = questions_understood_arr[removal_index]
        questions_help_hold = questions_help_arr[removal_index]
    
    # Remove values from removal_index when to_remove is true
    if(to_remove):
        names_arr.remove(names_arr[removal_index])
        questions_arr.remove(questions_arr[removal_index])
        questions_understood_arr.remove(questions_understood_arr[removal_index])
        questions_help_arr.remove(questions_help_arr[removal_index])
    #print(questions_understood_arr)
    
    # Create an array to find out if a student has been matched
    # Initialize the values in this array to zero
    matched = names_arr.copy()
    for i in range(len(matched)):
        matched[i] = False
    
    # Create an empty array called range that is the same size as the number of pairs we must return
    #pairs = []
    #     ranger = (len(names_arr))
    
    #     for i in range(int(ranger/2)):
    #         pairs.append("")
    #print(pairs)
    
    # Return the pairs where there is a direct match between a question understood for one students
    # and a question where help is required for another student
    pair = matching(questions_understood_arr, questions_help_arr, names_arr)



if __name__ == "__main__":
    app.run(debug=True)
