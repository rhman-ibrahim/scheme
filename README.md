<header>
    <h1>Scheme | sch</h1>
    <p><b>Scheme</b> is my foundation upon which I construct <b>web</b> projects, based on <a href="#python"><b>Python</b></a> (<a href="#django"><b>Django</b></a>/<a href="#drf"><b>DRF</b></a>) for the back-end and <a href="#javascript"><b>JavaScript</b></a> (<a href="#react"><b>React</b></a>/<a href="#vite"><b>Vite</b></a>) for the front-end, alongside with <a href="#bash"><b>Bash</b></a> scripts to automate general project tasks. I created this repository during the early days of <b>Django</b> learning process and before starting learning <b>React</b>, I decided to keep because I'm really proud of this messy commits which talk about my journey from being lost and overwhelmed to focus and determination. Also to use this repository to explain <b>Scheme</b> related repositories which are <a href="#sch-py"><b>sch-py</b></a>, <a href="#sch-js"><b>sch-js</b></a>, <a href="#sch-sh"><b>sch-sh</b></a> and <a href="#sch-cf"><b>sch-cf</b></a>; I will explain each of them and the tools used below.</p>
    <h2>Here You Will Find</h2>
    <ul>
        <li><a href="https://github.com/rhman-ibrahim/scheme/blob/main/sch.sh" target="_blank"><b>sch</b></a> is a bash script that takes the project name (a string) as a parameter, to create <b>Scheme</b> project based on the latest versions of <b>Scheme</b> related repositories.</li>
        <li><a href="https://github.com/rhman-ibrahim/scheme/blob/main/release.sh" target="_blank"><b>release</b></a> is a bash script that takes the project name and the relase tag (both are strings), to create <b>Scheme</b> project based on the chosen release.</li>
    </ul>
