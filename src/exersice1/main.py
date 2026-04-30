import math
import os
import random
import time
from multiprocessing import Process, Manager, Lock


class Student:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.status = "Очередь"
        self.time_start = None
        self.time_end = None
        self.examiner = None
        self.correct = 0
        self.wrong = 0

    def start_exam(self, examiner):
        self.examiner = examiner.name
        self.time_start = time.time()

    def finish_exam(self, correct, wrong, passed):
        self.correct = correct
        self.wrong = wrong
        self.time_end = time.time()
        self.status = "Сдал" if passed else "Провалил"

    def to_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "status": self.status,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "examiner": self.examiner,
            "correct": self.correct,
            "wrong": self.wrong,
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data["name"], data["gender"])
        student.status = data["status"]
        student.time_start = data["time_start"]
        student.time_end = data["time_end"]
        student.examiner = data["examiner"]
        student.correct = data["correct"]
        student.wrong = data["wrong"]
        return student


class Examiner:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.current_student = "-"
        self.total_students = 0
        self.failed_students = 0
        self.work_time = 0.0
        self.lunch_taken = False

    def get_exam_duration(self):
        return random.uniform(max(0.1, len(self.name) - 1), len(self.name) + 1)

    def start_exam(self, student):
        self.current_student = student.name
        student.start_exam(self)

    def finish_exam(self, student, passed, duration):
        self.current_student = "-"
        self.total_students += 1
        self.work_time += duration

        if not passed:
            self.failed_students += 1

    def should_go_to_lunch(self, exam_start_time):
        return not self.lunch_taken and time.time() - exam_start_time >= 30

    def go_to_lunch(self):
        lunch_time = random.uniform(12, 18)
        self.current_student = "-"
        time.sleep(lunch_time)
        self.work_time += lunch_time
        self.lunch_taken = True

    def to_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "current_student": self.current_student,
            "total_students": self.total_students,
            "failed_students": self.failed_students,
            "work_time": self.work_time,
            "lunch_taken": self.lunch_taken,
        }

    @classmethod
    def from_dict(cls, data):
        examiner = cls(data["name"], data["gender"])
        examiner.current_student = data["current_student"]
        examiner.total_students = data["total_students"]
        examiner.failed_students = data["failed_students"]
        examiner.work_time = data["work_time"]
        examiner.lunch_taken = data["lunch_taken"]
        return examiner


class Question:
    def __init__(self, text):
        self.text = text
        self.words = text.split()

    def to_dict(self):
        return {
            "text": self.text,
            "words": self.words,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["text"])


class Exam:
    def __init__(self, questions):
        self.questions = questions
        self.question_stats = {question.text: 0 for question in questions}
        self.phi = (1 + math.sqrt(5)) / 2

    def _build_weights(self, count, gender):
        rest = 1.0
        weights = []

        for _ in range(count - 1):
            weight = rest / self.phi
            weights.append(weight)
            rest -= weight

        weights.append(rest)

        if gender == "Ж":
            weights.reverse()

        return weights

    def _choose_word(self, words, gender):
        weights = self._build_weights(len(words), gender)
        return random.choices(words, weights=weights, k=1)[0]

    def _choose_correct_answers(self, question, examiner_gender):
        available = question.words[:]
        correct_answers = set()

        first = self._choose_word(available, examiner_gender)
        correct_answers.add(first)
        available.remove(first)

        while available:
            if random.random() < 1 / 3:
                word = self._choose_word(available, examiner_gender)
                correct_answers.add(word)
                available.remove(word)
            else:
                break

        return correct_answers

    def _select_questions(self):
        if len(self.questions) >= 3:
            return random.sample(self.questions, 3)

        return random.choices(self.questions, k=3)

    def conduct(self, student, examiner):
        selected_questions = self._select_questions()

        correct = 0
        wrong = 0

        for question in selected_questions:
            student_answer = self._choose_word(question.words, student.gender)
            correct_answers = self._choose_correct_answers(question, examiner.gender)

            if student_answer in correct_answers:
                correct += 1
                self.question_stats[question.text] += 1
            else:
                wrong += 1

        roll = random.random()

        if roll < 1 / 8:
            passed = False
        elif roll < 3 / 8:
            passed = True
        else:
            passed = correct > wrong

        return passed, correct, wrong


def load_lines(filename):
    with open(filename) as file:
        return [line.strip() for line in file]


def load_people(filename):
    people = []

    with open(filename) as file:
        for line in file:
            line = line.strip()

            name, gender = line.split()

            people.append({"name": name, "gender": gender})

    return people


