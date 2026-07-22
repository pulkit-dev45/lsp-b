from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Course, Module, Lesson, Quiz, Question, Option
from django.core.files.base import ContentFile
import requests
from io import BytesIO

PYTHON_MODULES = [
    "Introduction to Python",
    "Data Types & Variables",
    "Control Flow",
    "Functions & Scope",
    "Data Structures",
    "Object-Oriented Programming",
    "Modules & Packages",
    "File I/O",
    "Error Handling",
    "Final Project",
]

WEB_MODULES = [
    "HTML Fundamentals",
    "CSS Styling",
    "JavaScript Basics",
    "DOM Manipulation",
    "Async JavaScript & APIs",
    "React Fundamentals",
    "Node.js & Express",
    "Databases & SQL",
    "Deployment",
    "Full Stack Project",
]

YOUTUBE_VIDEOS = [
    "https://www.youtube.com/embed/rfscVS0vtbw",
    "https://www.youtube.com/embed/WGJJIrtnfpk",
    "https://www.youtube.com/embed/kqtD5dpn9C8",
    "https://www.youtube.com/embed/8DvywoWv6fI",
    "https://www.youtube.com/embed/_uQrJ0TkZlc",
    "https://www.youtube.com/embed/f79MRyMsjrQ",
    "https://www.youtube.com/embed/HVS1lVlPZTs",
    "https://www.youtube.com/embed/ng2o98kH4TY",
    "https://www.youtube.com/embed/Z1Yd7upH0bA",
    "https://www.youtube.com/embed/JJmcL1N2KQs",
]

PYTHON_LESSON_TOPICS = [
    "What is Python", "Installing Python", "Your First Program", "Python Syntax", "Running Python Code",
    "Numbers & Strings", "Booleans & None", "Type Conversion", "Variables & Assignment", "Constants & Naming",
    "If Statements", "For Loops", "While Loops", "Break & Continue", "List Comprehensions",
    "Defining Functions", "Parameters & Arguments", "Return Values", "Lambda Functions", "Scope & Globals",
    "Lists", "Tuples", "Dictionaries", "Sets", "List Operations",
    "Classes & Objects", "Inheritance", "Polymorphism", "Encapsulation", "Magic Methods",
    "Importing Modules", "Standard Library", "Third-Party Packages", "Virtual Environments", "Requirements",
    "Reading Files", "Writing Files", "File Modes", "Context Managers", "CSV & JSON",
    "Try/Except", "Raising Exceptions", "Custom Exceptions", "Logging", "Debugging",
    "Planning Your App", "Building the CLI", "Adding Features", "Testing", "Packaging & Sharing",
]

WEB_LESSON_TOPICS = [
    "HTML Document Structure", "Headings & Paragraphs", "Links & Images", "Lists & Tables", "Forms & Inputs",
    "CSS Selectors", "Box Model", "Flexbox", "Grid Layout", "Responsive Design",
    "Variables & Data Types", "Functions", "Objects & Arrays", "Loops & Conditionals", "ES6+ Features",
    "Selecting Elements", "Modifying the DOM", "Events", "Creating Elements", "Animations",
    "Callbacks & Promises", "Fetch API", "Async/Await", "REST APIs", "Error Handling",
    "JSX & Components", "Props & State", "Hooks", "Routing", "Building an App",
    "Setting Up Express", "Routes & Middleware", "RESTful APIs", "Templates", "Authentication",
    "SQL Basics", "CRUD Operations", "Joins & Relations", "ORM with SQLAlchemy", "NoSQL with MongoDB",
    "Hosting & Domains", "Environment Variables", "CI/CD", "Docker Basics", "Monitoring",
    "Planning the Stack", "Building the Backend", "Building the Frontend", "Connecting Front & Back", "Deploying",
]

