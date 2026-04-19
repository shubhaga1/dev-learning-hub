"""
reorganize.py — restructure edu.io by EM/DoE interview priority.

Creates numbered bucket folders and moves course folders into them
with a priority number prefix inside each bucket.

Run: python3 reorganize.py
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).parent

# ── Priority mapping ───────────────────────────────────────────────────────────
# Format: (bucket_folder, [course_folder_name, ...])
# Buckets ordered by EM/DoE interview priority.
# Courses inside each bucket ordered by relevance.

STRUCTURE = [
    ("01-system-design", [
        "Web Application _ Software Architecture 101 - Learn Interactively",
        "Grokking Computer Networking for Software Engineers - Learn Interactively",
        "Database Design Fundamentals for Software Engineers - Learn Interactively",
        "Microservice Architecture_ Practical Implementation - Learn Interactively",
        "An Introduction to Microservice Principles and Concepts - Learn Interactively",
        "Cloud Architecture_ A Guide To Design _ Architect Your Cloud - Learn Interactively",
        "Software Design Patterns_ Best Practices for Software Developers - Learn Interactively",
        "The Definitive Guide to MongoDB - Learn Interactively",
        "An Introductory Guide to SQL - Learn Interactively",
        "Docker for Developers - Learn Interactively",
        "A Practical Guide to Kubernetes - Learn Interactively",
        "Advanced Kubernetes Techniques_ Monitoring_ Logging_ Auto-Scaling - Learn Interactively",
        "Running Serverless Applications with AWS Lambda - Learn Interactively",
        "Learn the A to Z of Amazon Web Services _AWS_ - Learn Interactively",
    ]),
    ("02-leadership-behavioral", [
        "Grokking the Behavioral Interview - Learn Interactively",
    ]),
    ("03-ml-ai", [
        "Machine Learning for Software Engineers - Learn Interactively",
        "Applied Machine Learning_ Deep Learning for Industry - Learn Interactively",
        "Applied Machine Learning_ Industry Case Study with TensorFlow - Learn Interactively",
        "Natural Language Processing with Machine Learning - Learn Interactively",
        "Grokking Data Science - Learn Interactively",
        "Image Recognition with Machine Learning - Learn Interactively",
        "Make Your Own Neural Network in Python - Learn Interactively",
        "Python Data Analysis and Visualization - Learn Interactively",
        "From Python to Numpy - Learn Interactively",
        "Python for Scientists and Engineers - Learn Interactively",
        "Data Science for Non-Programmers - Learn Interactively",
        "Learn Data Science with Bash Shell - Learn Interactively",
    ]),
    ("04-algorithms-ds", [
        "A Visual Introduction to Algorithms - Learn Interactively",
        "Big-O Notation For Coding Interviews and Beyond - Learn Interactively",
        "Data Structures and Algorithms in Python - Learn Interactively",
        "Data Structures in Javascript_ Visualizations _ Exercises - Learn Interactively",
        "Mastering Data Structures and Sorting Algorithms in JavaScript - Learn Interactively",
    ]),
    ("05-java", [
        "Java Multithreading for Senior Engineering Interviews - Learn Interactively",
        "Java Unit Testing with JUnit 5 - Learn Interactively",
        "Learn Object-Oriented Programming in Java - Learn Interactively",
        "The Complete Java Crash Course - Learn Interactively",
        "Learn Java from Scratch - Learn Interactively",
        "Design a Test Automation Framework with Selenium and Java - Learn Interactively",
        "Modern Android App Development with Java - Learn Interactively",
    ]),
    ("06-python", [
        "Python 201 - Interactively Learn Advanced Concepts in Python 3 - Learn Interactively",
        "Python 3_ An interactive deep dive - Learn Interactively",
        "Python Regular Expressions with Data Scraping Projects - Learn Interactively",
        "Flask_ Develop Web Applications in Python - Learn Interactively",
        "Full Speed Python - Learn Interactively",
        "Learn Python from Scratch - Learn Interactively",
        "Python 101_ Interactively learn how to program with Python 3 - Learn Interactively",
        "Learn Object-Oriented Programming in Python - Learn Interactively",
    ]),
    ("07-graphql-api", [
        "A Practical Guide to GraphQL_ From the Client Perspective - Learn Interactively",
    ]),
    ("08-javascript-typescript", [
        "Advanced TypeScript Masterclass - Learn Interactively",
        "Learn TypeScript_ The Complete Course for Beginners - Learn Interactively",
        "Using TypeScript with React - Learn Interactively",
        "The Complete Guide to Modern JavaScript - Learn Interactively",
        "JavaScript In Practice_ ES6 And Beyond - Learn Interactively",
        "Complete JavaScript Course_ Build a Real World App from Scratch - Learn Interactively",
        "Step Up Your JS_ A Comprehensive Guide to Intermediate JavaScript - Learn Interactively",
        "Intermediate JavaScript_ Building Frontend Components - Learn Interactively",
        "JavaScript in Practice_ Getting Started - Learn Interactively",
        "Introduction to JavaScript_ First Steps - Learn Interactively",
        "JavaScript Fundamentals Before Learning React - Learn Interactively",
        "Let_s learn ES6! Master new JavaScript features faster and easier - Learn Interactively",
        "Functional Programming Patterns With RamdaJS! - Learn Interactively",
        "JS Assessment_ Assess your Javascript skills - Learn Interactively",
    ]),
    ("09-react-frontend", [
        "Advanced React Patterns With Hooks - Learn Interactively",
        "The Road to React_ The one with Hooks - Learn Interactively",
        "React in Patterns - Learn Interactively",
        "React Tracked_ Creating Web Apps with Global State - Learn Interactively",
        "Reintroducing React_ V16 and Beyond - Learn Interactively",
        "The Road to React_ The one with Class Components - Learn Interactively",
        "Learn React_js_ Redux _ Immutable_js while building a weather app - Learn Interactively",
        "Practical Redux - Learn Interactively",
        "Understanding Redux_ A Beginner_s Guide To State Management - Learn Interactively",
        "Building Tesla's Battery Range Calculator with React _ Redux - Learn Interactively",
        "Full-Stack Web Applications with Firebase - Learn Interactively",
        "Integrating Firebase with React - Learn Interactively",
        "Testing Vue_js Components with Jest - Learn Interactively",
    ]),
    ("10-web-html-css", [
        "Learn HTML_ CSS_ and JavaScript from Scratch - Learn Interactively",
        "Web Development_ Unraveling HTML_ CSS_ and JavaScript - Learn Interactively",
        "The Complete Advanced Guide to CSS - Learn Interactively",
        "Sass for CSS_ Advanced Frontend Development - Learn Interactively",
        "CSS Theming for Professionals - Learn Interactively",
        "Understanding Flexbox_ Everything you need to know - Learn Interactively",
        "Web Development_ a Primer - Learn Interactively",
        "A Complete Guide to Launching Your Website_ From Local to Live - Learn Interactively",
        "HTML5 Canvas_ From Noob to Ninja - an interactive deep dive - Learn Interactively",
        "Coding for Visual Learners_ Learning JavaScript with p5_js - Learn Interactively",
    ]),
    ("11-go", [
        "Mastering Concurrency in Go - Learn Interactively",
        "An Introduction to Programming in Go - Learn Interactively",
        "The Way to Go - Learn Interactively",
    ]),
    ("12-bash-linux", [
        "Bash for Programmers - Learn Interactively",
        "Master the Bash Shell - Learn Interactively",
        "Learn to Use HPC Systems and Supercomputers - Learn Interactively",
    ]),
    ("13-other-languages", [
        "Learn Rust from Scratch - Learn Interactively",
        "Kotlin Crash Course for Programmers - Learn Interactively",
        "Learn Scala from Scratch - Learn Interactively",
        "Learn Ruby from Scratch - Learn Interactively",
        "Ruby Concurrency for Senior Engineering Interviews - Learn Interactively",
        "Learn R from Scratch - Learn Interactively",
        "Learn Dart_ First Step to Flutter - Learn Interactively",
        "Functional Programming with ReasonML - Learn Interactively",
        "Programming in D_ The Ultimate Guide for Software Engineers - Learn Interactively",
        "Learn PHP from Scratch - Learn Interactively",
        "Learn Perl from Scratch - Learn Interactively",
        "Learn C from Scratch - Learn Interactively",
        "C_ for Programmers_ A Practical Guide - Learn Interactively",
        "Fixing Random_ Techniques in C_ - Learn Interactively",
        "Learn Object-Oriented Programming in C_ - Learn Interactively",
        "Learn C__ from Scratch - Learn Interactively",
        "C__ Fundamentals for Professionals - Learn Interactively",
        "C__ Standard Library including C__ 14 _ C__ 17 - Learn Interactively",
        "C__17 in Detail_ A Deep Dive - Learn Interactively",
        "Generic Programming Templates in C__ - Learn Interactively",
        "Modern C__ Concurrency_ Get the most out of any machine - Learn Interactively",
        "Embedded Programming with Modern C__ - Learn Interactively",
        "Learn Object-Oriented Programming in C__ - Learn Interactively",
        "Learn Object-Oriented Programming in JavaScript - Learn Interactively",
    ]),
    ("14-blockchain-other", [
        "Become a Blockchain Developer - Learn Interactively",
    ]),
]


def main():
    moved   = 0
    missing = []

    for bucket_name, courses in STRUCTURE:
        bucket_path = ROOT / bucket_name
        bucket_path.mkdir(exist_ok=True)

        for i, course in enumerate(courses, 1):
            src = ROOT / course
            if not src.exists():
                missing.append(f"{bucket_name}/{i:02d} — {course}")
                continue

            # New name: 01_Original Course Name...
            new_name = f"{i:02d}_{course}"
            dst = bucket_path / new_name

            if dst.exists():
                print(f"  already moved: {bucket_name}/{new_name[:60]}")
                continue

            shutil.move(str(src), str(dst))
            print(f"  ✓ {bucket_name}/{new_name[:60]}")
            moved += 1

    print(f"\n{'='*60}")
    print(f"Moved: {moved} course folders")

    if missing:
        print(f"\nNot found ({len(missing)}):")
        for m in missing:
            print(f"  ✗ {m}")


if __name__ == "__main__":
    main()
