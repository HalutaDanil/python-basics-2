# Project 02 — Python_Bootcamp

**Summary:**  
In this project, you'll practice using object-oriented, procedural, and multiparadigm approaches in Python — and you'll also write code that follows the functional programming paradigm.

💡 Click here to share your feedback on this project. It's anonymous and helps us make the learning experience better. We recommend filling out the survey right after completing the project.

## Contents

  - [Chapter I](#chapter-i)
    - [Instructions](#instructions)
  - [Chapter II](#chapter-ii)
    - [General Information](#general-information)
  - [Chapter III](#chapter-iii)
    - [Task 1. Exam](#task-1-exam)
    - [Task 2. Image Downloader](#task-2-image-downloader)

## Chapter I

### Instructions

1. Throughout this course, you'll often feel uncertain and lacking information — that's normal. Remember: the repository and Google are always with you. So are your peers and Rocket.Chat. Communicate. Search. Use common sense. Don't be afraid to make mistakes.
2. Be mindful of your sources. Verify. Think critically. Analyze. Compare.
3. Read each task carefully. Then read it again.
4. Go through the examples just as attentively — they may contain important details not explicitly mentioned in the task description.
5. You might encounter contradictions — something in a task or example may conflict with what you've already learned. If that happens, try to figure it out. If you're stuck, write it down as an open question and resolve it during the process. Never leave open questions unanswered.
6. If a task seems unclear or impossible — it just seems that way. Try breaking it down. Chances are, the individual parts will start to make sense.
7. You'll face a variety of challenges. Bonus tasks are for the curious and meticulous — they're more difficult and optional, but completing them will give you extra experience and insight.
8. Don’t try to game the system or fool others — in the end, you’re only fooling yourself.
9. Got a question? Ask the peer on your right. If that doesn’t help — ask the one on your left.
10. When you get help, always make sure you understand it fully: the why, the how, and the what for. Otherwise, the help is meaningless.
11. Always push to the develop branch only! The master branch will be ignored. Work inside the src directory.
12. Your directory should only contain the files explicitly required by the tasks.

## Chapter II

### General Information

Topics to explore:

- **OOP (Object-Oriented Programming)** — a programming paradigm that structures and organizes code as objects that interact with each other.
- **Procedural approach** — a programming style where tasks are broken down into small procedures or functions.
- **Functional paradigm** — focuses on defining and applying functions that transform data without mutating the original values.
- **Multiparadigm approach** — combining multiple programming paradigms within a single program.
- **Differences from C and C++** — syntax, dynamic typing, memory management, and built-in libraries.
- **Asynchronous / parallel programming** — techniques for running multiple tasks simultaneously.

## Chapter III

**Important!** Each task must be organized as a separate project.  
For example: `T01/src/exercise0`, `T01/src/exercise1`, ..., `T01/src/exerciseN-1`, where **N** is the total number of tasks.  
If one task builds upon the previous one, simply copy the previous project into the new directory and continue development from there.

### Task 1. Exam

Students are lining up to take an exam. Several examiners are working simultaneously. All students wait in a single shared queue. As soon as an examiner becomes available, the next student in line enters for their exam.

Thirty seconds after the exam begins, each examiner is allowed to take a lunch break. They finish the current session and then refuse new students for a random duration between 12 and 18 seconds.

The exam process works as follows:  
Each student is asked three questions from a question bank. For each question, the student randomly picks a word from the question as their answer. Statistically, boys tend to choose words closer to the beginning of the question, while girls prefer words toward the end. The probabilities follow the golden ratio distribution. For example, for the question “There is a table,” a boy would answer “There” with probability `**a = 1/F**`, “is” with `**b = (1–a)/F**`, and “table” with `**c = 1–a–b**`, where `**F ≈ 1.618...**` (for a 4-word question, `**c = (1–a–b)/F**`, and so on). A girl answering the same question would choose “table” with probability `**a**`, “is” with `**b**`, and “There” with `**c**`.

Examiners do not know the correct answer in advance, so they follow the same approach and randomly select words from the question. Multiple correct answers are allowed: after selecting one, the examiner has a 1/3 chance of picking another, and continues this process until stopping or selecting all words from the question as correct.

Once the student has answered, the examiner decides whether they passed the exam. There is a 1/8 chance the examiner is in a bad mood (in which case the student automatically fails), a 1/4 chance of a good mood (student automatically passes), and a 5/8 chance of a neutral mood. In that case, the outcome depends on performance: the student passes if they gave more correct than incorrect answers.

The duration of the exam depends on the length of the examiner's name. For example, an examiner named **Stepan** (6 letters) would conduct exams lasting between 5 and 7 seconds (a random float in that range).

You need to simulate the exam process.

When the program starts:

- The list of examiners is read from examiners.txt.
- The list of students, who arrived in advance and formed a queue, is read from students.txt.
- The question bank is read from questions.txt.

The exam then begins.

Each examiner conducts exams on a separate thread.

During execution, the console must display up-to-date exam information, including:

1. **Table of students** with two columns: "Student" and "Status"
    - Status can be one of the following: "In queue", "Passed", "Failed". The table must be sorted by status: students in queue (in the order they’ll be examined), followed by those who passed, then those who failed.
2. **Table of examiners** with five columns: "Examiner", "Current student", "Total students", "Failed", "Work time"
    - When the examiner is on a break or done for the day, show "-" in the "Current student" column.
3. A **separate line** showing the number of students still in queue out of the total.
4. A **separate line** displaying the time since the exam started.

This information should be **updated in-place**, not printed as new lines.

**When the exam ends and program stops, display**

1. **Table of students** with two columns: "Student" and "Status"
    - Status is now only "Passed" or "Failed". Table sorted: passed first, failed last.
2. **Table of examiners** with four columns: "Examiner", "Total students", "Failed", "Work time"
3. A **separate line** showing total time from exam start to finish.
4. A **separate line** listing **top-performing students** (those who passed the exam the fastest), comma-separated.
5. A **separate line** listing **top examiners** (those with the **lowest failure rate** among their students), comma-separated.
6. A **separate line** listing **students to be expelled** — these are the ones who failed **and finished earlier** than others who also failed.
7. A **separate line** listing the **best questions**, comma-separated — a question is considered best if the highest number of students answered it correctly.
8. A **separate line** with the **exam result summary**. The exam is considered successful if **more than 85%** of students passed.

**Input**

| examiners.txt |
| --- |
| Stepan M<br>Darya F<br>Mikhail M |

| students.txt |
| --- |
| Petr M<br>Sergey M<br>Varvara F<br><br>Ivan M<br>Ekaterina F<br>Alexandra F<br>Aleksey M |

| questions.txt |
| --- |
| There is a table<br>A man is a dog’s friend<br>Solar eclipses affect people<br>Programming is an interesting activity |

**Output**

During exam

```
+------------+----------+
| Student    |  Status  |
+------------+----------+
| Aleksey    | In queue |
| Petr       |  Passed  |
| Ivan       |  Passed  |
| Ekaterina  |  Passed  |
| Sergey     |  Failed  |
| Varvara    |  Failed  |
| Alexandra  |  Failed  |
+------------+----------+

+-------------+-----------------+-----------------+---------+--------------+
| Examiner    | Current student | Total students  | Failed  | Work time    |
+-------------+-----------------+-----------------+---------+--------------+
| Stepan      | Aleksey         |        1        |    0    |    12.31     |
| Darya       | -               |        3        |    2    |    12.14     |
| Mikhail     | -               |        2        |    1    |     7.21     |
+-------------+-----------------+-----------------+---------+--------------+

Remaining in queue: 1 out of 7
Time since exam started: 12.31

```

After exam

```
+------------+----------+
| Student    |  Status  |
+------------+----------+
| Petr       |  Passed  |
| Ivan       |  Passed  |
| Ekaterina  |  Passed  |
| Sergey     |  Failed  |
| Varvara    |  Failed  |
| Alexandra  |  Failed  |
| Aleksey    |  Failed  |
+------------+----------+

+-------------+-----------------+---------+--------------+
| Examiner    | Total students  | Failed  | Work time    |
+-------------+-----------------+---------+--------------+
| Stepan      |        2        |    1    |    12.35     |
| Darya       |        3        |    2    |    12.14     |
| Mikhail     |        2        |    1    |     7.21     |
+-------------+-----------------+---------+--------------+

Time from exam start to finish: 12.35  
Top-performing students: Ivan  
Top examiners: Stepan, Mikhail  
Students to be expelled: Varvara  
Best questions: There is a table, A man is a dog’s friend  
Result: Exam failed
```

### Task 2. Image Downloader
Write a link handler that prompts the user to enter an image URL and then downloads it asynchronously. The user should be asked for the next URL immediately after entering the previous one, continuing until they enter an empty line. If not all images have been downloaded by that point, display a message and terminate the program only after all downloads are complete.

If any error occurs, do not terminate the program immediately. Instead, store the status for summary output at the end.  
At the beginning, the user must specify the path where the downloaded images should be saved.  
If the specified path is invalid or the program does not have write access to it, prompt the user to enter a different path.

Before exiting, display a summary of successful and failed downloads.

**Input**

```
./img
https://images2.pics4learning.com/catalog/s/swamp_15.jpg
https://bad-link-no-website-here.strange/img.png
https://images2.pics4learning.com/catalog/p/parrot.jpg

```

**Output**

Summary of successful and unsuccessful downloads

```
+----------------------------------------------------------+--------+
| Link                                                     | Status |
+----------------------------------------------------------+--------+
| https://images2.pics4learning.com/catalog/s/swamp_15.jpg | Success|
| https://bad-link-no-website-here.strange/img.png         | Error  |
| https://images2.pics4learning.com/catalog/p/parrot.jpg   | Success|
+----------------------------------------------------------+--------+
```