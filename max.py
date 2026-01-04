student_scores =[150,142,185,120,171,184,174,149, 24,59,68,199,78,65,89,87]

#max_score = max(student_scores)
#print(max_score)

max_score = student_scores[0]
for num in student_scores:
    if num > max_score:
        max_score = num
       
print(max_score)


min_score = student_scores[0]
for num in student_scores:
    if num < min_score :
        min_score = num
print(min_score)  