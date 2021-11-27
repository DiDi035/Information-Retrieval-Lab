def get_multiple_question_and_answer():
    path_file = './data/MQA.txt'
    question = []
    answer = []
    
    f = open(path_file, 'r') 
    data_list = f.readlines()
    f.close()
    
    for line in data_list:
        data_line = line.strip().split('#')
        question.append(data_line[0])
        answer.append(data_line[1])
    
    return question, answer

question,answer = get_multiple_question_and_answer()
# for i in range(len(question)):
#     print(question[i])
#     print(answer[i])
# print(question)
# print(answer)