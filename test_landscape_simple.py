import lv_config_simple as lv_config
import lvgl as lv
import time

HEIGHT = lv_config.HEIGHT
WIDTH = lv_config.WIDTH

size_x = 50
size_y = 50
slide_x = 200
slide_y = 40
text_y = -100

print('Hello LVGL - Landscape Mode Test')

scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x000000), 0)

print('Creating colored squares...')
# Left TOP - Red
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(0, 0)
rect.set_style_bg_color(lv.color_make(255, 0, 0), 0)

label = lv.label(rect)
label.set_text("R")
label.center()
label.set_style_text_color(lv.color_make(0, 0, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

# Right TOP - Green
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(WIDTH-size_x, 0)
rect.set_style_bg_color(lv.color_make(0, 255, 0), 0)

label = lv.label(rect)
label.set_text("G")
label.center()
label.set_style_text_color(lv.color_make(0, 0, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

# Left BOTTOM - Blue
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(0, HEIGHT-size_y)
rect.set_style_bg_color(lv.color_make(0, 0, 255), 0)

label = lv.label(rect)
label.set_text("B")
label.center()
label.set_style_text_color(lv.color_make(0, 0, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

# Right BOTTOM - White
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(WIDTH-size_x, HEIGHT-size_y)
rect.set_style_bg_color(lv.color_make(255, 255, 255), 0)

label = lv.label(rect)
label.set_text("W")
label.center()
label.set_style_text_color(lv.color_make(0, 0, 0), 0)
label.set_style_text_font(lv.font_montserrat_16, 0)

# Draw cross lines
line1 = lv.line(scr)
line2 = lv.line(scr)

points1 = [
    {"x": size_x, "y": size_y},
    {"x": WIDTH - size_x, "y": HEIGHT - size_y}
]
points2 = [
    {"x": WIDTH - size_x, "y": size_y},
    {"x": size_x, "y": HEIGHT - size_y}
]

line1.set_points(points1, 2)
line2.set_points(points2, 2)

line1.set_style_line_color(lv.color_make(255, 255, 255), 0)
line2.set_style_line_color(lv.color_make(255, 255, 255), 0)

line1.set_style_line_width(2, 0)
line2.set_style_line_width(2, 0)

# Slider
slider = lv.slider(scr)
slider.set_size(slide_x, slide_y)
slider.center()

# Center label
label = lv.label(scr)
label.set_text(f"{WIDTH}x{HEIGHT}")
label.align(lv.ALIGN.CENTER, 0, text_y)
label.set_style_text_font(lv.font_montserrat_16, 0)

print('UI created. Starting main loop...')

# Main loop
while True:
    lv.timer_handler()
    time.sleep_ms(5)
