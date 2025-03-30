
#### Course Link - [here](udemy.com/course/complete-guide-in-html-css-build-responsive-website)
---
No Resources found in this course, so typing the notes here.

---
### HTML
---
- Introduction to HTML

    - HTML (Hypertext Markup Language) is the standard markup language for creating web pages.
    - Commonly used tags:
        - `<html>`: The root element of an HTML page.
        - `<head>`: Contains meta-information about the document.
        - `<title>`: Sets the title of the document (shown in the browser's title bar or tab).
        - `<body>`: Contains the content of the document.
        - `<h1>` to `<h6>`: Headings, with `<h1>` being the largest and `<h6>` being the smallest.
        - `<p>`: Paragraph element.
        - `<a href="URL">`: Anchor tag for hyperlinks.
        - `<img src="URL" alt="description">`: Image tag.
        - `<ul>`, `<ol>`, and `<li>`: Unordered and ordered lists.
        - `<div>`: A generic container for grouping elements.
        - `<span>`: A generic inline container for text.
        - `<table>`, `<tr>`, `<td>`: Table elements for creating tables.
        - `<form>`: Used to create forms for user input.
        - `<input>`: Input field for forms.
        - `<button>`: Button element.
        - `<label>`: Label for form elements.
        - `<select>`: Dropdown list.
        - `<option>`: Option in a dropdown list.
        - `<textarea>`: Multi-line text input field.
        - `<iframe>`: Inline frame for embedding another document within the current document.
        - `<script>`: Used to embed JavaScript code.
        - `<link>`: Used to link external resources like CSS files.
        - `<meta>`: Provides metadata about the HTML document.
        - `<style>`: Used to define CSS styles within the HTML document.
        - `<header>`: Represents introductory content or a group of navigational links.
        - `<footer>`: Represents the footer of a section or page.
        - `<nav>`: Represents a section of navigation links.


        - eg:
        
        `<!DOCTYPE html>`: Declares the document type and version of HTML.

        `<html lang="en">`: Sets the language of the document to English.

        `<meta charset="UTF-8">`: Sets the character encoding for the document to UTF-8.
        
        `<meta name="viewport" content="width=device-width, initial-scale=1.0">`: Sets the viewport for responsive design.

        `<link rel="stylesheet" href="styles.css">`: Links an external CSS file.

        `<script src="script.js"></script>`: Links an external JavaScript file.

            
        `<title>Document Title</title>`: Sets the title of the document.

        `<body>`: Contains the content of the document.

        `<h1>Hello World</h1>`: Displays "Hello World" as a heading.

        `<p>This is a paragraph.</p>`: Displays a paragraph of text.

        `<a href="https://www.example.com">Click here</a>`: Creates a hyperlink to "https://www.example.com".

        `<img src="image.jpg" alt="Image description">`: Displays an image with a description.

        `<ul><li>Item 1</li><li>Item 2</li></ul>`: Creates an unordered list with two items.

        `<ol><li>Item 1</li><li>Item 2</li></ol>`: Creates an ordered list with two items.

        `<div class="container">Content</div>`: Creates a div with a class of "container".

        `<span style="color:red;">Red Text</span>`: Displays red text using inline CSS.

        `<table><tr><td>Cell 1</td><td>Cell 2</td></tr></table>`: Creates a table with one row and two cells.


        `<form action="/submit" method="POST"><input type="text" name="name"><button type="submit">Submit</button></form>`: Creates a form with a text input and a submit button.

        `<label for="name">Name:</label><input type="text" id="name" name="name">`: Creates a label for a text input.

        `<select><option value="1">Option 1</option><option value="2">Option 2</option></select>`: Creates a dropdown list with two options.

        `<textarea rows="4" cols="50"></textarea>`: Creates a multi-line text input field.

        `<iframe src="https://www.example.com"></iframe>`: Embeds another document within the current document.

        `<script>alert('Hello, World!');</script>`: Displays an alert box with "Hello, World!".

        `<link rel="stylesheet" href="styles.css">`: Links an external CSS file.

        `<meta name="description" content="This is a sample HTML document.">`: Provides metadata about the document.

        `<style>body { background-color: lightblue; }</style>`: Defines CSS styles within the HTML document.

        `<header><h1>Header Content</h1></header>`: Represents the header of the document.

        `<footer><p>Footer Content</p></footer>`: Represents the footer of the document.

        `<nav><ul><li><a href="#home">Home</a></li><li><a href="#about">About</a></li></ul></nav>`: Represents navigation links.
        `<article><h2>Article Title</h2><p>Article content.</p></article>`: Represents an independent piece of content.

        `<section><h2>Section Title</h2><p>Section content.</p></section>`: Represents a thematic grouping of content.

        `<aside><p>Related content or sidebar.</p></aside>`: Represents content related to the main content.

        `<main><h1>Main Content</h1></main>`: Represents the main content of the document.

        `<figure><img src="image.jpg" alt="Image description"><figcaption>Image caption.</figcaption></figure>`: Represents self-contained content, like an image with a caption.

        `<time datetime="2023-10-01">October 1, 2023</time>`: Represents a specific time or date.

        `<mark>Highlighted text</mark>`: Represents highlighted text.

        `<progress value="50" max="100"></progress>`: Represents a progress bar.

        `<meter value="0.5" min="0" max="1"></meter>`: Represents a scalar measurement within a known range.

        `<details><summary>More Info</summary><p>Additional information.</p></details>`: Represents additional details that can be shown or hidden.

        `<summary>Summary of details</summary>`: Represents a summary for the details element.

        `<dialog open>Dialog content</dialog>`: Represents a dialog box or popup.

        `<canvas id="myCanvas" width="200" height="100"></canvas>`: Represents a drawable region in HTML.

        `<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red"/></svg>`: Represents Scalable Vector Graphics.

        `<link rel="icon" href="favicon.ico">`: Links a favicon for the document.

        `<base href="https://www.example.com/">`: Sets a base URL for relative URLs in the document.

        `<noscript>This is displayed if JavaScript is disabled.</noscript>`: Provides alternative content for users with JavaScript disabled.

        `<address>Contact information</address>`: Represents contact information for the author or owner of the document.

        `<bdi>Text that should not be formatted</bdi>`: Represents text that should not be affected by surrounding text formatting.

        `<bdo dir="rtl">Right-to-left text</bdo>`: Represents text direction override.

        `<wbr>`: Suggests an optional line break opportunity.
        `<abbr title="Abbreviation">Abbr</abbr>`: Represents an abbreviation or acronym.

        `<cite>Title of a work</cite>`: Represents the title of a creative work.

        `<dfn>Definition term</dfn>`: Represents a term being defined.

        `<kbd>Keyboard input</kbd>`: Represents user input via keyboard.

        `<samp>Sample output</samp>`: Represents sample output from a computer program.

        `<var>Variable name</var>`: Represents a variable in programming or mathematical expressions.

        `<time datetime="2023-10-01">October 1, 2023</time>`: Represents a specific time or date.

        `<small>Small print</small>`: Represents small print or fine print.

        `<strong>Strong importance</strong>`: Represents strong importance or emphasis.

        `<em>Emphasized text</em>`: Represents emphasized text.

        `<del datetime="2023-10-01">Deleted text</del>`: Represents deleted text with a date.

        `<ins datetime="2023-10-01">Inserted text</ins>`: Represents inserted text with a date.

        `<sub>Subscript text</sub>`: Represents subscript text.

        `<sup>Superscript text</sup>`: Represents superscript text.

        `<b>Bold text</b>`: Represents bold text.

        `<i>Italic text</i>`: Represents italic text.

        `<u>Underlined text</u>`: Represents underlined text.

        `<s>Strikethrough text</s>`: Represents strikethrough text.

        `<q cite="https://www.example.com">Quoted text</q>`: Represents a short inline quotation.

        `<blockquote cite="https://www.example.com"><p>Blockquote content</p></blockquote>`: Represents a block of quoted content.

        `<code>Code snippet</code>`: Represents a fragment of computer code.

        `<pre><code>Preformatted code</code></pre>`: Represents preformatted code with whitespace preserved.

        `<bdi>Bidirectional isolation</bdi>`: Represents bidirectional isolation for text.

        `<bdo dir="rtl">Bidirectional override</bdo>`: Represents bidirectional override for text direction.

        `<ruby><rb>Ruby base</rb><rp>(</rp><rt>Ruby annotation</rt><rp>)</rp></ruby>`: Represents ruby annotations for East Asian typography.

        `<rt>Ruby text</rt>`: Represents ruby text for annotations.

        `<rp>(</rp><rt>Ruby parenthesis</rt><rp>)</rp>`: Represents parentheses for ruby annotations.

        `<bdi dir="ltr">Bidirectional isolation with left-to-right direction</bdi>`: Represents bidirectional isolation with left-to-right direction.

        `<bdo dir="ltr">Bidirectional override with left-to-right direction</bdo>`: Represents bidirectional override with left-to-right direction.

        `<wbr>Word break opportunity</wbr>`: Represents a word break opportunity.

        `<s>Strikethrough text</s>`: Represents strikethrough text.

        `<mark>Highlighted text</mark>`: Represents highlighted text.

        `<progress value="50" max="100"></progress>`: Represents a progress bar.

        `<meter value="0.5" min="0" max="1"></meter>`: Represents a scalar measurement within a known range.

        `<details><summary>More Info</summary><p>Additional information.</p></details>`: Represents additional details that can be shown or hidden.

        `<summary>Summary of details</summary>`: Represents a summary for the details element.

        `<dialog open>Dialog content</dialog>`: Represents a dialog box or popup.

        `<canvas id="myCanvas" width="200" height="100"></canvas>`: Represents a drawable region in HTML.

        `<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red"/></svg>`: Represents Scalable Vector Graphics.

        `<link rel="icon" href="favicon.ico">`: Links a favicon for the document.

        `<base href="https://www.example.com/">`: Sets a base URL for relative URLs in the document.

        `<noscript>This is displayed if JavaScript is disabled.</noscript>`: Provides alternative content for users with JavaScript disabled.

        `<address>Contact information</address>`: Represents contact information for the author or owner of the document.

- Tags and Attributes

    - Tags are the building blocks of HTML. They are used to create elements on a web page.
    - Attributes provide additional information about an element. They are always specified in the opening tag and come in name/value pairs like `name="value"`.
    - Common attributes include `id`, `class`, `style`, `src`, `href`, and `alt`.
    - Tags vs Elements:
        - A tag is the markup that defines the start and end of an element. An element consists of the opening tag, content, and closing tag.
        - Example:
            ```
            <p>This is a paragraph.</p>
            ```
            - In this example, `<p>` is the opening tag, `This is a paragraph.` is the content, and `</p>` is the closing tag.
            - The entire structure is the `<p>` element.
            - Tags can be self-closing, like `<img src="image.jpg" alt="Description of the image" />`, which does not require a closing tag.
            - In this case, the `<img>` tag is self-closing and does not have a separate closing tag.
            - Self-closing tags are often used for elements that do not have any content, such as images or line breaks.
            - Example:
                ```
                <br /> <!-- Line break -->
                <hr /> <!-- Horizontal rule -->
                <img src="image.jpg" alt="Description of the image" />
                ```
                - In this example, `<br />` creates a line break, `<hr />` creates a horizontal line, and `<img />` displays an image.
                - All of these tags are self-closing and do not require a separate closing tag.

    - Example:
        ```
        <img src="image.jpg" alt="Description of the image" class="image-class" id="image-id">
        ```
        - In this example, `src` specifies the source of the image, `alt` provides alternative text for the image, `class` assigns a class to the image, and `id` assigns a unique identifier to the image.

        - The `class` attribute can be used to apply CSS styles to multiple elements, while the `id` attribute is unique and can be used to target a specific element with CSS or JavaScript.

        - The `style` attribute allows you to apply inline CSS styles directly to an element, but it's generally better practice to use external CSS files for styling.

        - Example:
            ```
            <div class="container" id="main-container" style="background-color: lightblue;">
                <h1>Welcome to My Website</h1>
                <p>This is a sample paragraph.</p>
            </div>
            ```
            - In this example, the `div` element has a class of "container", an id of "main-container", and an inline style that sets the background color to light blue.
            - The `h1` element contains a heading, and the `p` element contains a paragraph of text.

- Style

    
    - CSS (Cascading Style Sheets) is used to style HTML elements. It allows you to control the layout, colors, fonts, and other visual aspects of a web page.
    - CSS can be applied in three ways:
        - Inline CSS: Using the `style` attribute within an HTML element.
        - Internal CSS: Using a `<style>` tag within the `<head>` section of an HTML document.
        - External CSS: Linking to an external CSS file using the `<link>` tag.

        - Example:
            ```
            <head>
                <link rel="stylesheet" href="styles.css">
            </head>
            ```
            - In this example, the `<link>` tag links to an external CSS file named "styles.css".
            - The `rel` attribute specifies the relationship between the current document and the linked document, and `href` specifies the URL of the linked document.

            - The `type` attribute specifies the type of the linked document, which is "text/css" for CSS files.

            - The `media` attribute specifies the media type for which the CSS file is intended, such as "screen" or "print".

            - example:
                ```
                <link rel="stylesheet" type="text/css" href="styles.css" media="screen">
                ```
                - In this example, the `media` attribute specifies that the CSS file is intended for screen display.

- Text Formatting

    
        - HTML provides various tags for formatting text, including:
            - `<strong>`: Represents strong importance or emphasis.
            - `<em>`: Represents emphasized text.
            - `<b>`: Represents bold text.
            - `<i>`: Represents italic text.
            - `<u>`: Represents underlined text.
            - `<s>`: Represents strikethrough text.
            - `<mark>`: Represents highlighted text.
            - `<small>`: Represents small print or fine print.
            - `<sub>`: Represents subscript text.
            - `<sup>`: Represents superscript text.
    
        - Example:
            ```
            <p>This is <strong>strong</strong> and <em>emphasized</em> text.</p>
            ```
            - In this example, the `<strong>` tag makes the text "strong" bold and the `<em>` tag makes the text "emphasized" italic.

- Comments

    - HTML comments are used to insert notes or explanations in the code that are not displayed in the browser.
    - Comments are enclosed within `<!--` and `-->` tags.
    - Example:
        ```
        <!-- This is a comment -->
        <p>This is a paragraph.</p>
        ```
        - In this example, the comment "This is a comment" will not be displayed in the browser, but it can be seen in the HTML source code.
        - Comments are useful for documenting code, explaining complex sections, or temporarily disabling code without deleting it.
        - Example:
            ```
            <!-- This is a comment -->
            <p>This is a paragraph.</p>
            <!-- <p>This paragraph is commented out and will not be displayed.</p> -->
            ```
            - In this example, the second paragraph is commented out and will not be displayed in the browser.
            - Comments can also be used to provide information about the purpose of a section of code or to leave reminders for future developers.

- Colors

    - HTML supports various color formats, including:
        - Named colors: e.g., "red", "blue", "green".
        - Hexadecimal colors: e.g., `#FF0000` for red.
        - RGB colors: e.g., `rgb(255, 0, 0)` for red.
        - RGBA colors: e.g., `rgba(255, 0, 0, 0.5)` for red with 50% opacity.
        - HSL colors: e.g., `hsl(0, 100%, 50%)` for red.
        - HSLA colors: e.g., `hsla(0, 100%, 50%, 0.5)` for red with 50% opacity.

    - Example:
        ```
        <p style="color: red;">This text is red.</p>
        <p style="color: #FF0000;">This text is also red.</p>
        <p style="color: rgb(255, 0, 0);">This text is also red.</p>
        ```
        - In this example, all three paragraphs will display the text in red using different color formats.

    - background color:
        ```
        <div style="background-color: lightblue;">This div has a light blue background.</div>
        ```
        - In this example, the `div` element has a light blue background color.
        - The `background-color` property is used to set the background color of the element.

        - The `background-color` property can accept various color formats, including named colors, hexadecimal colors, RGB colors, RGBA colors, HSL colors, and HSLA colors.

        - Example:
            ```
            <div style="background-color: #FF0000;">This div has a red background.</div>
            <div style="background-color: rgb(255, 0, 0);">This div has a red background.</div>
            <div style="background-color: rgba(255, 0, 0, 0.5);">This div has a red background with 50% opacity.</div>
            ```
            - In this example, the first two `div` elements have a red background using different color formats, and the third `div` has a red background with 50% opacity.
            - The `rgba` format allows you to specify the red, green, and blue values along with an alpha value for opacity. 

    - border 

        ```
        <div style="border: 2px solid black;">This div has a black border.</div>
        ```
        - In this example, the `div` element has a black border with a width of 2 pixels and a solid line style.
        - The `border` property is a shorthand property that combines the `border-width`, `border-style`, and `border-color` properties.

        - Example:
            ```
            <div style="border: 2px solid red;">This div has a red border.</div>
            <div style="border: 1px dashed blue;">This div has a blue dashed border.</div>
            <div style="border: 3px dotted green;">This div has a green dotted border.</div>
            ```
            - In this example, the first `div` has a red solid border, the second `div` has a blue dashed border, and the third `div` has a green dotted border.
            - The `border-style` property can accept various values, including `solid`, `dashed`, `dotted`, `double`, `groove`, `ridge`, `inset`, and `outset`.

- Images

    - Images can be added to HTML documents using the `<img>` tag.
    - The `src` attribute specifies the source of the image, and the `alt` attribute provides alternative text for the image.
    - Example:
        ```
        <img src="image.jpg" alt="Description of the image">
        ```
        - In this example, the `img` tag displays an image located at "image.jpg" with a description of "Description of the image".
        - The `alt` attribute is important for accessibility and SEO, as it provides a text alternative for users who cannot see the image.

    - Image Formats:
        - Common image formats include JPEG, PNG, GIF, SVG, and WebP.
        - JPEG is commonly used for photographs and images with many colors.
        - PNG is used for images with transparency and lossless compression.
        - GIF is used for animated images and simple graphics.
        - SVG is used for vector graphics and can be scaled without losing quality.
        - WebP is a modern image format that provides both lossy and lossless compression.

    - Example:
        ```
        <img src="image.jpg" alt="Description of the image" width="300" height="200">
        ```
        - In this example, the `img` tag displays an image with a width of 300 pixels and a height of 200 pixels.

- Favicons

    - A favicon (short for "favorite icon") is a small icon that represents a website and is displayed in the browser's address bar, tab, or bookmark list.
    - Favicons are typically 16x16 pixels or 32x32 pixels in size and can be in various formats, including ICO, PNG, and SVG.
    - To add a favicon to an HTML document, use the `<link>` tag in the `<head>` section of the document.
    - Example:
        ```
        <link rel="icon" href="favicon.ico" type="image/x-icon">
        ```
        - In this example, the `link` tag links to a favicon file named "favicon.ico".
        - The `rel` attribute specifies the relationship between the current document and the linked document, and `type` specifies the MIME type of the linked document.

    - Example:
        ```
        <link rel="icon" href="favicon.png" type="image/png">
        ```
        - In this example, the `link` tag links to a PNG favicon file named "favicon.png".

    - Example:
        ```
        <link rel="icon" href="favicon.svg" type="image/svg+xml">
        ```
        - In this example, the `link` tag links to an SVG favicon file named "favicon.svg".

- Page Title

    - The page title is set using the `<title>` tag within the `<head>` section of an HTML document.
    - The title is displayed in the browser's title bar or tab and is important for SEO and user experience.
    - Example:
        ```
        <head>
            <title>My Web Page</title>
        </head>
        ```
        - In this example, the title of the web page is set to "My Web Page".
        - The title should be descriptive and relevant to the content of the page.

    - Example:
        ```
        <head>
            <title>Welcome to My Website</title>
        </head>
        ```
        - In this example, the title of the web page is set to "Welcome to My Website".

    - Example:
        ```
        <head>
            <title>Contact Us</title>
        </head> 
        ```
        - In this example, the title of the web page is set to "Contact Us".

- Tables

    - Tables are created using the `<table>` tag, and they consist of rows (`<tr>`) and cells (`<td>` for data cells and `<th>` for header cells).
    - Example:
        ```
        <table>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
            </tr>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </table>
        ```
        - In this example, a table is created with two header cells and one row of data.
        - The `<th>` tag is used for header cells, which are typically bold and centered by default.
        - The `<td>` tag is used for data cells, which contain the actual content of the table.

- Input attributes

    - HTML forms are created using the `<form>` tag, and they can contain various input elements like text fields, checkboxes, radio buttons, and buttons.
    - Example:
        ```
        <form action="/submit" method="POST">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
            <input type="submit" value="Submit">
        </form>
        ```
        - In this example, a form is created with a text input field for the user's name and a submit button.
        - The `action` attribute specifies the URL to which the form data will be submitted, and the `method` attribute specifies the HTTP method (GET or POST) used to send the data.
        - The `required` attribute indicates that the input field must be filled out before submitting the form.

    - Example:
        ```
        <form action="/submit" method="POST">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            <input type="submit" value="Submit">
        </form>
        ```
        - In this example, a form is created with an email input field for the user's email address and a submit button.

- Input Form Attributes

    - HTML input elements can have various attributes to control their behavior and appearance.
    - Common input attributes include:
        - `type`: Specifies the type of input (e.g., text, email, password, checkbox, radio, file, etc.).
        - `name`: Specifies the name of the input element, which is used to identify the data when the form is submitted.
        - `id`: Specifies a unique identifier for the input element.
        - `value`: Specifies the default value of the input element.
        - `placeholder`: Provides a short hint or description of the expected input.
        - `required`: Indicates that the input field must be filled out before submitting the form.
        - `disabled`: Disables the input field, preventing user interaction.
        - `readonly`: Makes the input field read-only, preventing user modification.
        - `maxlength`: Specifies the maximum number of characters allowed in a text input field.
        - `min` and `max`: Specify the minimum and maximum values for numeric inputs.
        - `pattern`: Specifies a regular expression that the input value must match.
        - `novalidate`: Prevents the browser from performing validation on the form when submitted.
        - `enctype`: Specifies the encoding type for form data when submitting to a server.
        - `accept`: Specifies the types of files that can be uploaded in a file input field.
        - `multiple`: Allows multiple files to be selected in a file input field.
        - `autofocus`: Automatically focuses on the input field when the page loads.
        - Example for input form attribute

            ```
            <form action="/submit" method="POST" enctype="multipart/form-data">
                <label for="file">Upload File:</label>
                <input type="file" id="file" name="file" required>
                <input type="submit" value="Upload">
            </form>
            ```
            - In this example, a form is created with a file input field for uploading files and a submit button.
            - The `enctype` attribute specifies the encoding type for the form data, which is set to "multipart/form-data" for file uploads.


- Canvas

    - The `<canvas>` element is used to draw graphics on a web page using JavaScript.
    - It provides a drawable region defined in HTML, and you can use JavaScript to manipulate the canvas and create shapes, images, and animations.
    - Example:
        ```
        <canvas id="myCanvas" width="200" height="100"></canvas>
        <script>
            var canvas = document.getElementById("myCanvas");
            var ctx = canvas.getContext("2d");
            ctx.fillStyle = "red";
            ctx.fillRect(20, 20, 150, 50);
        </script>
        ```
        - In this example, a canvas element is created with a width of 200 pixels and a height of 100 pixels.
        - The JavaScript code retrieves the canvas element and its 2D rendering context, sets the fill color to red, and draws a filled rectangle on the canvas.

    - Example:
        ```
        <canvas id="myCanvas" width="400" height="400"></canvas>
        <script>
            var canvas = document.getElementById("myCanvas");
            var ctx = canvas.getContext("2d");
            ctx.fillStyle = "blue";
            ctx.fillRect(50, 50, 300, 300);

            ctx.strokeStyle = "black";
            ctx.lineWidth = 5;
            ctx.strokeRect(50, 50, 300, 300);

            ctx.fillStyle = "white";
            ctx.font = "30px Arial";
            ctx.fillText("Hello, Canvas!", 100, 200);
        </script>                           

        ```
        - In this example, a canvas element is created with a width and height of 400 pixels.

        - The JavaScript code retrieves the canvas element and its 2D rendering context, sets the fill color to blue, and draws a filled rectangle on the canvas.

- Add Video

    - The `<video>` element is used to embed video content in a web page.
    - It supports various video formats, including MP4, WebM, and Ogg.
    - Example:
        ```
        <video width="320" height="240" controls>
            <source src="movie.mp4" type="video/mp4">
            <source src="movie.ogg" type="video/ogg">
            Your browser does not support the video tag.
        </video>
        ```
        - In this example, a video element is created with a width of 320 pixels and a height of 240 pixels.
        - The `controls` attribute adds playback controls (play, pause, volume) to the video player.
        - The `<source>` tags specify the video files and their formats. If the browser does not support the specified format, it will try the next source.

    - Example:
        ```
        <video width="640" height="360" controls autoplay loop muted>
            <source src="video.mp4" type="video/mp4">
            <source src="video.webm" type="video/webm">
            Your browser does not support the video tag.
        </video>
        ```

        - In this example, a video element is created with a width of 640 pixels and a height of 360 pixels.

        - The `autoplay` attribute makes the video start playing automatically when the page loads.

        - The `loop` attribute makes the video loop continuously.

        - The `muted` attribute mutes the audio of the video.

        - The `<source>` tags specify the video files and their formats. If the browser does not support the specified format, it will try the next source.
        - The text "Your browser does not support the video tag." will be displayed if the browser does not support the `<video>` element.

        - Example:
            ```
            <video width="640" height="360" controls poster="poster.jpg">
                <source src="video.mp4" type="video/mp4">
                <source src="video.webm" type="video/webm">
                Your browser does not support the video tag.
            </video>
            ```
            - In this example, a video element is created with a width of 640 pixels and a height of 360 pixels.

            - The `poster` attribute specifies an image to be displayed while the video is loading or before the user clicks play.

            - The `<source>` tags specify the video files and their formats. If the browser does not support the specified format, it will try the next source.
            - The text "Your browser does not support the video tag." will be displayed if the browser does not support the `<video>` element.

            - The `controls` attribute adds playback controls (play, pause, volume) to the video player.

            - The `autoplay` attribute makes the video start playing automatically when the page loads.
            - The `loop` attribute makes the video loop continuously.

- Add Audio

    - The `<audio>` element is used to embed audio content in a web page.
    - It supports various audio formats, including MP3, Ogg, and WAV.
    - Example:
        ```
        <audio controls>
            <source src="audio.mp3" type="audio/mpeg">
            <source src="audio.ogg" type="audio/ogg">
            Your browser does not support the audio tag.
        </audio>
        ```
        - In this example, an audio element is created with playback controls (play, pause, volume).
        - The `<source>` tags specify the audio files and their formats. If the browser does not support the specified format, it will try the next source.

    - Example:
        ```
        <audio controls autoplay loop muted>
            <source src="audio.mp3" type="audio/mpeg">
            <source src="audio.ogg" type="audio/ogg">
            Your browser does not support the audio tag.
        </audio>
        ```
        - In this example, an audio element is created with playback controls (play, pause, volume).

- SVG

    - SVG (Scalable Vector Graphics) is an XML-based format for vector graphics.
    - It allows you to create and manipulate graphics using HTML and CSS.
    - Example:
        ```
        <svg width="100" height="100">
            <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
        </svg>
        ```
        - In this example, an SVG element is created with a width and height of 100 pixels.
        - A circle is drawn with a center at (50, 50), a radius of 40 pixels, a black stroke, and a red fill.

    - Example:
        ```
        <svg width="200" height="200">
            <rect x="10" y="10" width="100" height="100" fill="blue" />
            <circle cx="150" cy="150" r="40" fill="green" />
            <text x="50" y="50" font-family="Verdana" font-size="20" fill="white">Hello SVG</text>
        </svg>
        ```
        - In this example, an SVG element is created with a width and height of 200 pixels.

        - A blue rectangle is drawn at (10, 10) with a width and height of 100 pixels.

        - A green circle is drawn with a center at (150, 150) and a radius of 40 pixels.

        - A text element is added at (50, 50) with the text "Hello SVG", using the Verdana font, a font size of 20 pixels, and white fill color.

        - SVG graphics are scalable, meaning they can be resized without losing quality, making them ideal for responsive web design.

- Classes

    - Classes are used to group elements and apply styles to them using CSS.
    - The `class` attribute is used to assign a class name to an HTML element.
    - Example:
        ```
        <div class="container">
            <h1 class="header">Welcome to My Website</h1>
            <p class="paragraph">This is a sample paragraph.</p>
        </div>
        ```
        - In this example, the `div` element has a class of "container", the `h1` element has a class of "header", and the `p` element has a class of "paragraph".
        - CSS styles can be applied to these classes in an external stylesheet or within a `<style>` tag in the HTML document.

    - Example:
        ```
        <style>
            .container {
                background-color: lightblue;
                padding: 20px;
            }
            .header {
                color: darkblue;
                font-size: 24px;
            }
            .paragraph {
                color: black;
                font-size: 16px;
            }
        </style>
        ```
        - In this example, CSS styles are defined for the "container", "header", and "paragraph" classes.
        - The "container" class has a light blue background and padding of 20 pixels.

        - The "header" class has dark blue text color and a font size of 24 pixels.
        - The "paragraph" class has black text color and a font size of 16 pixels.

        - These styles will be applied to the corresponding elements in the HTML document.

- Lists

    - HTML provides various types of lists to organize content, including:
        - Unordered lists (`<ul>`): Used for items that do not have a specific order.
        - Ordered lists (`<ol>`): Used for items that have a specific order.
        - Definition lists (`<dl>`): Used for terms and their definitions.

    - Example of an unordered list:
        ```
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
            <li>Item 3</li>
        </ul>
        ```
        - In this example, an unordered list is created with three list items.

    - Example of an ordered list:
        ```
        <ol>
            <li>First item</li>
            <li>Second item</li>
            <li>Third item</li>
        </ol>
        ```
        - In this example, an ordered list is created with three list items.

    - Example of a definition list:
        ```
        <dl>
            <dt>Term 1</dt>
            <dd>Definition of term 1.</dd>
            <dt>Term 2</dt>
            <dd>Definition of term 2.</dd>
        </dl>
        ```
        - In this example, a definition list is created with two terms and their definitions.

        - The `<dt>` tag is used for the term, and the `<dd>` tag is used for the definition.
        - The terms and definitions are grouped together, making it easy to read and understand.

- iframes

    - The `<iframe>` element is used to embed another HTML document within the current document.
    - It allows you to display content from other sources, such as videos, maps, or other web pages.
    - Example:
        ```
        <iframe src="https://www.example.com" width="600" height="400"></iframe>
        ```
        - In this example, an iframe is created with a source URL of "https://www.example.com" and a width of 600 pixels and a height of 400 pixels.

    - Example:
        ```
        <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" width="560" height="315" frameborder="0" allowfullscreen></iframe>
        ```
        - In this example, an iframe is created to embed a YouTube video with a width of 560 pixels and a height of 315 pixels.
        - The `frameborder` attribute specifies whether to display a border around the iframe (0 for no border, 1 for a border).

        - The `allowfullscreen` attribute allows the video to be viewed in fullscreen mode.

        - The `src` attribute specifies the URL of the embedded content.

        - The `width` and `height` attributes specify the dimensions of the iframe.

- File Paths

    - File paths are used to specify the location of files on a web server or local file system.
    - There are two types of file paths:
        - Absolute paths: Specify the full URL to the file, including the protocol (e.g., `http://`, `https://`).
        - Relative paths: Specify the path to the file relative to the current document.

    - Example of an absolute path:
        ```
        <img src="https://www.example.com/images/image.jpg" alt="Image">
        ```
        - In this example, an image is displayed using an absolute URL.

    - Example of a relative path:
        ```
        <img src="images/image.jpg" alt="Image">
        ```
        - In this example, an image is displayed using a relative path to the "images" folder in the same directory as the HTML document.

    - Example of a relative path with parent directory:
        ```
        <img src="../images/image.jpg" alt="Image">
        ```
        - In this example, an image is displayed using a relative path that goes up one directory level to access the "images" folder.

    - Example of a relative path with current directory:
        ```
        <img src="./images/image.jpg" alt="Image">
        ```
        - In this example, an image is displayed using a relative path that specifies the current directory with "./".

        - The `./` indicates the current directory, while `../` indicates the parent directory.
        - Relative paths are useful for organizing files within a project and making it easier to move the project to different locations without breaking links.

- Layout

    - HTML provides various layout elements to structure content on a web page.
    - Common layout elements include:
        - `<div>`: A generic container for grouping elements and applying styles.
        - `<header>`: Represents the header section of a document or section.
        - `<nav>`: Represents navigation links.
        - `<main>`: Represents the main content of a document.
        - `<section>`: Represents a thematic grouping of content.
        - `<article>`: Represents a self-contained piece of content.
        - `<aside>`: Represents content that is tangentially related to the main content.
        - `<footer>`: Represents the footer section of a document or section.

    - Example:
        ```
        <header>
            <h1>My Website</h1>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>
        ```
        - In this example, a header section is created with a title and navigation links.

    - Example:
        ```
        <main>
            <section id="home">
                <h2>Welcome to My Website</h2>
                <p>This is the home section.</p>
            </section>
            <section id="about">
                <h2>About Me</h2>
                <p>This is the about section.</p>
            </section>
            <section id="contact">
                <h2>Contact Me</h2>
                <p>This is the contact section.</p>
            </section>
        </main>
        ```

        - In this example, a main section is created with three subsections: home, about, and contact.
        - Each section has a heading and a paragraph of text.
        - The `id` attribute is used to create anchors for linking to specific sections of the page.

        - The `id` attribute allows you to create unique identifiers for each section, making it easy to link to them from the navigation menu or other parts of the page.
        - Example:
            ```
            <aside>
                <h3>Related Links</h3>
                <ul>
                    <li><a href="#link1">Link 1</a></li>
                    <li><a href="#link2">Link 2</a></li>
                </ul>
            </aside>
            ```
            - In this example, an aside section is created with related links.
            - The aside section is typically used for content that is tangentially related to the main content.

- Semantics

    - HTML5 introduced semantic elements that provide meaning to the content and improve accessibility and SEO.
    - Semantic elements include:
        - `<header>`: Represents the header section of a document or section.
        - `<nav>`: Represents navigation links.
        - `<main>`: Represents the main content of a document.
        - `<section>`: Represents a thematic grouping of content.
        - `<article>`: Represents a self-contained piece of content.
        - `<aside>`: Represents content that is tangentially related to the main content.
        - `<footer>`: Represents the footer section of a document or section.

    - Example:
        ```
        <article>
            <h2>My First Article</h2>
            <p>This is the content of my first article.</p>
            <footer>
                <p>Published on: January 1, 2023</p>
            </footer>
        </article>
        ```
        - In this example, an article element is created with a heading, content, and a footer with publication information.

    - Example:
        ```
        <section>
            <h2>About Me</h2>
            <p>This is the about me section.</p>
        </section>
        ```
        - In this example, a section element is created with a heading and content.

        - The section element is used to group related content together, making it easier to understand the structure of the document.

        - The semantic elements improve the readability of the HTML code and provide better context for search engines and assistive technologies.
        - Example:
            ```
            <footer>
                <p>&copy; 2023 My Website</p>
            </footer>
            ```
            - In this example, a footer element is created with copyright information.
            - The footer element typically contains information about the document, such as copyright, contact information, or links to related content.

            - The footer element is usually placed at the bottom of the page or section.


- Forms

    - HTML forms are used to collect user input and submit data to a server.
    - Forms are created using the `<form>` tag, and they can contain various input elements like text fields, checkboxes, radio buttons, and buttons.
    - Example:
        ```
        <form action="/submit" method="POST">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
            <input type="submit" value="Submit">
        </form>
        ```
        - In this example, a form is created with a text input field for the user's name and a submit button.
        - The `action` attribute specifies the URL to which the form data will be submitted, and the `method` attribute specifies the HTTP method (GET or POST) used to send the data.
        - The `required` attribute indicates that the input field must be filled out before submitting the form.

    - Example:
        ```
        <form action="/submit" method="POST">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            <input type="submit" value="Submit">
        </form>
        ```
        - In this example, a form is created with an email input field for the user's email address and a submit button.


- Form Attributes

    - HTML input elements can have various attributes to control their behavior and appearance.
    - Common input attributes include:
        - `type`: Specifies the type of input (e.g., text, email, password, checkbox, radio, file, etc.).
        - `name`: Specifies the name of the input element, which is used to identify the data when the form is submitted.
        - `id`: Specifies a unique identifier for the input element.
        - `value`: Specifies the default value of the input element.
        - `placeholder`: Provides a short hint or description of the expected input.
        - `required`: Indicates that the input field must be filled out before submitting the form.
        - `disabled`: Disables the input field, preventing user interaction.
        - `readonly`: Makes the input field read-only, preventing user modification.
        - `maxlength`: Specifies the maximum number of characters allowed in a text input field.
        - `min` and `max`: Specify the minimum and maximum values for numeric inputs.
        - `pattern`: Specifies a regular expression that the input value must match.
        - `novalidate`: Prevents the browser from performing validation on the form when submitted.
        - `enctype`: Specifies the encoding type for form data when submitting to a server.
        - `accept`: Specifies the types of files that can be uploaded in a file input field.
        - `multiple`: Allows multiple files to be selected in a file input field.
        - `autofocus`: Automatically focuses on the input field when the page loads.
        - `reset` : Resets the form to its initial state.

- Input Type

    - HTML provides various input types to create different types of input fields in forms.
    - Common input types include:
        - `text`: A single-line text input field.
        - `email`: An input field for email addresses, with built-in validation.
        - `password`: A password input field that hides the entered characters.
        - `checkbox`: A checkbox input for selecting options.
        - `radio`: A radio button input for selecting one option from a group.
        - `file`: An input field for uploading files.
        - `number`: An input field for numeric values, with built-in validation for min and max values.
        - `date`: An input field for selecting dates, with a date picker in supported browsers.
        - `color`: An input field for selecting colors, with a color picker in supported browsers.

    - Example:
        ```
        <form action="/submit" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <input type="submit" value="Submit">
        </form>
        ```
        - In this example, a form is created with a text input field for the user's username and a submit button.

    - Example:
        ```
        <form action="/submit" method="POST">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            <input type="submit" value="Submit">
        </form>
        ``` 

---
CSS
---

- Introduction to CSS

    - CSS (Cascading Style Sheets) is a stylesheet language used to describe the presentation of a document written in HTML or XML.
    - CSS controls the layout, colors, fonts, and overall appearance of web pages.
    - CSS allows you to separate content from presentation, making it easier to maintain and update styles across multiple pages.

    - Example

        ```
        <style>
            body {
                background-color: lightblue;
                font-family: Arial, sans-serif;
            }
            h1 {
                color: darkblue;
                text-align: center;
            }
            p {
                color: black;
                font-size: 16px;
            }
        </style>
        ```
        - In this example, CSS styles are defined for the `body`, `h1`, and `p` elements.
        - The `body` element has a light blue background color and uses the Arial font.
        - The `h1` element has dark blue text color and is centered on the page.
        - The `p` element has black text color and a font size of 16 pixels.


        - To use this style.css file in html file:
            ```
            <link rel="stylesheet" type="text/css" href="style.css">
            ```

- Selectors

    - CSS selectors are used to select and apply styles to HTML elements.
    - Common types of selectors include:
        - Type selector: Selects elements by their tag name (e.g., `h1`, `p`, `div`).
        - Class selector: Selects elements by their class attribute (e.g., `.class-name`).
        - ID selector: Selects elements by their id attribute (e.g., `#id-name`).
        - Descendant selector: Selects elements that are descendants of a specified element (e.g., `div p` selects all `p` elements inside a `div`).
        - Attribute selector: Selects elements based on their attributes (e.g., `[type="text"]` selects all input elements with type "text").
        - Pseudo-class selector: Selects elements based on their state or position (e.g., `a:hover` selects links when hovered over).
        - Pseudo-element selector: Selects a specific part of an element (e.g., `::before`, `::after`).

    - Example:
        ```
        <style>
            h1 {
                color: blue;
            }
            .class-name {
                font-size: 20px;
            }
            #id-name {
                background-color: yellow;
            }
            div p {
                color: green;
            }
            input[type="text"] {
                border: 1px solid black;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
        ```
        - In this example, various selectors are used to apply styles to different elements.


- Comments    

    - CSS comments are used to add notes or explanations within the CSS code.
    - Comments are ignored by the browser and do not affect the rendering of the page.
    - CSS comments are enclosed in `/*` and `*/`.
    - Example:
        ```
        /* This is a comment */
        body {
            background-color: lightblue; /* This sets the background color */
        }
        ```
        - In this example, a comment is added to explain the purpose of the CSS rule. 

        - The comment `/* This is a comment */` is ignored by the browser and does not affect the rendering of the page.       

- Colors

    - CSS supports various color formats, including named colors, hexadecimal colors, RGB colors, RGBA colors, HSL colors, and HSLA colors.
    - Named colors: Predefined color names (e.g., `red`, `blue`, `green`).
    - Hexadecimal colors: Colors represented in hexadecimal format (e.g., `#FF0000` for red).
    - RGB colors: Colors represented using the RGB model (e.g., `rgb(255, 0, 0)` for red).
    - RGBA colors: RGB colors with an alpha value for opacity (e.g., `rgba(255, 0, 0, 0.5)` for red with 50% opacity).
    - HSL colors: Colors represented using the HSL model (e.g., `hsl(0, 100%, 50%)` for red).
    - HSLA colors: HSL colors with an alpha value for opacity (e.g., `hsla(0, 100%, 50%, 0.5)` for red with 50% opacity).

    - Example:
        ```
        <style>
            body {
                background-color: lightblue;
            }
            h1 {
                color: #FF0000; /* Red */
            }
            p {
                color: rgb(0, 255, 0); /* Green */
            }
            .class-name {
                color: rgba(0, 0, 255, 0.5); /* Blue with 50% opacity */
            }
        </style>
        ```
        - In this example, various color formats are used to set the text color of different elements.


- Backgrounds

    - CSS allows you to set background properties for elements, including background color, background image, background position, background size, and background repeat.
    - Example:
        ```
        <style>
            body {
                background-color: lightblue;
                background-image: url('background.jpg');
                background-position: center;
                background-size: cover;
                background-repeat: no-repeat;
            }
        </style>
        ```
        - In this example, the body element has a light blue background color and a background image.
        - The `background-position` property centers the image, the `background-size` property makes the image cover the entire element, and the `background-repeat` property prevents the image from repeating.

    - Example:
        ```
        <style>
            .class-name {
                background-color: yellow;
                background-image: linear-gradient(to right, red, orange);
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a yellow background color and a linear gradient background image that transitions from red to orange.

- Borders

    - CSS allows you to set borders for elements, including border width, border style, and border color.
    - Example:
        ```
        <style>
            .class-name {
                border: 2px solid black; /* 2px width, solid style, black color */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a 2-pixel solid black border.

    - Example:
        ```
        <style>
            .class-name {
                border-width: 5px;
                border-style: dashed;
                border-color: red;
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a 5-pixel dashed red border.

- Margins

    - CSS allows you to set margins for elements, which create space outside the element's border.
    - Margins can be set using the `margin` property, which can take one to four values.
    - Example:
        ```
        <style>
            .class-name {
                margin: 20px; /* 20 pixels on all sides */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a margin of 20 pixels on all sides.

    - Example:
        ```
        <style>
            .class-name {
                margin: 10px 20px; /* 10 pixels top and bottom, 20 pixels left and right */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a margin of 10 pixels on the top and bottom and 20 pixels on the left and right.

    - Example:
        ```
        <style>
            .class-name {
                margin: 5px 10px 15px; /* 5 pixels top, 10 pixels left and right, 15 pixels bottom */
            }
        </style>
        ```

    - margin - auto, 
        ```
        <style>
            .class-name {
                margin: auto; /* Center the element horizontally */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with an automatic margin, which centers the element horizontally within its parent container.


- Padding        

    - CSS allows you to set padding for elements, which creates space inside the element's border.
    - Padding can be set using the `padding` property, which can take one to four values.
    - Example:
        ```
        <style>
            .class-name {
                padding: 20px; /* 20 pixels on all sides */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a padding of 20 pixels on all sides.

    - Example:
        ```
        <style>
            .class-name {
                padding: 10px 20px; /* 10 pixels top and bottom, 20 pixels left and right */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a padding of 10 pixels on the top and bottom and 20 pixels on the left and right.

    - Example:
        ```
        <style>
            .class-name {
                padding: 5px 10px 15px; /* 5 pixels top, 10 pixels left and right, 15 pixels bottom */
            }
        </style>
        ```

    - Example:
        ```
        <style>
            .class-name {
                padding: 5px; /* 5 pixels on all sides */
                border: 1px solid black; /* Border around the element */
            }
        </style>        
        ```

        - In this example, a class named "class-name" is created with a padding of 5 pixels on all sides and a solid black border around the element.


- Height and Width

    - CSS allows you to set the height and width of elements using the `height` and `width` properties.
    - Height and width can be set using absolute values (e.g., pixels, ems) or relative values (e.g., percentages).
    - Example:
        ```
        <style>
            .class-name {
                width: 300px; /* 300 pixels wide */
                height: 200px; /* 200 pixels tall */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a width of 300 pixels and a height of 200 pixels.

    - Example:
        ```
        <style>
            .class-name {
                width: 50%; /* 50% of the parent element's width */
                height: auto; /* Height adjusts automatically based on content */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a width of 50% of its parent element's width and an automatic height that adjusts based on the content.

    - Example:
        ```
        <style>
            .class-name {
                max-width: 100%; /* Maximum width of 100% of the parent element */
                min-height: 100px; /* Minimum height of 100 pixels */
            }
        </style>
        ```

- Box Model

    - The CSS box model describes the rectangular boxes generated for elements in the document tree and consists of the following components:
        - Content: The actual content of the element (text, images, etc.).
        - Padding: The space between the content and the border.
        - Border: The line surrounding the padding and content.
        - Margin: The space outside the border, separating the element from other elements.

    - Example:
        ```
        <style>
            .class-name {
                width: 300px;
                height: 200px;
                padding: 20px;
                border: 5px solid black;
                margin: 10px;
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a width of 300 pixels, a height of 200 pixels, 20 pixels of padding, a 5-pixel solid black border, and a 10-pixel margin.

- Outline

    - The CSS outline property is used to create a line around an element, similar to a border but without taking up space in the layout.
    - Outlines can be set using the `outline` shorthand property or individual properties for outline color, style, and width.
    - Example:
        ```
        <style>
            .class-name {
                outline: 2px dashed red; /* 2-pixel dashed red outline */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a 2-pixel dashed red outline.

    - Example:
        ```
        <style>
            .class-name {
                outline-color: blue; /* Blue outline color */
                outline-style: solid; /* Solid outline style */
                outline-width: 3px; /* 3-pixel outline width */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with a blue solid outline that is 3 pixels wide.


- Text

    - CSS provides various properties to style text, including font size, font family, font weight, text color, text alignment, line height, letter spacing, and text decoration.
    - Example:
        ```
        <style>
            .class-name {
                font-size: 20px; /* Font size of 20 pixels */
                font-family: Arial, sans-serif; /* Arial font family */
                font-weight: bold; /* Bold font weight */
                color: blue; /* Blue text color */
                text-align: center; /* Centered text alignment */
                line-height: 1.5; /* Line height of 1.5 */
                letter-spacing: 2px; /* 2 pixels of letter spacing */
                text-decoration: underline; /* Underlined text */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with various text styles applied.

- Fonts

    - CSS allows you to set fonts for text using the `font-family`, `font-size`, `font-weight`, and `font-style` properties.
    - You can also use web fonts from services like Google Fonts or Adobe Fonts.
    - Example:
        ```
        <style>
            .class-name {
                font-family: 'Roboto', sans-serif; /* Google Font */
                font-size: 18px; /* Font size of 18 pixels */
                font-weight: normal; /* Normal font weight */
                font-style: italic; /* Italic font style */
            }
        </style>
        ```
        - In this example, a class named "class-name" is created with the Roboto font family, a font size of 18 pixels, normal font weight, and italic font style.

    - Example:
        ```
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif; /* Google Font */
            }
        </style>
        ```

        - In this example, the Roboto font is imported from Google Fonts and applied to the body element.

        - The `link` tag is used to include the font stylesheet, and the `font-family` property is set to use the Roboto font.  

- Icons

    - CSS allows you to use icons in web pages using icon fonts or SVG icons.

    - Icon fonts are font files that contain icons instead of letters, allowing you to use them like text.

    - Example:
        ```
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            .icon {
                font-family: 'Font Awesome 5 Free';
                font-weight: 900; /* Font weight for solid icons */
            }
        </style>
        ```
        - In this example, the Font Awesome icon library is included using a CDN link, and a class named "icon" is created to apply the Font Awesome font family and font weight for solid icons.

- Links

    - CSS allows you to style links using the `a` selector and various properties like color, text decoration, and hover effects.
    - Example:
        ```
        <style>
            a {
                color: blue; /* Blue link color */
                text-decoration: none; /* No underline */
            }
            a:hover {
                text-decoration: underline; /* Underline on hover */
            }
        </style>
        ```
        - In this example, all links are styled with a blue color and no underline, and an underline is added when the link is hovered over.

    - Example:
        ```
        <style>
            a {
                color: red; /* Red link color */
                font-weight: bold; /* Bold link text */
            }
            a:hover {
                color: green; /* Green link color on hover */
            }
        </style>
        ```
        - In this example, all links are styled with a red color and bold text, and the link color changes to green when hovered over.

- Lists

    - CSS allows you to style lists using the `list-style` property and various properties like `padding`, `margin`, and `text-indent`.
    - Example:
        ```
        <style>
            ul {
                list-style-type: square; /* Square bullet points */
                padding-left: 20px; /* Left padding */
            }
            li {
                margin-bottom: 10px; /* Bottom margin for list items */
            }
        </style>
        ```
        - In this example, an unordered list is styled with square bullet points and left padding, and each list item has a bottom margin of 10 pixels.

    - Example:
        ```
        <style>
            ol {
                list-style-type: decimal; /* Decimal numbering */
                padding-left: 20px; /* Left padding */
            }
            li {
                text-indent: 20px; /* Indent text for list items */
            }
        </style>
        ```
        - In this example, an ordered list is styled with decimal numbering and left padding, and each list item has a text indent of 20 pixels.


- Image Sprites

    - CSS image sprites are a technique used to combine multiple images into a single image file, reducing the number of HTTP requests and improving page load times.
    - Example:
        ```
        <style>
            .sprite {
                background-image: url('sprite.png');
                width: 50px; /* Width of each sprite */
                height: 50px; /* Height of each sprite */
            }
            .icon1 {
                background-position: 0 0; /* Position for icon 1 */
            }
            .icon2 {
                background-position: -50px 0; /* Position for icon 2 */
            }
        </style>
        ```
        - In this example, a class named "sprite" is created with a background image of the sprite sheet, and two additional classes "icon1" and "icon2" are created to position the individual icons within the sprite sheet.

- Forms

    - CSS allows you to style form elements, including input fields, buttons, and labels.
    - Example:
        ```
        <style>
            input[type="text"] {
                width: 200px; /* Width of text input */
                padding: 10px; /* Padding inside the input */
                border: 1px solid gray; /* Border around the input */
            }
            button {
                background-color: blue; /* Button background color */
                color: white; /* Button text color */
                padding: 10px 20px; /* Padding inside the button */
                border: none; /* No border */
                cursor: pointer; /* Pointer cursor on hover */
            }
            button:hover {
                background-color: darkblue; /* Darker blue on hover */
            }
        </style>
        ```
        - In this example, a text input field is styled with a width of 200 pixels, padding, and a gray border.
        - A button is styled with a blue background color, white text color, padding, no border, and a pointer cursor on hover. The button's background color changes to dark blue when hovered over.

- Position

    - CSS allows you to control the position of elements using the `position` property, which can take values like `static`, `relative`, `absolute`, `fixed`, and `sticky`.
    - Example:
        ```
        <style>
            .relative {
                position: relative; /* Relative positioning */
                top: 20px; /* Move down 20 pixels */
                left: 10px; /* Move right 10 pixels */
            }
            .absolute {
                position: absolute; /* Absolute positioning */
                top: 50px; /* Move down 50 pixels */
                left: 100px; /* Move right 100 pixels */
            }
            .fixed {
                position: fixed; /* Fixed positioning */
                bottom: 0; /* Stick to the bottom of the viewport */
                right: 0; /* Stick to the right of the viewport */
            }
        </style>
        ```
        - In this example, three classes are created with different positioning styles.
        - The "relative" class moves the element down and to the right relative to its original position.
        - The "absolute" class positions the element at a specific location within its nearest positioned ancestor.
        - The "fixed" class positions the element at a fixed location in the viewport, regardless of scrolling.

- Floating

    - CSS allows you to float elements to the left or right using the `float` property.
    - Floating elements can be used to create multi-column layouts or wrap text around images.
    - Example:
        ```
        <style>
            .float-left {
                float: left; /* Float element to the left */
                width: 200px; /* Width of floated element */
                margin-right: 20px; /* Right margin */
            }
            .float-right {
                float: right; /* Float element to the right */
                width: 200px; /* Width of floated element */
                margin-left: 20px; /* Left margin */
            }
        </style>
        ```
        - In this example, two classes are created for floating elements.
        - The "float-left" class floats the element to the left with a width of 200 pixels and a right margin of 20 pixels.
        - The "float-right" class floats the element to the right with a width of 200 pixels and a left margin of 20 pixels.

    - Example:
        ```
        <style>
            .clearfix::after {
                content: "";
                display: table;
                clear: both;
            }
        </style>
        ```

- Overflow

    - CSS allows you to control how content that overflows an element's box is handled using the `overflow` property.
    - The `overflow` property can take values like `visible`, `hidden`, `scroll`, and `auto`.
    - Example:
        ```
        <style>
            .overflow {
                width: 200px; /* Width of the element */
                height: 100px; /* Height of the element */
                overflow: auto; /* Add scrollbars if content overflows */
            }
        </style>
        ```
        - In this example, a class named "overflow" is created with a width of 200 pixels, a height of 100 pixels, and the `overflow` property set to `auto`, which adds scrollbars if the content overflows the element's box.

- Align

    - CSS allows you to align elements using properties like `text-align`, `vertical-align`, and `flexbox` or `grid` layout techniques.

- Opacity

    - CSS allows you to set the opacity of elements using the `opacity` property, which takes a value between 0 (completely transparent) and 1 (completely opaque).
    - Example:
        ```
        <style>
            .transparent {
                opacity: 0.5; /* 50% opacity */
            }
        </style>
        ```
        - In this example, a class named "transparent" is created with an opacity of 50%, making the element semi-transparent.

    - Example:
        ```
        <style>
            .semi-transparent {
                background-color: rgba(255, 0, 0, 0.5); /* Red with 50% opacity */
            }
        </style>
        ```
        - In this example, a class named "semi-transparent" is created with a red background color and 50% opacity using the RGBA color format.

- Dropdowns

    - CSS allows you to create dropdown menus using the `display` property and pseudo-classes like `:hover`.
    - Example:
        ```
        <style>
            .dropdown {
                position: relative; /* Position relative to parent */
            }
            .dropdown-content {
                display: none; /* Hide dropdown content by default */
                position: absolute; /* Position absolute to parent */
                background-color: white; /* Background color */
                min-width: 160px; /* Minimum width */
                z-index: 1; /* Stack above other elements */
            }
            .dropdown:hover .dropdown-content {
                display: block; /* Show dropdown content on hover */
            }
        </style>
        ```
        - In this example, a class named "dropdown" is created with relative positioning, and a nested class named "dropdown-content" is created with absolute positioning and hidden by default.
        - The dropdown content is displayed when the parent element is hovered over.

    - Example:
        ```
        <style>
            .dropdown {
                position: relative;
            }
            .dropdown-content {
                display: none;
                position: absolute;
                background-color: white;
                min-width: 160px;
                z-index: 1;
            }
            .dropdown:hover .dropdown-content {
                display: block;
            }
        </style>
        ```