PYTHON_QUESTIONS = [
    {"q": "What is the correct syntax to output 'Hello World' in Python?", "opts": [
        "print('Hello World')", "echo 'Hello World'", "printf('Hello World')", "console.log('Hello World')"], "correct": 0},
    {"q": "Which of the following is a mutable data type in Python?", "opts": [
        "Tuple", "String", "List", "Integer"], "correct": 2},
    {"q": "How do you create a function in Python?", "opts": [
        "function myFunc():", "def myFunc():", "create myFunc():", "func myFunc():"], "correct": 1},
    {"q": "Which keyword is used to handle exceptions in Python?", "opts": [
        "catch", "except", "error", "handle"], "correct": 1},
    {"q": "What does the 'len()' function do?", "opts": [
        "Returns length of an object", "Converts to lowercase", "Rounds a number", "Creates a list"], "correct": 0},
    {"q": "Which of the following is NOT a Python data type?", "opts": [
        "List", "Dictionary", "Array", "Tuple"], "correct": 2},
    {"q": "How do you insert comments in Python?", "opts": [
        "// comment", "# comment", "/* comment */", "<!-- comment -->"], "correct": 1},
    {"q": "Which operator is used for exponentiation in Python?", "opts": [
        "^", "**", "^^", "pow()"], "correct": 1},
    {"q": "What is the output of 'print(3 * 'ab')'?", "opts": [
        "ababab", "ab3", "3ab", "Error"], "correct": 0},
    {"q": "Which method removes the last item from a list?", "opts": [
        "delete()", "remove()", "pop()", "shift()"], "correct": 2},
    {"q": "What is the correct way to create a class in Python?", "opts": [
        "class MyClass:", "create MyClass:", "new MyClass:", "object MyClass:"], "correct": 0},
    {"q": "How do you start a for loop?", "opts": [
        "for x in y:", "for (x in y):", "for x > y:", "for each x in y:"], "correct": 0},
    {"q": "Which keyword is used to define a lambda function?", "opts": [
        "lambda", "def", "function", "arrow"], "correct": 0},
    {"q": "What is the output of 'print(type(10))'?", "opts": [
        "<class 'str'>", "<class 'int'>", "<class 'float'>", "<class 'number'>"], "correct": 1},
    {"q": "How do you convert a string to lowercase?", "opts": [
        "str.lower()", "str.toLower()", "str.downcase()", "str.lowercase()"], "correct": 0},
    {"q": "Which library is used for regular expressions in Python?", "opts": [
        "regex", "re", "regexp", "pyregex"], "correct": 1},
    {"q": "What is a dictionary in Python?", "opts": [
        "A list of items", "A key-value store", "A mathematical function", "A type of loop"], "correct": 1},
    {"q": "Which statement is used to exit a loop?", "opts": [
        "exit", "break", "stop", "return"], "correct": 1},
    {"q": "What does the 'self' keyword represent in a class?", "opts": [
        "The class itself", "The instance of the class", "A static method", "A class variable"], "correct": 1},
    {"q": "How do you handle multiple exceptions?", "opts": [
        "Using multiple except blocks", "Using one except block", "Using try-multiple", "Using catch-all"], "correct": 0},
    {"q": "What is the correct file extension for Python files?", "opts": [
        ".pyth", ".pt", ".py", ".p"], "correct": 2},
    {"q": "Which function converts a string to an integer?", "opts": [
        "int()", "str()", "float()", "char()"], "correct": 0},
    {"q": "What is the output of 'print(10 // 3)'?", "opts": [
        "3.33", "3", "3.0", "1"], "correct": 1},
    {"q": "Which data type is immutable?", "opts": [
        "List", "Dictionary", "Set", "Tuple"], "correct": 3},
    {"q": "What does pip stand for?", "opts": [
        "Python Install Program", "Pip Installs Packages", "Python Index Processor", "Package Installer for Python"], "correct": 1},
    {"q": "How do you open a file in Python?", "opts": [
        "open()", "file()", "read()", "load()"], "correct": 0},
    {"q": "What is the purpose of '__init__' method?", "opts": [
        "To initialize variables", "Constructor of a class", "To import modules", "To delete objects"], "correct": 1},
    {"q": "Which of these is NOT a Python framework?", "opts": [
        "Django", "Flask", "Laravel", "FastAPI"], "correct": 2},
    {"q": "What is a decorator in Python?", "opts": [
        "A design pattern", "A function that modifies another function", "A class method", "A type of loop"], "correct": 1},
    {"q": "Which keyword creates a generator?", "opts": [
        "yield", "return", "await", "generate"], "correct": 0},
    {"q": "What is the result of 'set([1,2,2,3])'?", "opts": [
        "{1,2,2,3}", "{1,2,3}", "[1,2,2,3]", "(1,2,3)"], "correct": 1},
    {"q": "How do you check the type of a variable?", "opts": [
        "typeof()", "type()", "isinstance()", "kind()"], "correct": 1},
    {"q": "Which module provides math functions?", "opts": [
        "math", "cmath", "numeric", "algebra"], "correct": 0},
    {"q": "What is the output of 'bool([])'?", "opts": [
        "True", "False", "None", "Error"], "correct": 1},
    {"q": "How do you add an element to a set?", "opts": [
        "add()", "append()", "insert()", "push()"], "correct": 0},
    {"q": "What is the purpose of 'super()'?", "opts": [
        "Call parent class method", "Create super user", "Define super function", "Access super variables"], "correct": 0},
    {"q": "Which operator checks equality?", "opts": [
        "=", "==", "===", "!="], "correct": 1},
    {"q": "What is a virtual environment?", "opts": [
        "A simulated OS", "Isolated Python environment", "A cloud server", "A code editor"], "correct": 1},
    {"q": "How do you install a package with pip?", "opts": [
        "pip install package", "pip add package", "pip get package", "pip load package"], "correct": 0},
    {"q": "What is the output of 'print(2 ** 3)'?", "opts": [
        "6", "8", "9", "5"], "correct": 1},
    {"q": "Which method returns the index of an element?", "opts": [
        "find()", "index()", "search()", "locate()"], "correct": 1},
    {"q": "What is the purpose of 'pass' statement?", "opts": [
        "Skip the current iteration", "Do nothing placeholder", "Exit the program", "Pass arguments"], "correct": 1},
    {"q": "Which parameter is used to specify the default value in a function?", "opts": [
        "default", "optional", "keyword", "positional"], "correct": 0},
    {"q": "What does 'JSON' stand for?", "opts": [
        "Java Serialized Object Notation", "JavaScript Object Notation", "Java Standard Output Notation",
        "JavaScript Ordered Network"], "correct": 1},
    {"q": "How do you create an alias while importing?", "opts": [
        "import numpy as np", "import numpy alias np", "from numpy import np", "include numpy as np"], "correct": 0},
    {"q": "Which method reads a file line by line?", "opts": [
        "read()", "readline()", "readlines()", "scan()"], "correct": 1},
    {"q": "What is the purpose of 'if __name__ == '__main__'?'", "opts": [
        "Check if running as main program", "Define main function", "Import main module", "Create main class"],
        "correct": 0},
    {"q": "Which data structure follows FIFO?", "opts": [
        "Stack", "Queue", "Tree", "Graph"], "correct": 1},
    {"q": "What does 'PEP 8' refer to?", "opts": [
        "Python Enhancement Proposal", "Python Execution Protocol", "Python Error Prevention", "Python Exception Policy"],
        "correct": 0},
    {"q": "How do you raise a custom exception?", "opts": [
        "raise Exception('msg')", "throw Exception('msg')", "error Exception('msg')", "except Exception('msg')"],
        "correct": 0},
]

