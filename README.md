# Static site generator from Markdown

This simple program will take Markdown files, convert them into an intermediate
representation, and output them as HTML files.

## Further notes

* This project is a POC, not a production-ready static site generator ! You can take inspiration from it, but it is voluntarily limited. The goal here is to get better at Python, not to write a perfect markdown parser.

* For example, nested inline elements are not implemented, like in this case:

`This is an *italic and **bold** word*.`

* Also, it doesn't make use of a parsing expression grammar (PEG) like most other modern markdown implementations.

* Finally, take a look at [commonmark](https://commonmark.org/) if you want to see good implementations.
