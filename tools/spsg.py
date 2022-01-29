# A very simple script to generate a blog html page using jinja2.
import jinja2
import markdown
import argparse
import os

# Parse arguments with arparse's help
# Needs two (2) arguments 1st one is the posts template and 2nd is the index page template both are required!
parser = argparse.ArgumentParser()
parser.add_argument("template", help="The template file.", type=str)
parser.add_argument("index_template", help="The template for the index page.", type=str)
args = parser.parse_args()

template = args.template
index_template = args.index_template

# All the the posts must be written in markdown and saved in the follder ./_posts .
inpath = './_posts/'
# The ouput will be directed to the folder ./blog .
outpath = './blog/'

all_posts = []

# Create the ./blog directory if not already exits
os.makedirs(os.path.dirname(outpath), exist_ok=True)

for file in sorted(os.listdir(inpath), reverse=True):
    print("Processing:", file)
    md = os.path.join(inpath, file)
    
    # Check if they are indeed markdown files.
    if file.endswith('.md'):
        with open(md, 'r') as f:
            m = markdown.Markdown(extensions=['markdown.extensions.meta', 'markdown.extensions.extra'])
            html = m.convert(f.read())
        
        content = jinja2.Environment(loader=jinja2.FileSystemLoader('./')).get_template(template).render(body=html, meta=m.Meta)
        # There is probably a beter way but I currently I get the title and date from the markdown metadata
        # and then I create a dictionary called post with them and I also include the path for the file.
        title = m.Meta.get("title")
        date = m.Meta.get("date")
        post = {"title": title[0], "date": date[0], "path": os.path.splitext(file)[0]+'.html'}
        # I then add them in the list all_posts .
        all_posts.append(post)

        outfile = os.path.join(outpath, os.path.splitext(file)[0]+'.html')
        with open(outfile, 'w') as o: o.write(content)
    else:
        print(file, "is not a markdown file!")
        print("\tIt will be skiped!")

# Here is where the index page is constructed.
print("\n*** Generating index page ***")
index_content = jinja2.Environment(loader=jinja2.FileSystemLoader('./')).get_template(index_template).render(all_posts=all_posts)
with open('./blog/index.html', 'w') as i: i.write(index_content)

print("\n---FINISHED!---")

