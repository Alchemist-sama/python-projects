def format_names(f_name,l_name):
   formated_fname = f_name.title()
   l_name = l_name.title()
   return f"{formated_fname}{l_name}"  

print(format_names(f_name="eugene", l_name="samuel"))