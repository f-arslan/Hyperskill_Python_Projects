class University:
    def __init__(self) -> None:
        self.departments = {"Biotech": [], "Chemistry": [],
                            "Engineering": [], "Mathematics": [], "Physics": []}
        self.places = int(input())
        self.total_list = self.load_applicants()
        self.chem_sort = self.total_list[0]
        self.engineering_sort = self.total_list[1]
        self.math_sort = self.total_list[2]
        self.physics_sort = self.total_list[3]
        self.biotech_sort = self.total_list[4]

    @staticmethod
    def load_applicants():
        with open('applicant_list_7.txt', 'r') as f:
            applicants = [applicant.strip('\n').split() for applicant in f]

        physics_sort = sorted(
            applicants, key=lambda x: (-max((float(x[2]) + float(x[4])) / 2, float(x[6])), x[0] + x[1]))
        chem_sort = sorted(
            applicants, key=lambda x: (-max(float(x[3]), float(x[6])), x[0] + x[1]))
        math_sort = sorted(
            applicants, key=lambda x: (-max(float(x[4]), float(x[6])), x[0] + x[1]))
        engineering_sort = sorted(
            applicants, key=lambda x: (-max((float(x[5]) + float(x[4])) / 2, float(x[6])), x[0] + x[1]))
        biotech_sort = sorted(
            applicants, key=lambda x: (-max((float(x[3]) + float(x[2])) / 2, float(x[6])), x[0] + x[1]))

        total_list = (chem_sort, engineering_sort,
                      math_sort, physics_sort, biotech_sort)
        return total_list

    def assign_applicants(self):
        for i in range(7, 10):
            self.priority_list(i)

    def priority_list(self, priority):

        sort_list = [self.biotech_sort, self.chem_sort,
                     self.engineering_sort, self.math_sort, self.physics_sort]

        sort_name = ['Biotech', 'Chemistry',
                     'Engineering', 'Mathematics', 'Physics']
        index = 0
        for applicant_list in sort_list:
            for applicant in applicant_list:
                if applicant[priority] == sort_name[index] and len(self.departments.get(sort_name[index])) < self.places:
                    self.departments[sort_name[index]].append(applicant)
                    self.remove_all(applicant)
            index += 1

    def remove_all(self, key):
        reaming_applications_chem = list(self.chem_sort)
        reaming_applications_engineering = list(self.engineering_sort)
        reaming_applications_math = list(self.math_sort)
        reaming_applications_physics = list(self.physics_sort)
        reaming_applications_biotech = list(self.biotech_sort)
        sort_list = [self.biotech_sort, self.chem_sort, self.engineering_sort,
                     self.math_sort, self.physics_sort]
        list_remain = [reaming_applications_biotech, reaming_applications_chem, reaming_applications_engineering,
                       reaming_applications_math, reaming_applications_physics]

        index = 0
        for applicant_list in sort_list:
            for application in applicant_list:
                if application == key:
                    list_remain[index].remove(application)
                    break
            index += 1

        self.biotech_sort = reaming_applications_biotech
        self.chem_sort = reaming_applications_chem
        self.engineering_sort = reaming_applications_engineering
        self.math_sort = reaming_applications_math
        self.physics_sort = reaming_applications_physics

    def publish_results_writes(self):
        another_keys = [[2, 3], [3, 3], [4, 5], [4, 4], [2, 4]]
        text_list = ['biotech.txt', 'chemistry.txt',
                     'engineering.txt', 'mathematics.txt', 'physics.txt']
        i = 0
        for key in self.departments.keys():
            self.departments[key].sort(
                key=lambda x: (-max((float(x[another_keys[i][0]]) + float(x[another_keys[i][1]])), float(x[6]) * 2), x[0] + x[1]))
            print(key)
            with open(text_list[i], 'w') as f:
                for student in self.departments[key]:
                    keep = max(((float(
                        student[another_keys[i][0]]) + float(student[another_keys[i][1]])) / 2), float(student[6]))
                    print(student[0], student[1], max(((float(
                        student[another_keys[i][0]]) + float(student[another_keys[i][1]])) / 2), float(student[6])))
                    f.write(student[0] + ' ' + student[1] + ' ' + str(keep) + '\n')
                print('')
            i += 1


esogu = University()
esogu.assign_applicants()
esogu.publish_results_writes()

