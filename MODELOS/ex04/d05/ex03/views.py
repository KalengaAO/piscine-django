from django.shortcuts import render

# Create your views here.
def gradient_table(request):
    colors = {"black": (0 , 0, 0), "red": (255, 0, 0), "green": (0, 255, 0), "blue":(0, 0, 255),}

    gradient = []
    for it in range(50):
        row = []
        for (r, g, b) in colors.values():
            factor = int((it / 49) * 255)
            row.append(f"{factor * r // 255}, {factor * g // 255}, {factor * b // 255}")
        gradient.append(row)

    return render(request, "ex03/index.html", {"gradient":gradient})