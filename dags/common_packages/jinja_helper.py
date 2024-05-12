import jinja2


def load_jinja2_template(template_dir, template_file):
    template_loader = jinja2.FileSystemLoader(searchpath=f"{template_dir}/")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file)
    return template


def render_jinja2_template(template_dir, template_filename, data):
    template = load_jinja2_template(template_dir, template_filename)
    rendered_template = template.render(data)
    return rendered_template