def load_questions(filename):
    return [Question(line) for line in load_lines(filename)]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def make_table(headers, rows):
    widths = []

    for i, header in enumerate(headers):
        max_width = len(str(header))

        for row in rows:
            max_width = max(max_width, len(str(row[i])))

        widths.append(max_width)

    lines = []
    header_line = " | ".join(
        str(headers[i]).ljust(widths[i]) for i in range(len(headers))
    )
    separator = "-+-".join("-" * width for width in widths)

    lines.append(header_line)
    lines.append(separator)

    for row in rows:
        lines.append(" | ".join(str(row[i]).ljust(widths[i]) for i in range(len(row))))

    return "\n".join(lines)


def examiner_worker(
    examiner_name,
    queue,
    students_data,
    examiners_data,
    questions_data,
    question_stats,
    lock,
    exam_start_time,
):
    questions = [Question.from_dict(question_data) for question_data in questions_data]
    exam = Exam(questions)

    while True:
        with lock:
            if len(queue) == 0:
                examiner = Examiner.from_dict(examiners_data[examiner_name])
                examiner.current_student = "-"
                examiners_data[examiner_name] = examiner.to_dict()
                break

            student_name = queue.pop(0)

            student = Student.from_dict(students_data[student_name])
            examiner = Examiner.from_dict(examiners_data[examiner_name])

            examiner.start_exam(student)

            students_data[student_name] = student.to_dict()
            examiners_data[examiner_name] = examiner.to_dict()

        duration = examiner.get_exam_duration()
        time.sleep(duration)

        passed, correct, wrong = exam.conduct(student, examiner)

        with lock:
            student = Student.from_dict(students_data[student_name])
            examiner = Examiner.from_dict(examiners_data[examiner_name])

            student.finish_exam(correct, wrong, passed)
            examiner.finish_exam(student, passed, duration)

            students_data[student_name] = student.to_dict()
            examiners_data[examiner_name] = examiner.to_dict()

            for question in exam.question_stats:
                question_stats[question] = (
                    question_stats.get(question, 0) + exam.question_stats[question]
                )

            exam.question_stats = {question.text: 0 for question in questions}

        examiner = Examiner.from_dict(examiners_data[examiner_name])

        if examiner.should_go_to_lunch(exam_start_time):
            with lock:
                examiner.current_student = "-"
                examiners_data[examiner_name] = examiner.to_dict()

            examiner.go_to_lunch()

            with lock:
                examiners_data[examiner_name] = examiner.to_dict()


def get_students_rows_live(students_data, queue):
    students = list(students_data.values())
    queue_names = list(queue)
    queue_positions = {name: index for index, name in enumerate(queue_names)}

    def sort_key(student):
        status_order = {
            "Очередь": 0,
            "Сдал": 1,
            "Провалил": 2,
        }

        position = queue_positions.get(student["name"], len(queue_positions))

        return status_order[student["status"]], position, student["name"]

    students = sorted(students, key=sort_key)

    return [[student["name"], student["status"]] for student in students]


def get_students_rows_final(students_data):
    students = list(students_data.values())

    def sort_key(student):
        status_order = {
            "Сдал": 0,
            "Провалил": 1,
        }

        return status_order[student["status"]], student["name"]

    students = sorted(students, key=sort_key)

    return [[student["name"], student["status"]] for student in students]


def get_examiners_rows_live(examiners_data):
    examiners = sorted(
        list(examiners_data.values()), key=lambda examiner: examiner["name"]
    )

    return [
        [
            examiner["name"],
            examiner["current_student"],
            examiner["total_students"],
            examiner["failed_students"],
            round(examiner["work_time"], 2),
        ]
        for examiner in examiners
    ]


def get_examiners_rows_final(examiners_data):
    examiners = sorted(
        list(examiners_data.values()), key=lambda examiner: examiner["name"]
    )

    return [
        [
            examiner["name"],
            examiner["total_students"],
            examiner["failed_students"],
            round(examiner["work_time"], 2),
        ]
        for examiner in examiners
    ]


def print_students_live(students_data, queue):
    rows = get_students_rows_live(students_data, queue)
    print("СТУДЕНТЫ")
    print(make_table(["Студент", "Статус"], rows))


def print_examiners_live(examiners_data):
    rows = get_examiners_rows_live(examiners_data)
    print("\nЭКЗАМЕНАТОРЫ")
    print(
        make_table(
            [
                "Экзаменатор",
                "Текущий студент",
                "Всего студентов",
                "Завалил",
                "Время работы",
            ],
            rows,
        )
    )


def print_students_final(students_data):
    rows = get_students_rows_final(students_data)
    print("СТУДЕНТЫ")
    print(make_table(["Студент", "Статус"], rows))


