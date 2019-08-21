import numpy as np  
import re

class Data:

    def __init__(self, filepath):
        
        self.__full_table = np.genfromtxt(filepath, dtype=None, delimiter=",", encoding=None)
    
    
    def get_courses(self):
        return self.__full_table[0][1:]

    def get_students(self):
        return self.__full_table[..., 0][1:]
    
    def get_dirty_sid(self):
        """
        get the indices of error student id.
        return: indices(np.array)
        """
        sid_patt = re.compile('^s\d{7}$')
        sid_match = np.vectorize(lambda x : bool(not sid_patt.match(x)))
        students = self.get_students()
        return np.where(sid_match(students))
        

    def get_dirty_grades(self):
        """
        get the indices of error grade.
        return indices(np.array)
        """
        grade_patt = re.compile('[1-7]{1}$|^$')
        grade_match = np.vectorize(lambda x : bool(not grade_patt.match(x)))
        grades = self.get_all_student2course()[...,1:]
        return np.where(grade_match(grades))

    
    def get_all_student2course(self):
        """
        remove course id and get all student to grades in string.
        """
        return self.__full_table[1:]

    def get_s2c_trainset(self):
        """
            return(np.array): student to course contain student id.
                    shape: (3947, 109)
                    data type: string
        """
        all_s2c = self.get_all_student2course()
        return all_s2c[:int(0.7*len(all_s2c))]

    def get_s2c_testset(self):
        """
        return(np.array): student to course contain student id.
                shape: (1692, 109)
                data type: string
    """
        all_s2c = self.get_all_student2course()
        return all_s2c[int(0.7*len(all_s2c)):]

    def get_all_course2student(self):
        return np.transpose(self.__full_table[..., 1:])
    
    def get_c2s_trainset(self):
        all_c2s = self.get_all_course2student()
        return all_c2s[:int(0.7*len(all_c2s))]

    def get_c2s_testset(self):
        all_c2s = self.get_all_course2student()
        return all_c2s[int(0.7*len(all_c2s)):]
    
    
    def get_int_dataset(self, str_dataset):
        str_grade = str_dataset[...,1:]
        str_grade[str_grade==""] = "0"
        return str_grade.astype(np.int64)

