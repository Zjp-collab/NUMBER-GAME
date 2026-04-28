# HW2
# REMINDER: The work in this assignment must be your own original work and must be completed alone.

import random, os

# --------------------------------------------------
# Course
# --------------------------------------------------

class Course:
    def __init__(self, cid, cname, credits):
        self.cid = cid
        self.cname = cname
        self.credits = credits

    def __str__(self):
        return f"{self.cid}({self.credits}): {self.cname}"

    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(other, Course) and self.cid == other.cid


# --------------------------------------------------
# Catalog
# --------------------------------------------------

class Catalog:
    def __init__(self):
        self.courseOfferings = {}

    def addCourse(self, cid, cname, credits):
        if cid in self.courseOfferings:
            return 'Course already exists'
        self.courseOfferings[cid] = Course(cid, cname, credits)
        return 'Course added successfully'

    def removeCourse(self, cid):
        if cid not in self.courseOfferings:
            return 'Course not found'
        del self.courseOfferings[cid]
        return 'Course removed successfully'

    def _loadCatalog(self, file):
        target_path = os.path.join(os.path.dirname(__file__), file)
        with open(target_path, "r") as f:
            for line in f:
                cid, cname, credits = line.strip().split(',')
                self.courseOfferings[cid] = Course(cid, cname, int(credits))


# --------------------------------------------------
# Semester
# --------------------------------------------------

class Semester:
    def __init__(self):
        self.courses = {}

    def __str__(self):
        if not self.courses:
            return 'No courses'
        return '; '.join(self.courses.keys())

    __repr__ = __str__

    def addCourse(self, course):
        if course.cid in self.courses:
            return 'Course already added'
        self.courses[course.cid] = course
        return 'Course added successfully'

    def dropCourse(self, course):
        if course.cid not in self.courses:
            return 'No such course'
        del self.courses[course.cid]
        return 'Course dropped successfully'

    @property
    def totalCredits(self):
        return sum(c.credits for c in self.courses.values())

    @property
    def isFullTime(self):
        return self.totalCredits >= 12


# --------------------------------------------------
# Loan
# --------------------------------------------------

class Loan:
    def __init__(self, amount):
        self.amount = amount
        self.loan_id = random.randint(10000, 99999)

    def __str__(self):
        return f"Balance: ${self.amount}"

    __repr__ = __str__


# --------------------------------------------------
# Person
# --------------------------------------------------

class Person:
    def __init__(self, name, ssn):
        self.name = name
        self.__ssn = ssn

    def __str__(self):
        return f"Person({self.name}, ***-**-{self.__ssn[-4:]})"

    __repr__ = __str__

    def get_ssn(self):
        return self.__ssn

    def __eq__(self, other):
        return isinstance(other, Person) and self.__ssn == other.get_ssn()


# --------------------------------------------------
# Staff
# --------------------------------------------------

class Staff(Person):
    def __init__(self, name, ssn, supervisor=None):
        super().__init__(name, ssn)
        self.__supervisor = supervisor if isinstance(supervisor, Staff) else None

    def __str__(self):
        return f"Staff({self.name}, {self.id})"

    __repr__ = __str__

    @property
    def id(self):
        initials = ''.join(n[0].lower() for n in self.name.split())
        return f"905{initials}{self.get_ssn()[-4:]}"

    @property
    def getSupervisor(self):
        return self.__supervisor

    def setSupervisor(self, new_supervisor):
        if isinstance(new_supervisor, Staff):
            self.__supervisor = new_supervisor
            return 'Completed!'

    def applyHold(self, student):
        if isinstance(student, Student):
            student.hold = True
            return 'Completed!'

    def removeHold(self, student):
        if isinstance(student, Student):
            student.hold = False
            return 'Completed!'

    def unenrollStudent(self, student):
        if isinstance(student, Student):
            student.active = False
            return 'Completed!'

    def createStudent(self, person):
        return Student(person.name, person.get_ssn(), 'Freshman')


# --------------------------------------------------
# Student
# --------------------------------------------------

class Student(Person):
    def __init__(self, name, ssn, year):
        super().__init__(name, ssn)
        self.classCode = year
        self.semesters = {}
        self.hold = False
        self.active = True
        self.account = StudentAccount(self)

    def __str__(self):
        return f"Student({self.name}, {self.id}, {self.classCode})"

    __repr__ = __str__

    @property
    def id(self):
        initials = ''.join(n[0].lower() for n in self.name.split())
        return f"{initials}{self.get_ssn()[-4:]}"

    def registerSemester(self):
        if not self.active or self.hold:
            return 'Unsuccessful operation'

        key = max(self.semesters.keys(), default=0) + 1
        self.semesters[key] = Semester()

        if key <= 2:
            self.classCode = 'Freshman'
        elif key <= 4:
            self.classCode = 'Sophomore'
        elif key <= 6:
            self.classCode = 'Junior'
        else:
            self.classCode = 'Senior'

    def enrollCourse(self, cid, catalog):
        if not self.active or self.hold:
            return 'Unsuccessful operation'

        course = None
        for k, v in catalog.courseOfferings.items():
            if k.replace(' ', '') == cid.replace(' ', ''):
                course = v
                break

        if not course:
            return 'Course not found'

        semester = self.semesters[max(self.semesters)]
        if course.cid in semester.courses:
            return 'Course already enrolled'

        semester.addCourse(course)
        self.account.chargeAccount(course.credits * StudentAccount.CREDIT_PRICE)
        return 'Course added successfully'

    def dropCourse(self, cid):
        if not self.active or self.hold:
            return 'Unsuccessful operation'

        semester = self.semesters[max(self.semesters)]
        key = None
        for k in semester.courses:
            if k.replace(' ', '') == cid.replace(' ', ''):
                key = k
                break

        if not key:
            return 'Course not found'

        course = semester.courses[key]
        semester.dropCourse(course)
        refund = (course.credits * StudentAccount.CREDIT_PRICE) / 2
        self.account.makePayment(refund)
        return 'Course dropped successfully'

    def getLoan(self, amount):
        if not self.active:
            return 'Unsuccessful operation'

        semester = self.semesters[max(self.semesters)]
        if not semester.isFullTime:
            return 'Not full-time'

        loan = Loan(amount)
        self.account.loans[loan.loan_id] = loan
        self.account.chargeAccount(amount)


# --------------------------------------------------
# StudentAccount
# --------------------------------------------------

class StudentAccount:
    CREDIT_PRICE = 1000

    def __init__(self, student):
        self.student = student
        self.balance = 0
        self.loans = {}

    def __str__(self):
        return (
            f"Name: {self.student.name}\n"
            f"ID: {self.student.id}\n"
            f"Balance: ${self.balance}"
        )

    __repr__ = __str__

    def makePayment(self, amount):
        self.balance -= amount
        return self.balance

    def chargeAccount(self, amount):
        self.balance += amount
        return self.balance


# --------------------------------------------------
# Doctest runner
# --------------------------------------------------

def run_tests():
    import doctest
    doctest.testmod(verbose=True)


if __name__ == "__main__":
    run_tests()
