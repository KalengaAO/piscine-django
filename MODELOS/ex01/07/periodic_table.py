import sys 

def read_periodic_table(filename) -> list[dict]:
    elements = []
    with open(filename, "r") as file:
        for line in file:
            name, properpeties = line.strip().split(" = ")
            properpeties = dict(prop.strip().split(":") for prop in properpeties.split(",")) 
            properpeties['name'] = name
            elements.append(properpeties)
    return elements


def write_td(file, element) -> None:
    file.write('<td style="border: 1px solid black; padding:  10px;">\n')
    file.write(f'<h4>{element["name"]}</h4>\n')
    file.write('<ul>\n')
    file.write(f'<li>No {element["number"]}</li>\n')
    file.write(f'<li>{element["small"]}</li>\n')
    file.write(f'<li>{element["molar"]}</li>\n')
    file.write(f'<li>{element["electron"]}</li>\n')
    file.write('</ul>\n')
    file.write('</td>\n')

def write_html(elements) -> None:
    with open("./periodic_table.html", "w") as file:
        file.write('<!DOCTYPE html>\n')
        file.write('<html lang="en">\n')
        file.write('<head><title>Periodic table HTML</title></head>\n')
        file.write('<body>\n<table>\n')

        for index, element in enumerate(elements):
            position = int(element['position'])
            if position == 0:
                file.write('<tr>\n')
            write_td(file, element)

            if index + 1 < len(elements):
                next_position = int(elements[index  + 1]["position"])
                if next_position != 0 and position + 1 != next_position:
                    file.write(f'<td colspan={next_position - position - 1} style="border: 0px;"></td>\n')

            if position == 17:
                file.write('<tr>\n')
            
        file.write('</table>\n')
        file.write('</body>\n')
        file.write('</html>\n')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        elements = read_periodic_table(sys.argv[1])
        write_html(elements)
    else:
        print(f"Usage: python {sys.argv[0]} periodic_table.txt")