WEB_QUESTIONS = [
    {"q": "What does HTML stand for?", "opts": [
        "Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyper Transfer Markup Language"], "correct": 0},
    {"q": "Which HTML tag is the largest heading?", "opts": [
        "<head>", "<h6>", "<h1>", "<heading>"], "correct": 2},
    {"q": "How do you create a hyperlink in HTML?", "opts": [
        "<a href='url'>link</a>", "<link src='url'>link</link>", "<href url='url'>link</href>", "<hyperlink url='url'>link</hyperlink>"], "correct": 0},
    {"q": "Which CSS property changes the text color?", "opts": [
        "text-color", "font-color", "color", "text-style"], "correct": 2},
    {"q": "What is the correct way to include JavaScript in HTML?", "opts": [
        "<script src='file.js'>", "<javascript src='file.js'>", "<js src='file.js'>", "<link src='file.js'>"], "correct": 0},
    {"q": "What does CSS stand for?", "opts": [
        "Computer Style Sheets", "Cascading Style Sheets", "Creative Style System", "Colorful Style Sheets"], "correct": 1},
    {"q": "Which property is used for flexbox?", "opts": [
        "display: flex", "display: block", "display: inline", "display: grid"], "correct": 0},
    {"q": "How do you declare a JavaScript variable?", "opts": [
        "var x = 5", "v x = 5", "variable x = 5", "int x = 5"], "correct": 0},
    {"q": "Which method selects an element by ID?", "opts": [
        "getElementById()", "getElementByClass()", "getElementByTag()", "getElementByName()"], "correct": 0},
    {"q": "What does API stand for?", "opts": [
        "Application Programming Interface", "Application Processing Integration", "Automated Program Interaction", "Advanced Protocol Interface"], "correct": 0},
    {"q": "Which HTML tag creates a paragraph?", "opts": ["<para>", "<p>", "<text>", "<paragraph>"], "correct": 1},
    {"q": "What is the default position in CSS?", "opts": ["relative", "absolute", "static", "fixed"], "correct": 2},
    {"q": "Which method adds an event listener?", "opts": [
        "addEventListener()", "attachEvent()", "listenEvent()", "onEvent()"], "correct": 0},
    {"q": "What is React?", "opts": [
        "A JavaScript library for UI", "A CSS framework", "A database", "A programming language"], "correct": 0},
    {"q": "What does 'this' refer to in JavaScript?", "opts": [
        "The current object", "The parent object", "The global object", "Depends on context"], "correct": 3},
    {"q": "Which HTML tag is used for an image?", "opts": ["<img>", "<image>", "<pic>", "<src>"], "correct": 0},
    {"q": "What is the box model?", "opts": [
        "Content, padding, border, margin", "Header, main, footer", "HTML, CSS, JS", "Inline, block, flex"], "correct": 0},
    {"q": "Which symbol selects an ID in CSS?", "opts": [".", "#", "@", "$"], "correct": 1},
    {"q": "What is a promise in JavaScript?", "opts": [
        "An async operation handler", "A data type", "A loop construct", "A CSS selector"], "correct": 0},
    {"q": "What does NPM stand for?", "opts": [
        "Node Package Manager", "New Programming Module", "Network Process Manager", "Node Project Manager"], "correct": 0},
    {"q": "Which HTML tag creates an input field?", "opts": ["<input>", "<text>", "<field>", "<form>"], "correct": 0},
    {"q": "What is a media query used for?", "opts": [
        "Responsive design", "Database queries", "API calls", "File uploads"], "correct": 0},
    {"q": "What does 'JSON.parse()' do?", "opts": [
        "Converts JSON string to object", "Converts object to JSON string", "Parses HTML", "Validates JSON"], "correct": 0},
    {"q": "What is JSX?", "opts": [
        "JavaScript XML syntax", "A new JavaScript version", "A CSS preprocessor", "A build tool"], "correct": 0},
    {"q": "Which HTTP method retrieves data?", "opts": ["GET", "POST", "PUT", "DELETE"], "correct": 0},
    {"q": "What attribute opens a link in a new tab?", "opts": [
        "target='_blank'", "new='tab'", "open='new'", "rel='external'"], "correct": 0},
    {"q": "Which CSS unit is relative to font-size?", "opts": ["px", "em", "cm", "pt"], "correct": 1},
    {"q": "What is the purpose of 'useState'?", "opts": [
        "Manage component state", "Create routes", "Handle forms", "Style components"], "correct": 0},
    {"q": "What is middleware in Express?", "opts": [
        "Functions that process requests", "Database connectors", "Template engines", "Route definitions"], "correct": 0},
    {"q": "What is SQL used for?", "opts": [
        "Database management", "Styling web pages", "Server configuration", "API development"], "correct": 0},
    {"q": "Which HTML tag creates an ordered list?", "opts": ["<ol>", "<ul>", "<li>", "<list>"], "correct": 0},
    {"q": "What does 'git clone' do?", "opts": [
        "Copies a repository", "Creates a branch", "Saves changes", "Deletes files"], "correct": 0},
    {"q": "What is a RESTful API?", "opts": [
        "An API following REST principles", "A database type", "A CSS framework", "A JavaScript library"], "correct": 0},
    {"q": "Which CSS property centers text?", "opts": [
        "text-align: center", "align: center", "center: text", "justify: center"], "correct": 0},
    {"q": "What does 'event.preventDefault()' do?", "opts": [
        "Prevents default behavior", "Stops event propagation", "Removes event listener", "Creates a new event"], "correct": 0},
    {"q": "What is a database index?", "opts": [
        "Speed up queries", "Store text data", "Create backups", "Encrypt data"], "correct": 0},
    {"q": "Which command starts a React app?", "opts": [
        "npm start", "npm run dev", "npm build", "npm init"], "correct": 0},
    {"q": "What does CORS stand for?", "opts": [
        "Cross-Origin Resource Sharing", "Cross-Origin Request System", "Central Object Response Service",
        "Common Origin Resource Sharing"], "correct": 0},
    {"q": "Which property creates space inside an element?", "opts": ["padding", "margin", "border", "gap"], "correct": 0},
    {"q": "What is the virtual DOM?", "opts": [
        "A lightweight copy of the real DOM", "A database for DOM", "A CSS preprocessor", "A build tool"], "correct": 0},
    {"q": "What is the purpose of 'key' in React lists?", "opts": [
        "Identify elements uniquely", "Style list items", "Handle clicks", "Store data"], "correct": 0},
    {"q": "Which method sends a POST request?", "opts": [
        "fetch(url, {method: 'POST'})", "fetch.post(url)", "http.post(url)", "ajax.post(url)"], "correct": 0},
    {"q": "What does Docker do?", "opts": [
        "Containerizes applications", "Manages databases", "Edits code", "Deploys websites"], "correct": 0},
    {"q": "Which status code means 'Not Found'?", "opts": ["200", "301", "404", "500"], "correct": 2},
    {"q": "What is environment variable?", "opts": [
        "Configuration for app environment", "A JavaScript variable", "A CSS custom property", "A database field"], "correct": 0},
    {"q": "What is CI/CD?", "opts": [
        "Continuous Integration/Continuous Deployment", "Code Integration/Code Development",
        "Computer Interface/Computer Design", "Central Input/Central Output"], "correct": 0},
    {"q": "Which HTML tag is semantic for navigation?", "opts": ["<nav>", "<menu>", "<header>", "<div>"], "correct": 0},
    {"q": "What does the spread operator (...) do?", "opts": [
        "Expands iterables into elements", "Creates a loop", "Defines a function", "Declares a variable"], "correct": 0},
    {"q": "What is SQL injection?", "opts": [
        "A security vulnerability", "A database type", "A query method", "A data structure"], "correct": 0},
    {"q": "Which tool is used for version control?", "opts": ["Git", "NPM", "Webpack", "Babel"], "correct": 0},
]


