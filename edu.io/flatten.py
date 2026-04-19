"""
flatten.py — move merged PDFs to bucket level with clean names, remove course folders.

Before:  01-system-design/01_Web Application.../  _MERGED_01_Web Application....pdf
After:   01-system-design/01_Web-Application-Software-Architecture.pdf

Run: python3 flatten.py
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

# Clean name mapping: course folder prefix → short clean filename
NAMES = {
    # 01-system-design
    "01_Web Application":              "01_Web-Application-Software-Architecture",
    "02_Grokking Computer Networking": "02_Grokking-Computer-Networking",
    "03_Database Design":              "03_Database-Design-Fundamentals",
    "04_Microservice Architecture_ Practical": "04_Microservice-Architecture-Practical",
    "05_An Introduction to Microservice":      "05_Microservice-Principles-and-Concepts",
    "06_Cloud Architecture":           "06_Cloud-Architecture-Design",
    "07_Software Design Patterns":     "07_Software-Design-Patterns",
    "08_The Definitive Guide to MongoDB": "08_MongoDB-Definitive-Guide",
    "09_An Introductory Guide to SQL": "09_SQL-Introductory-Guide",
    "10_Docker":                       "10_Docker-for-Developers",
    "11_A Practical Guide to Kubernetes": "11_Kubernetes-Practical-Guide",
    "12_Advanced Kubernetes":          "12_Kubernetes-Advanced-Techniques",
    "13_Running Serverless":           "13_Serverless-AWS-Lambda",
    "14_Learn the A to Z of Amazon":   "14_AWS-A-to-Z",
    # 02-leadership-behavioral
    "01_Grokking the Behavioral":      "01_Grokking-Behavioral-Interview",
    # 03-ml-ai
    "01_Machine Learning for Software": "01_Machine-Learning-for-SWE",
    "02_Applied Machine Learning_ Deep": "02_Applied-ML-Deep-Learning",
    "03_Applied Machine Learning_ Industry": "03_Applied-ML-TensorFlow-Case-Study",
    "04_Natural Language Processing":  "04_NLP-with-Machine-Learning",
    "05_Grokking Data Science":        "05_Grokking-Data-Science",
    "06_Image Recognition":            "06_Image-Recognition-ML",
    "07_Make Your Own Neural Network": "07_Make-Your-Own-Neural-Network",
    "08_Python Data Analysis":         "08_Python-Data-Analysis-Visualization",
    "09_From Python to Numpy":         "09_From-Python-to-Numpy",
    "10_Python for Scientists":        "10_Python-for-Scientists-Engineers",
    "11_Data Science for Non":         "11_Data-Science-for-Non-Programmers",
    "12_Learn Data Science with Bash": "12_Data-Science-with-Bash",
    # 04-algorithms-ds
    "01_A Visual Introduction":        "01_Visual-Introduction-to-Algorithms",
    "02_Big-O Notation":               "02_Big-O-Notation-Coding-Interviews",
    "03_Data Structures and Algorithms in Python": "03_Data-Structures-Algorithms-Python",
    "04_Data Structures in Javascript": "04_Data-Structures-JavaScript",
    "05_Mastering Data Structures":    "05_Mastering-DS-Sorting-Algorithms-JS",
    # 05-java
    "01_Java Multithreading":          "01_Java-Multithreading-Senior-Interviews",
    "02_Java Unit Testing":            "02_Java-Unit-Testing-JUnit5",
    "03_Learn Object-Oriented Programming in Java": "03_OOP-in-Java",
    "04_The Complete Java Crash":      "04_Java-Crash-Course",
    "05_Learn Java from Scratch":      "05_Java-from-Scratch",
    "06_Design a Test Automation":     "06_Test-Automation-Selenium-Java",
    "07_Modern Android":               "07_Android-App-Dev-Java",
    # 06-python
    "01_Python 201":                   "01_Python-201-Advanced-Concepts",
    "02_Python 3_":                    "02_Python-3-Deep-Dive",
    "03_Python Regular Expressions":   "03_Python-Regex-Data-Scraping",
    "04_Flask_":                       "04_Flask-Web-Apps",
    "05_Full Speed Python":            "05_Full-Speed-Python",
    "06_Learn Python from Scratch":    "06_Python-from-Scratch",
    "07_Python 101":                   "07_Python-101",
    "08_Learn Object-Oriented Programming in Python": "08_OOP-in-Python",
    # 07-graphql-api
    "01_A Practical Guide to GraphQL": "01_GraphQL-Practical-Guide",
    # 08-javascript-typescript
    "01_Advanced TypeScript":          "01_Advanced-TypeScript-Masterclass",
    "02_Learn TypeScript_":            "02_TypeScript-Complete-Course",
    "03_Using TypeScript with React":  "03_TypeScript-with-React",
    "04_The Complete Guide to Modern JavaScript": "04_Modern-JavaScript-Complete",
    "05_JavaScript In Practice_":      "05_JavaScript-ES6-and-Beyond",
    "06_Complete JavaScript Course":   "06_JavaScript-Real-World-App",
    "07_Step Up Your JS":              "07_JavaScript-Step-Up",
    "08_Intermediate JavaScript":      "08_JavaScript-Intermediate",
    "09_JavaScript in Practice_ Getting": "09_JavaScript-Getting-Started",
    "10_Introduction to JavaScript":   "10_JavaScript-First-Steps",
    "11_JavaScript Fundamentals Before": "11_JavaScript-Fundamentals-Before-React",
    "12_Let_s learn ES6":              "12_ES6-Mastery",
    "13_Functional Programming Patterns": "13_Functional-Programming-RamdaJS",
    "14_JS Assessment":                "14_JavaScript-Assessment",
    # 09-react-frontend
    "01_Advanced React Patterns":      "01_Advanced-React-Patterns-Hooks",
    "02_The Road to React_ The one with Hooks": "02_Road-to-React-Hooks",
    "03_React in Patterns":            "03_React-in-Patterns",
    "04_React Tracked":                "04_React-Global-State",
    "05_Reintroducing React":          "05_React-V16-and-Beyond",
    "06_The Road to React_ The one with Class": "06_Road-to-React-Class-Components",
    "07_Learn React":                  "07_React-Redux-Immutable",
    "08_Practical Redux":              "08_Practical-Redux",
    "09_Understanding Redux":          "09_Redux-State-Management",
    "10_Building Tesla":               "10_Tesla-Battery-Calculator-React-Redux",
    "11_Full-Stack Web Applications with Firebase": "11_Firebase-Full-Stack",
    "12_Integrating Firebase":         "12_Firebase-with-React",
    "13_Testing Vue":                  "13_Vue-Testing-Jest",
    # 10-web-html-css
    "01_Learn HTML":                   "01_HTML-CSS-JavaScript-from-Scratch",
    "02_Web Development_ Unraveling":  "02_Web-Dev-HTML-CSS-JS",
    "03_The Complete Advanced Guide to CSS": "03_Advanced-CSS-Complete",
    "04_Sass":                         "04_Sass-Advanced-CSS",
    "05_CSS Theming":                  "05_CSS-Theming",
    "06_Understanding Flexbox":        "06_Flexbox-Complete",
    "07_Web Development_ a Primer":    "07_Web-Dev-Primer",
    "08_A Complete Guide to Launching": "08_Website-Launch-Guide",
    "09_HTML5 Canvas":                 "09_HTML5-Canvas-Noob-to-Ninja",
    "10_Coding for Visual Learners":   "10_JavaScript-p5js-Visual",
    # 11-go
    "01_Mastering Concurrency in Go":  "01_Go-Concurrency-Mastery",
    "02_An Introduction to Programming in Go": "02_Go-Introduction",
    "03_The Way to Go":                "03_The-Way-to-Go",
    # 12-bash-linux
    "01_Bash for Programmers":         "01_Bash-for-Programmers",
    "02_Master the Bash Shell":        "02_Bash-Shell-Master",
    "03_Learn to Use HPC":             "03_HPC-Supercomputers",
    # 13-other-languages
    "01_Learn Rust":                   "01_Rust-from-Scratch",
    "02_Kotlin":                       "02_Kotlin-Crash-Course",
    "03_Learn Scala":                  "03_Scala-from-Scratch",
    "04_Learn Ruby from Scratch":      "04_Ruby-from-Scratch",
    "05_Ruby Concurrency":             "05_Ruby-Concurrency-Senior",
    "06_Learn R":                      "06_R-from-Scratch",
    "07_Learn Dart":                   "07_Dart-Flutter",
    "08_Functional Programming with ReasonML": "08_ReasonML-Functional",
    "09_Programming in D":             "09_D-Language",
    "10_Learn PHP":                    "10_PHP-from-Scratch",
    "11_Learn Perl":                   "11_Perl-from-Scratch",
    "12_Learn C from Scratch":         "12_C-from-Scratch",
    "13_C_ for Programmers":           "13_C-for-Programmers",
    "14_Fixing Random":                "14_Csharp-Fixing-Random",
    "15_Learn Object-Oriented Programming in C_": "15_OOP-in-Csharp",
    "16_Learn C__":                    "16_Cpp-from-Scratch",
    "17_C__ Fundamentals":             "17_Cpp-Fundamentals",
    "18_C__ Standard Library":         "18_Cpp-Standard-Library",
    "19_C__17 in Detail":              "19_Cpp17-Deep-Dive",
    "20_Generic Programming":          "20_Cpp-Generic-Templates",
    "21_Modern C__ Concurrency":       "21_Cpp-Modern-Concurrency",
    "22_Embedded Programming":         "22_Cpp-Embedded-Programming",
    "23_Learn Object-Oriented Programming in C__": "23_OOP-in-Cpp",
    "24_Learn Object-Oriented Programming in JavaScript": "24_OOP-in-JavaScript",
    # 14-blockchain-other
    "01_Become a Blockchain":          "01_Blockchain-Developer",
}


def find_clean_name(folder_name: str) -> str:
    """Match folder name prefix to clean name."""
    for prefix, clean in NAMES.items():
        if folder_name.startswith(prefix):
            return clean
    # Fallback: use folder name, strip " - Learn Interactively"
    name = re.sub(r' - Learn Interactively$', '', folder_name)
    name = re.sub(r'[_\s]+', '-', name)
    return name[:60]


def main():
    moved   = 0
    missing = []

    buckets = sorted([d for d in ROOT.iterdir() if d.is_dir() and re.match(r'^\d{2}-', d.name)])

    for bucket in buckets:
        course_dirs = sorted([d for d in bucket.iterdir() if d.is_dir()])

        for course_dir in course_dirs:
            # Find the merged PDF inside
            merged_pdfs = list(course_dir.glob("_MERGED_*.pdf"))
            if not merged_pdfs:
                missing.append(f"{bucket.name}/{course_dir.name} — no merged PDF")
                shutil.rmtree(str(course_dir))
                continue

            merged_pdf = merged_pdfs[0]
            clean_name = find_clean_name(course_dir.name)
            dst = bucket / f"{clean_name}.pdf"

            merged_pdf.rename(dst)
            shutil.rmtree(str(course_dir))
            print(f"  ✓ {bucket.name}/{clean_name}.pdf")
            moved += 1

    print(f"\n{'='*60}")
    print(f"Moved and renamed: {moved} PDFs")
    print(f"Course folders removed: {moved}")
    if missing:
        print(f"\nIssues ({len(missing)}):")
        for m in missing:
            print(f"  ✗ {m}")


if __name__ == "__main__":
    main()
