---
permalink: /
---

# BF591 - R for Biological Sciences

**Under construction**

**Semester: Spring 2022**

**Location: NA**

**Time: NA**

This course introduces the R programming language through the lens of practitioners
in the biological sciences, particularly biology and bioinformatics. Key concepts
and patterns of the language are covered, including:

   * RStudio
   * Data wrangling with tidyverse
   * Data visualization with ggplot
   * Essential biological data shapes and formats
   * Core bioconductor packages
   * Basic data exploration, including elementary statistical modeling and summarization
   * "Toolifying" R scripts
   * Communicating R code and results with RMarkdown
   * Buidling R packages and unit testing strategies
   * Building interactive tools with RShiny

About 1/3 of the materials are drawn from the online textbook [R for Data Science](
https://r4ds.had.co.nz), while the rest has been developed by practicing
bioinformaticians based on their experiences.

Weekly programming assignments will help students apply these techniques to realistic
problems involving analysis and visualization of biological data. Students will be
introduced to a unit testing paradigm that will help them write correct code and
deposit all their code into github for evaluation.

The course materials are aligned with [BF528 Applications in Translational
Bioinformatics](https://bf528.rtfd.io) and are intended to be taken in tandem,
but the materials also stand alone as an independent class.

## Course Schedule

<table>
  <tr>
    <th>Topic #</th>
    <th>Date</th>
    <th>Topic</th>
    <th>Assignment</th>
  </tr>
{% for lec in site.data.schedule %}
  <tr>
    <td>{{ lec.lecnum }}</td>
    <td>{{ lec.date }}</td>
    <td>
      {%- if lec.lecnum != nil -%}
        {% assign page = site.lecture | where:"slug", lec.lecture_slug | first  %}
        <a href="lecture/{{ lec.lecture_slug }}.html">{{ lec.lecture }}</a>
      {%- else -%}
        {{ lec.comment }}
      {%- endif -%}
    </td>
    <td>
      {%- if lec.assignment_slug != nil -%}
        {% assign page = site.assignment | where:"slug", lec.assignment_slug | first %}
        <a href="assignment/{{ lec.assignment_slug }}.html">{{ lec.assignment }}</a>
      {%- endif -%}
    </td>
  </tr>
{% endfor %}
</table>

## Course Values and Policies

**Everyone is welcome.** Every background, race, color, creed, religion, ethnic
origin, age, sex, sexual orientation, gender identity, nationality is welcome
and celebrated in this course. Everyone deserves respect, patience, and
kindness. Disrespectful language, discrimination, or harassment of any kind are
not tolerated, and may result in removal from class or the University. This is
not merely [BU policy](http://www.bu.edu/policies/policy-category/harassment-discrimination/).
The instructors deem these principles to be inviolable human rights. Students
should feel safe reporting any and all instances of discrimination or
harassment to the instructor, to any of the Bioinformatics Program leadership,
or the [BU Equal Opportunity Office](http://www.bu.edu/eoo/).

**Everyone brings value.** Each of us brings unique experiences, skills, and
creativity to this course. Our diversity is our greatest asset.

**Collaboration is highly encouraged.** All students are encouraged to work
together and seek out any and all available resources when completing projects
in all aspects of the course, including sharing coding ideas and strategies with
each other as well as those found on the internet. Any and all available
resources may be brought to bear. However, consistent with BU policy, the bulk
of your code and your final reports should be written in your own words and
represent your own work and understanding of the material. Copying/pasting large
sections of code is not acceptable and will be investigated as cheating (we check).

**A safe space for dissent.** For complex topics such as those covered in this
class, there is seldom one correct answer, approach, or solution. Disagreement
fosters innovation. All in the course, including students and TAs, are
encouraged to express constructive criticism and alternative ideas on any
aspect of the content.

**We are always learning.** Our knowledge and understanding is always
incomplete. Even experts are fallible. The bioinformatics field evolves
rapidly, and Rome was not built in a day. Be kind to yourself and to others.
You are always smarter and more knowledgable today than you were yesterday.

