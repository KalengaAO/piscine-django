import sys, os, re
import settings


def reader(filename):
    if not filename.endswith('.template'):
        print(f"warning: extension is wrong {filename}")
        sys.exit(1)
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError as e:
        print(f"Error: {filename}: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: {filename}: {e}")
        sys.exit(1)
    except IsDirectoryError as e:
        print(f"Error: {filename}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {filename}: {e}")
        sys.exit(1)
    return content

""" funciona mais não é nada pythonico!
def render_other_way(template):
    template_data = {}
    if not os.path.exists("./settings.py"):
        print(f"file not exit settings.py")
        sys.exit(1)
    elif not template.endswith(".template"):
        print(f"error of format: {template}")
        sys.exit(1)
    try:
        with open("./settings.py", "r") as file:
            for line in file:
                key, value = line.split(" = ")
                template_data[f"{key.strip(' ')}"] = value.strip()
    except Exception as e:
        print(f"Error: {e}")
    html_file = re.sub('\.template', '.html', template)
    with open(html_file, "w") as html:
        with open(template, "r") as tmp:
            for line in tmp:
                for key, value in template_data.items():
                    line = line.replace("{" + key + "}", value)
                html.write(line)
"""

def render(filename):
    template = reader(filename)
    template = template.format(name=settings.name, surname=settings.surname, \
        age=settings.age, profession=settings.profession, title=settings.title)
    html_file = re.sub('\.template', '.html', filename)
    with open(html_file, 'w') as html:
        html.write(template)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        render(sys.argv[1])
        #render_other_way(sys.argv[1])
    else:
        print(f"Usage: python3 {sys.argv[0]} file.template")