
from Data import Data
import pickle

def course_code_name(filepath):

    f = open(filepath, "r")
    courses = {}
    for line in f:
        record = line.split(",")
        course_code = record[0].split("_")

        for c in course_code:
            courses[c] = record[1]
    f.close()
    pickle.dump(courses, open("temp/course_code_to_name.txt", "wb"))
    # return courses

def course_index_code():

    data = Data("dataset/UQDataset_5_5639_m.csv")

    courses = data.get_courses()
    course_ind2code = {}
    course_code2ind = {}
    for index in range(0,len(courses)):
        course_codes = courses[index].split("_")
        course_ind2code[str(index)] = course_codes
        for code in course_codes:
            course_code2ind[code] = str(index)
    pickle.dump(course_ind2code, open("temp/course_index_to_code.txt", "wb"))
    pickle.dump(course_code2ind, open("temp/course_code_to_index.txt", "wb"))
    # return course_ind2code, course_code2ind


if __name__ == "__main__":
    course_index_code()
    course_code_name("dataset/CourseName_m.csv")