def square(side):
    area = side * side
    if not isinstance(side, int):
        area = math.ceil(area)
    return area
