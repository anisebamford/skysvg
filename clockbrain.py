
def color_to_components(color: str) -> list[int]:
    trimmed = color[1:len(color)]
    components = []
    while len(trimmed) > 0:
        components.append(int(trimmed[0:2], base=16))
        trimmed = trimmed[2:len(trimmed)]
    return components

def components_to_color(components: list[int]) -> str:
    color = "#"
    for component in components:
        h = format_hex(component)
        color = color + h
    return color

def format_hex(value: int) -> str:
    h = hex(value)
    h = h[2:len(h)]
    h = h.rjust(2, "0")
    return h

def get_weighted_average_of_components(c1: int, c2: int, weight: float) -> int:
    return int(c1 * (1 - weight) + c2 * weight)

def get_weighted_average_of_colors(color1, color2, weight) -> str:
    components1 = color_to_components(color1)
    components2 = color_to_components(color2)
    final_components = []
    for i in range(0, len(components1)):
        final_components.append(get_weighted_average_of_components(components1[i], components2[i], weight))
    return components_to_color(final_components)

def format_hours(time_in_minutes: int) -> str:
    hours = time_in_minutes // 60
    return str(hours).rjust(2, "0")

def format_minutes(time_in_minutes: int) -> str:
    minutes = time_in_minutes % 60
    return str(minutes).rjust(2, "0")

def format_am_pm(time_in_minutes: int) -> str:
    return "PM" if time_in_minutes >= 12 * 60 else "AM"

def format_time(time_in_minutes: int) -> str:
    return format_hours(time_in_minutes) + ":" + format_minutes(time_in_minutes)

def get_color_on_gradient(gradient: dict[int, str], value: int) -> str:
    gradient_stops = list(gradient.keys())
    stop_index = 0
    while gradient_stops[stop_index] < value:
        stop_index += 1
        if stop_index == len(gradient_stops):
            return gradient[gradient_stops[stop_index - 1]]
    if stop_index == 0:
        return gradient[gradient_stops[0]]
    stop = gradient_stops[stop_index]
    prev_stop = gradient_stops[stop_index - 1]
    weight = (value - prev_stop) / (stop - prev_stop)
    return get_weighted_average_of_colors(gradient[prev_stop], gradient[stop], weight)

def test(fn, args, expected):
    print(fn)
    result = fn(*args)
    if type(expected) != type(result):
        raise Exception("Expected: " + type(expected) + ", Got: " + type(result))
    if expected != result:
        if type(expected) is list:
            expected = ", ".join(map(str, expected))
            result = ", ".join(map(str, result))
        raise Exception("Expected: " + expected + ", Got: " + result)
    print("Success!")

test(color_to_components, ["#aabbcc"], [0xaa, 0xbb, 0xcc])
test(components_to_color, [[0xaa, 0xbb, 0xcc]], "#aabbcc")
test(format_hex, [15], "0f")
test(format_hex, [16], "10")
test(get_weighted_average_of_components, [10, 20, 0.5], 15)
test(get_weighted_average_of_components, [10, 20, 0.0], 10)
test(get_weighted_average_of_components, [10, 20, 1.0], 20)
test(get_weighted_average_of_colors, ["#ffffff", "#000000", 0.5], "#7f7f7f")
test(format_hours, [8*60 + 59], "08")
test(format_minutes, [11*60 + 7], "07")
test(format_am_pm, [0], "AM")
test(format_am_pm, [11*60 + 59], "AM")
test(format_am_pm, [12*60], "PM")
test(format_time, [11*60+50], "11:50")
test(get_color_on_gradient, [{10: "#ffffff", 20: "#000000"}, 15], "#7f7f7f")


normalized_times = {
    "nightEnd": 5*60,
    "dawn": 6* 60,
    "dayStart": 7*60,
    "dayEnd": 17 * 60,
    "dusk": 18 * 60,
    "nightStart": 19 * 60,
}

skyGradient = {
    normalized_times["nightEnd"]: "#19072e",
    normalized_times["dawn"]: "#f9b1ff",
    normalized_times["dayStart"]: "#33e7ff",
    normalized_times["dayEnd"]: "#33e7ff",
    normalized_times["dusk"]: "#19072e",
    normalized_times["nightStart"]: "#19072e",
}

rightCloudGradient = {
    normalized_times["nightEnd"]: "#19072e",
    normalized_times["dawn"]: "#ff5599",
    normalized_times["dayStart"]: "#ffffff",
    normalized_times["dayEnd"]: "#ffffff",
    normalized_times["dusk"]: "#d54815",
    normalized_times["nightStart"]: "#19072e",
}

leftCloudGradient = {
    normalized_times["nightEnd"]: "#19072e",
    normalized_times["dawn"]: "#ff6600",
    normalized_times["dayStart"]: "#ffffff",
    normalized_times["dayEnd"]: "#ffffff",
    normalized_times["dusk"]: "#5d37d5",
    normalized_times["nightStart"]: "#19072e",
}

cloudBorderGradient = {
    normalized_times["nightEnd"]: "#ffffff",
    normalized_times["dawn"]: "#ffffff",
    normalized_times["dayStart"]: "#33e7ff",
    normalized_times["dayEnd"]: "#33e7ff",
    normalized_times["dusk"]: "#ffffff",
    normalized_times["nightStart"]: "#ffffff",
}