</header>
<main>
    <section id="sch-py">
        <h2>sch-py: Python | (Django & DRF)</h2>
        <p><b>sch-py</b> repository stores the project's back-end code which is built using Django and DRF, this code manages the database models, API endpoints, validation, error handling and more. For more information visit <a href="https://github.com/rhman-ibrahim/sch-py" target="_blank"><b>sch-py</b></a>.</p>
        <ul>
            <li id="python"><b>Python</b> is a high-level, interpreted programming language known for its simplicity and readability. Python emphasizes code readability and a clean syntax, which makes it an ideal language for beginners and experienced programmers alike. Created by <mark><b>Guido van Rossum</b></mark> and released in <b>1991</b></li>
            <li id="django"><b>Django</b> is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. Created by <mark><b>Adrian Holovaty</b></mark> and <mark><b>Simon Willison</b></mark> while working at the Lawrence Journal-World newspaper in <b>2003</b>.</li>
            <li id="drf"><b>Django REST Framework (DRF)</b> is a powerful and flexible toolkit for building Web APIs (Application Programming Interfaces) using Django, which is a high-level Python web framework. DRF provides a set of tools and libraries that simplify the process of building web APIs in Django-based applications. Created by <mark><b>Tom Christie</b></mark>. It was first released as an open-source project in <b>November 2011</b>.</li>
        </ul>
        <nav>
            <a href="https://www.python.org/" target="_blank">
                <img src="https://skillicons.dev/icons?i=python" />
            </a>
            <a href="https://www.djangoproject.com/" target="_blank">
                <img src="https://skillicons.dev/icons?i=django" />
            </a>
        </nav>
    </section>
    <section id="sch-js">
        <h2>sch-js: JavaScript | (React & Vite)</h2>
        <p><b>sch-js</b> repository stores the project's front-end code which is built using React and Vite, this code manages the user interface components, API requests, display language and more, For more information about the repository visit <a href="https://github.com/rhman-ibrahim/sch-js" target="_blank"><b>sch-js</b></a>.</p>
        <ul>
            <li id="javascript"><b>JavaScript</b> is a high-level, interpreted programming language primarily used for front-end web development. Created by <mark><b>Brendan Eich</b></mark> in <b>1995</b> while he was working at Netscape Communications Corporation.</li>
            <li id="react"><b>React</b> is the library for web and native user interfaces. Build user interfaces out of individual pieces called components written in JavaScript. Created by <mark><b>Jordan Walke</b></mark>, a software engineer at Facebook (Meta), and opend-sourced at JSConf US in <b>May 2013</b>.</li>
            <li id="vite"><b>Vite</b> is a build tool for modern web development, primarily focusing on building web applications using JavaScript frameworks like Vue.js and React. The term "Vite" comes from the French word for "fast," which reflects its main design goal of providing a fast development experience. Created by <mark><b>Evan You</b></mark> and announced in <b>April, 2020</b>.</li>
        </ul>
        <nav>
            <a href="https://ecma-international.org/publications-and-standards/standards/ecma-262/" target="_blank">
                <img src="https://skillicons.dev/icons?i=javascript" />
            </a>
            <a href="https://react.dev/" target="_blank">
                <img src="https://skillicons.dev/icons?i=react" />
            </a>
            <a href="https://vitejs.dev/" target="_blank">
                <img src="https://skillicons.dev/icons?i=vite" />
            </a>
        </nav>
    </section>
    <section id="sch-sh">
        <h2>sch-sh: Bash</h2>
        <p><b>sch-sh</b> repository stores the project's automation scripts which is written using Bash, these scripts automate general tasks sush as migrating, loading fixtures, starting the server and more. For more information about the repository vist <a href="https://github.com/rhman-ibrahim/sch-sh" target="_blank"><b>sch-sh</b></a>.</p>
        <ul id="bash">
            <li><b>Bash</b>, short for "<b>Bourne Again Shell</b>" is a Unix shell and command language for the GNU Project. It is the default shell for most Unix-like operating systems, including Linux distributions and macOS. It allows users to write scripts that automate tasks or perform complex operations. Written by <mark><b>Brian Fox</b></mark> and first released in <b>1989</b>.</li>
        </ul>
        <nav>
            <a href="https://www.gnu.org/software/bash/" target="_blank">
                <img src="https://skillicons.dev/icons?i=bash" />
            </a>
        </nav>
    </section>
    <section id="sch-cf">
        <h2>sch-cf: Configuration Files</h2>
        <p><b>sch-cf</b> repository stores the project's entry point (HTML file) and the configurarion files, these files may have different extensions. For more information about the repository visit <a href="https://github.com/rhman-ibrahim/sch-cf" target="_blank"><b>sch-cf</b></a>. In future this repository will store more advanced configuration files like <b>Docker</b>, <b>AWS: Amazon Web Services</b> and any new tool I will learn and use to automate and develope the <b>Scheme</b> foundation code.</p>
    </section>
</main>
<footer>
    <h2>Final Word</h2>
    <section>
        <p><b>I want to express huge and tremendous respect and admiration for these poeple whom horned this simple file by their names being mentioned here in it, and also those who contributed or worked in shadow to introduce a kind of help.
        <mark>Guido van Rossum: Python</mark>, <mark>Adrian Holovaty: Django</mark>, <mark>Simon Willison: Django</mark>, <mark>Tom Christie: DRF</mark>, <mark>Brendan Eich: JavaScript</mark>, <mark>Jordan Walke: React</mark>, <mark>Evan You: Vite</mark>, <mark>Brian Fox: Bash</mark>; Thank You.<b></p>
    </section>
    <hr/>
    <section>
        <p><b>Finally, I would love to give this file more honor to have tha name of <mark>Linus Torvalds: Linux & Git</mark> mentioned in it, <mark>Linus Benedict Torvalds</mark> is a Finnish software engineer who is the creator and lead developer of the Linux kernel. He also created the distributed version control system Git. Words won't be enough to express the respect you deserve, hope one day to have my name mentioned for doing something which is more than great like you.</b></p>
        <nav>
            <a href="https://www.linux.org/" target="_blank">
                <img src="https://skillicons.dev/icons?i=linux" />
            </a>
            <a href="https://git-scm.com/" target="_blank">
                <img src="https://skillicons.dev/icons?i=git" />
            </a>
        </nav>
    </section>
</footer>