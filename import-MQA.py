def get_multiple_question_and_answer():
    path_file = './data/MQA.txt'
    question = []
    answer = []
    
    f = open(path_file, 'r') 
    data_list = f.readlines()
    
    for line in data_list:
        data_line = line.strip().split('#')
        question.append(data_line[0])
        answer.append(data_line[1])
    
    return question, answer

# question,answer = get_multiple_question_and_answer()
# print(question)
# print(answer)