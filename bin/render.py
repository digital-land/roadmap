#!/usr/bin/env python3

import os
from frontmatter import Frontmatter

from digital_land_frontend.jinja import setup_jinja
from digital_land_frontend.filters import make_link
from digital_land_frontend.markdown.filter import compile_markdown, markdown_filter

docs_directory = "docs/"
content_directory = "content/"
url_root = "roadmap"

content = {}
tags = {}


def stripp_filter(html):
    html = html.replace('<p class="govuk-body">', '')
    html = html.replace('</p>', '')
    return html


def load_content(path):
    item = Frontmatter.read_file(path)
    key = os.path.splitext(os.path.basename(path))[0]
    content[key] = item

    for tag in item['attributes'].get('tags', []):
        tags.setdefault(tag, [])
        tags[tag].append(key)


def load_content_directory(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith('.md'):
                load_content(os.path.join(root, name))


def render(path, template, directory=docs_directory, **kwargs):
    path = os.path.join(directory, path)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w") as f:
        print(f"creating {path}")
        f.write(template.render(**kwargs))


if __name__ == "__main__":
    env = setup_jinja()
    env.globals["urlRoot"] = url_root
    env.filters["make_link"] = make_link
    env.filters["markdown"] = markdown_filter
    env.filters["stripp"] = stripp_filter

    load_content_directory(content_directory)

    # index pages ..
    for path, template in [
        ("index.html", "index.html"),
    ]:
        render(
            path,
            env.get_template(template),
            content=content,
            tags=tags,
        )
