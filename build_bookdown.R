install.packages('bookdown', repos='http://cran.us.r-project.org')
install.packages('downlit', repos='http://cran.us.r-project.org')

bookdown::render_book("content",
    # css="style.css" is required for <link> tag in HTML index
    # so that custom block styling works
    #output_format=bookdown::html_book(theme="darkly",css="style.css",split_by="section")
    output_format=bookdown::bs4_book(css="style.css",split_by="section")
)
