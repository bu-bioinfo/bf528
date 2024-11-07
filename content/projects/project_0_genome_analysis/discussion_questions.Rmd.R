Week 1

3. Answer the following questions in the provided notebook:
  
  a. What is the advantage of using the most up-to-date versions of software? 
  
  b. What are some disadvantages?
  
  3. Take a look at the `nextflow.config` and look for the `profile` section. Answer
the following question in the provided notebook: 
  
  a. What do you think the option `-profile local,conda` is doing?
  
  
week 2




5. Answer the following questions in your provided docs/week2_tasks.Rmd:
  
  a. What does the option `label 'process_single'` specify? Can you find where
this value is described?
  
  b. What would happen if the values in our channel were switched?
  i.e. [path/to/genome, name_of_genome] Would this process still run? Would the
tool still run?
  
  4. Answer the following questions in your provided week2_tasks.Rmd when nextflow
has finished running:
  
  a. Where are the outputs from Prokka stored?
  
  b. You may have noticed a new directory has been created in your repo called
`work/`. What is in this directory? What do you think the advantages of 
generating directories this way are? What are the disadvantages?
  
  
  week 3

1. Navigate to the directory in `work/` where your Prokka process ran successfully. 
Answer the following question in the provided week3_tasks.Rmd:
  
  1. Explain the purpose of each file that you find in this directory. You may
need to look up concepts such as stdout and stderr. 

1. Navigate to your `results/` directory and find the outputs created by Prokka.
Open up the `<replace_with_your_name>.gff` file and answer the following questions:
  
  a. Does this file have a regularized format? How would you parse or read this
file?
  
  b. What information appears to be stored in this file?
  
  :::{.box .task}
In the provided week3_tasks.Rmd, please answer the following questions:
  
  1. How would you change this argparse code to accept a list of file inputs?
  
  2. Why are we going to the trouble of making a separate script and nextflow
module to run this specific code?
  
  :::