class Command(BaseCommand):
    help = 'Seeds the database with dummy courses, modules, lessons, quizzes'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        if admin_user:
            admin_user.set_password('admin123')
            admin_user.save()

        demo_user, _ = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@example.com'}
        )
        if demo_user:
            demo_user.set_password('demo123')
            demo_user.save()

        course1 = self._create_course(
            title='Python Programming Masterclass',
            desc='From zero to Python pro. Master variables, functions, OOP, and build real-world projects.',
            is_active=True
        )
        self._create_modules_lessons_quizzes(
            course1, PYTHON_MODULES, PYTHON_LESSON_TOPICS, YOUTUBE_VIDEOS, PYTHON_QUESTIONS
        )

        course2 = self._create_course(
            title='Web Development Bootcamp',
            desc='Build modern web apps with HTML, CSS, JavaScript, React, Node.js, and databases.',
            is_active=True
        )
        self._create_modules_lessons_quizzes(
            course2, WEB_MODULES, WEB_LESSON_TOPICS, YOUTUBE_VIDEOS[1:] + [YOUTUBE_VIDEOS[0]], WEB_QUESTIONS
        )

        self.stdout.write(self.style.SUCCESS(f'Created {Course.objects.count()} courses'))
        self.stdout.write(self.style.SUCCESS(f'Created {Module.objects.count()} modules'))
        self.stdout.write(self.style.SUCCESS(f'Created {Lesson.objects.count()} lessons'))
        self.stdout.write(self.style.SUCCESS(f'Created {Quiz.objects.count()} quizzes'))
        self.stdout.write(self.style.SUCCESS(f'Created {Question.objects.count()} questions'))
        self.stdout.write(self.style.SUCCESS(f'Created {Option.objects.count()} options'))

    def _create_course(self, title, desc, is_active=True):
        course = Course.objects.create(
            title=title,
            description=desc,
            is_active=is_active,
        )
        img_url = f"https://picsum.photos/seed/{title.lower().replace(' ', '')}/800/450"
        try:
            resp = requests.get(img_url, timeout=10)
            if resp.status_code == 200:
                img_bytes = BytesIO(resp.content)
                course.thumbnail.save(f'{title.lower().replace(" ", "_")}.jpg', ContentFile(img_bytes.getvalue()))
        except Exception:
            self.stdout.write(self.style.WARNING(f'Could not fetch thumbnail for {title}'))
        return course

    def _create_modules_lessons_quizzes(self, course, module_titles, all_lesson_topics, videos, all_questions):
        lesson_idx = 0
        q_idx = 0

        for mod_order, mod_title in enumerate(module_titles, 1):
            module = Module.objects.create(
                course=course,
                title=mod_title,
                order=mod_order,
            )

            for les_order in range(1, 6):
                if lesson_idx >= len(all_lesson_topics):
                    break
                lesson = Lesson.objects.create(
                    course=course,
                    module=module,
                    title=all_lesson_topics[lesson_idx],
                    description=f"Learn about {all_lesson_topics[lesson_idx].lower()} in this comprehensive lesson.",
                    youtube_url=videos[(lesson_idx) % len(videos)],
                    order=lesson_idx + 1,
                    duration_minutes=8 + (lesson_idx % 8),
                )
                lesson_idx += 1

            quiz = Quiz.objects.create(
                module=module,
                title=f'{mod_title} Quiz',
            )

            for q_num in range(5):
                if q_idx >= len(all_questions):
                    q_idx = 0
                qdata = all_questions[q_idx]
                question = Question.objects.create(
                    quiz=quiz,
                    question=qdata['q'],
                )
                for opt_idx, opt_val in enumerate(qdata['opts']):
                    Option.objects.create(
                        question=question,
                        option_value=opt_val,
                        is_correct=(opt_idx == qdata['correct']),
                    )
                q_idx += 1
