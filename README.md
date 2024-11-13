# Static site generator from Markdown

This simple program will take Markdown files, convert them into an intermediate
representation, and output them as HTML files.

## Further notes

This project is a POC, not a production-ready static site generator !\
You can take inspiration from it, but it is voluntarily limited.

For example, nested inline elements are not implemented :

**Markdown**\
`This is an *italic and **bold** word*.`

**Render**\
This is an *italic and **bold** word*.
