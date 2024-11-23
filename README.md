# Markdown to Static Website Generator

## Preliminary notes

* This project is a Proof-Of-Concept, not a production-ready static site generator ! You can take inspiration from it, but it is voluntarily limited. If you want a stable, fast, and powerful Static Site Generator, take a look at [hugo](https://gohugo.io/).

* For example, nested inline elements are not implemented, like in this case:

`This is an *italic and **bold** word*.`

* Also, it doesn't make use of a parsing expression grammar (PEG) like most other modern markdown implementations.

* Finally, take a look at [commonmark](https://commonmark.org/) if you want to see good implementations.

## Overview

This application transforms a directory of Markdown files into a static website by converting the Markdown content into HTML and organizing it into a user-friendly structure. It uses a customizable HTML template for the pages and serves the generated site locally on port `8888`.

### Features

* **Markdown Parsing**: Converts Markdown files into HTML with support for:
  * Headings, paragraphs, and lists.
  * Inline formatting: bold, italic, and code.
  * Links: `[link text](URL)` will be rendered as `<a href="URL">link text</a>`.
  * Images: `![alt text](image URL)` will be rendered as `<img src="image URL" alt="alt text">`.
* **Template Integration**: Inserts the converted Markdown content into a customizable HTML template.
* **Filetree Handling**: Mirrors the directory structure of the `content` folder into the output directory.
* **Static Files**: Copies any static files (CSS, JS, images) in the `static` directory into the `public` folder.
* **Local Server**: Enables easy local preview by serving the generated website at [http://localhost:8888](http://localhost:8888).

---

## Directory Structure Example

Given the following project structure:

```
project/
├── content/
│   ├── index.md
│   ├── about/
│   │   └── team.md
│   └── blog/
│       ├── post1.md
│       └── post2.md
├── static/
│   └── style.css
├── template.html
└── main.sh
```

* **`content/`**: Contains the Markdown files that will be converted to HTML.
* **`static/`**: Holds static files (CSS, JS, images) that are directly copied to the output directory.
* **`template.html`**: The HTML template used for rendering pages. It should include `{{ Title }}` and `{{ Content }}` placeholders.

After running the program, the following structure will be generated:

```
public/
├── index.html
├── about/
│   └── team.html
├── blog/
│   ├── post1.html
│   └── post2.html
└── style.css
```

---

## How to Use

### 1. Prepare Your Project

* Place your Markdown files inside the `content/` directory.
* Add any static files (like CSS or images) into the `static/` directory.
* Create a `template.html` file with placeholders `{{ Title }}` for the page title and `{{ Content }}` for the main content.

### 2. Run the Application

Use the provided `main.sh` script to generate the site and serve it locally:

```bash
./main.sh
```

### 3. View the Generated Website

Open a browser and go to [http://localhost:8888](http://localhost:8888) to preview the website.

---

## Example Workflows

### Simple Example Workflow

#### Input Files

**`content/index.md`**

```markdown
# Welcome to My Website

This is the homepage of my static site. Enjoy browsing!
```

**`template.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ Title }}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header><h1>{{ Title }}</h1></header>
    <main>{{ Content }}</main>
</body>
</html>
```

#### Output

**`public/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to My Website</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header><h1>Welcome to My Website</h1></header>
    <main>
        <p>This is the homepage of my static site. Enjoy browsing!</p>
    </main>
</body>
</html>
```

---

### Example Workflow with Links and Images

#### Input Markdown File

**`content/about/team.md`**

```markdown
# Our Team

We have a dedicated team working on this project. Here's a quick intro:

- [Alice](https://example.com/alice): Lead Developer
- [Bob](https://example.com/bob): Project Manager

Here's a photo of our office:

![Office](https://example.com/office.jpg)
```

#### Output HTML

**`public/about/team.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Our Team</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header><h1>Our Team</h1></header>
    <main>
        <p>We have a dedicated team working on this project. Here's a quick intro:</p>
        <ul>
            <li><a href="https://example.com/alice">Alice</a>: Lead Developer</li>
            <li><a href="https://example.com/bob">Bob</a>: Project Manager</li>
        </ul>
        <p>Here's a photo of our office:</p>
        <img src="https://example.com/office.jpg" alt="Office">
    </main>
</body>
</html>
```

You can now add links and images to your Markdown files, and they will automatically render as HTML links and `<img>` tags in the generated site

---

## Troubleshooting

### Common Issues

1. **Error: Invalid Path**
   * Ensure the `static/`, `content/`, and `template.html` paths exist and are properly structured.

2. **Permission Denied**
   * Ensure the `main.sh` script is executable:

     ```bash
     chmod +x main.sh
     ```

3. **Port Already in Use**
   * Stop any processes using port `8888` or modify `main.sh` to use a different port.