def print_examiners_final(examiners_data):
    rows = get_examiners_rows_final(examiners_data)
    print("\nЭКЗАМЕНАТОРЫ")
    print(
        make_table(["Экзаменатор", "Всего студентов", "Завалил", "Время работы"], rows)
    )


def monitor_worker(
    students_data, examiners_data, queue, exam_start_time, finished_flag, total_students
):
    while not finished_flag.value:
        clear_screen()

        print_students_live(students_data, queue)
        print_examiners_live(examiners_data)

        print()
        print(f"Осталось в очереди: {len(queue)} из {total_students}")
        print(
            f"Время с начала экзамена: {round(time.time() - exam_start_time, 2)} секунд"
        )

        time.sleep(0.3)


def get_best_students(students_data):
    best = []
    min_time = None

    for student in students_data.values():
        if student["status"] != "Сдал":
            continue

        duration = student["time_end"] - student["time_start"]

        if min_time is None or duration < min_time:
            min_time = duration
            best = [student["name"]]
        elif duration == min_time:
            best.append(student["name"])

    return sorted(best)


def get_best_examiners(examiners_data):
    best = []
    min_ratio = None

    for examiner in examiners_data.values():
        if examiner["total_students"] == 0:
            continue

        ratio = examiner["failed_students"] / examiner["total_students"]

        if min_ratio is None or ratio < min_ratio:
            min_ratio = ratio
            best = [examiner["name"]]
        elif ratio == min_ratio:
            best.append(examiner["name"])

    return sorted(best)


def get_expelled(students_data):
    expelled = []
    min_finish_time = None

    for student in students_data.values():
        if student["status"] != "Провалил":
            continue

        finish_time = student["time_end"]

        if min_finish_time is None or finish_time < min_finish_time:
            min_finish_time = finish_time
            expelled = [student["name"]]
        elif finish_time == min_finish_time:
            expelled.append(student["name"])

    return sorted(expelled)


def get_best_questions(question_stats):
    if not question_stats:
        return []

    max_value = max(question_stats.values())

    return sorted(
        [question for question, value in question_stats.items() if value == max_value]
    )


def exam_success(students_data):
    total = len(students_data)

    if total == 0:
        return False

    passed = sum(1 for student in students_data.values() if student["status"] == "Сдал")

    return passed / total > 0.85


def main():
    students_list = load_people("students.txt")
    examiners_list = load_people("examiners.txt")
    questions = load_questions("questions.txt")

    with Manager() as manager:
        queue = manager.list()
        students_data = manager.dict()
        examiners_data = manager.dict()
        questions_data = manager.list()
        question_stats = manager.dict()
        finished_flag = manager.Value("i", 0)
        lock = Lock()

        for student in students_list:
            obj = Student(student["name"], student["gender"])
            students_data[obj.name] = obj.to_dict()
            queue.append(obj.name)

        for examiner in examiners_list:
            obj = Examiner(examiner["name"], examiner["gender"])
            examiners_data[obj.name] = obj.to_dict()

        for question in questions:
            questions_data.append(question.to_dict())
            question_stats[question.text] = 0

        exam_start_time = time.time()
        total_students = len(students_list)

        monitor = Process(
            target=monitor_worker,
            args=(
                students_data,
                examiners_data,
                queue,
                exam_start_time,
                finished_flag,
                total_students,
            ),
        )

        monitor.start()

        processes = []

        for examiner in examiners_list:
            process = Process(
                target=examiner_worker,
                args=(
                    examiner["name"],
                    queue,
                    students_data,
                    examiners_data,
                    questions_data,
                    question_stats,
                    lock,
                    exam_start_time,
                ),
            )

            process.start()
            processes.append(process)

        for process in processes:
            process.join()

        finished_flag.value = 1
        monitor.join()

        total_time = time.time() - exam_start_time

        clear_screen()

        print_students_final(students_data)
        print_examiners_final(examiners_data)

        print()
        print(f"Время экзамена: {round(total_time, 2)} секунд")

        best_students = get_best_students(students_data)
        best_examiners = get_best_examiners(examiners_data)
        expelled = get_expelled(students_data)
        best_questions = get_best_questions(question_stats)

        print("Лучшие студенты:", ", ".join(best_students) if best_students else "-")
        print(
            "Лучшие экзаменаторы:", ", ".join(best_examiners) if best_examiners else "-"
        )
        print("Отчислят:", ", ".join(expelled) if expelled else "-")
        print("Лучшие вопросы:", ", ".join(best_questions) if best_questions else "-")

        if exam_success(students_data):
            print("Экзамен удался")
        else:
            print("Экзамен не удался")


if __name__ == "__main__":
    main()
