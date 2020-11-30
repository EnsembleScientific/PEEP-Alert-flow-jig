from guizero import App, PushButton, Slider, Picture, ListBox, Box, Text, TextBox, info
from pathlib import Path

debug = True
full_screen = False
jig_version = 'v1.0.0'

app = App(title="PEEP-Alert Flow Jig", layout='align', width=800, height=480)

app.full_screen = full_screen
if not full_screen: #ie connected to Pi w/ touchscreen
    app.bg = 'black'


title_box = Box(app, height=30, width='fill', border=debug)
title = Text(title_box, text="PEEP-Alert Flow Jig", size=20, color="white")
status_box = Box(title_box, height='fill', width = 50, border=debug)
status_box.bg = 'yellow'

footer_box = Box(app, align='bottom', height=20, width='fill', border=debug)
plot_box = Box(app, align='right', width=500, height='fill', border=debug)

entry_box = Box(app, layout='align', height='fill', border=debug)
# textbox = TextBox(entry_box, text="Enter SN", width='fill')
# textbox.text_size = 16
# textbox.text_color = "white"

# tenkey_box = Box(entry_box, layout='grid')
# tenkey_button_width = 7
# tenkey_button_height = tenkey_button_width-5

version_name = Text(footer_box, align='right', text=jig_version, size=14)
version_name.text_color = "white"

picture = Picture(plot_box, width=500, height=int(500/640*480), image='placeholder.png')

def text_check():
    if arduino_connected():
        arduino_status_text.value = 'Camera ON'
        arduino_status_box.bg = 'green'
    else:
        arduino_status_text.value = "Camera OFF"
        picture.image = 'placeholder.png'
        arduino_status_box.bg = 'red'

arduino_status_box = Box(plot_box, align='bottom', width='fill', height=50, border=debug)
arduino_status_box.text_color = 'white'
arduino_status_box.bg = 'red'
arduino_status_text = Text(arduino_status_box, size=30, text="Camera OFF")
arduino_status_text.repeat(1000, text_check)

def clicked(event_data):
    button_name = event_data.widget.text
    if button_name == "Upload":
        arduino_status_text.value = 'Upload in progress...'
        try:
            success = spark.upload_spark(upload=True, upload_hex_file=hex_file, SN=textbox.value)
            if success:
                app.info('info', "Upload successful!")
            else:
                app.info('info', "Upload failed.")
        except:
            app.info('info', "Failed to upload.")

    elif button_name == "Cycle":
        try:
            spark_c.cycle()
        except:
            app.info('info', "Cycle test failed.")

    elif button_name == "Blocked Cartridge":
        try:
            block_cartridge_image = tests.blocked_cartridge(sn=textbox.value, name="blocked_cartridge")
            if block_cartridge_image is not None:
                print(block_cartridge_image)
                picture.image = str(block_cartridge_image)

        except:
            app.info("info", 'Blocked cartridge test failed.')

    elif button_name == "DEL":
        if textbox.value != "Enter SN":
            textbox.value = textbox.value[:-1]
            if len(textbox.value) == 0:
                textbox.value = "Enter SN"

    elif textbox.value != "Enter SN":
        textbox.value = textbox.value + str(event_data.widget.text)
    else:
        textbox.value = str(event_data.widget.text)


# button1 = PushButton(tenkey_box, text="1", grid=[0,0], width=tenkey_button_width, height=tenkey_button_height)
# button1.text_color = "white"
# button1.bg = "black"
# button1.when_clicked = clicked
# button2 = PushButton(tenkey_box, text="2", grid=[1,0], width=tenkey_button_width, height=tenkey_button_height)
# button2.text_color = "white"
# button2.bg = "black"
# button2.when_clicked = clicked
# button3 = PushButton(tenkey_box, text="3", grid=[2,0], width=tenkey_button_width, height=tenkey_button_height)
# button3.text_color = "white"
# button3.bg = "black"
# button3.when_clicked = clicked
# button4 = PushButton(tenkey_box, text="4", grid=[0,1], width=tenkey_button_width, height=tenkey_button_height)
# button4.text_color = "white"
# button4.bg = "black"
# button4.when_clicked = clicked
# button5 = PushButton(tenkey_box, text="5", grid=[1,1], width=tenkey_button_width, height=tenkey_button_height)
# button5.text_color = "white"
# button5.bg = "black"
# button5.when_clicked = clicked
# button6 = PushButton(tenkey_box, text="6", grid=[2,1], width=tenkey_button_width, height=tenkey_button_height)
# button6.text_color = "white"
# button6.bg = "black"
# button6.when_clicked = clicked
# button7 = PushButton(tenkey_box, text="7", grid=[0,2], width=tenkey_button_width, height=tenkey_button_height)
# button7.text_color = "white"
# button7.bg = "black"
# button7.when_clicked = clicked
# button8 = PushButton(tenkey_box, text="8", grid=[1,2], width=tenkey_button_width, height=tenkey_button_height)
# button8.text_color = "white"
# button8.bg = "black"
# button8.when_clicked = clicked
# button9 = PushButton(tenkey_box, text="9", grid=[2,2], width=tenkey_button_width, height=tenkey_button_height)
# button9.text_color = "white"
# button9.bg = "black"
# button9.when_clicked = clicked
# button0 = PushButton(tenkey_box, text="0", grid=[1,3], width=tenkey_button_width, height=tenkey_button_height)
# button0.text_color = "white"
# button0.bg = "black"
# button0.when_clicked = clicked
# button_delete = PushButton(tenkey_box, text="DEL", grid=[2,3], width=tenkey_button_width, height=tenkey_button_height)
# button_delete.text_color = "white"
# button_delete.bg = "black"
# button_delete.when_clicked = clicked
#
button_upload = PushButton(entry_box, enabled=True, text="Upload", width='fill', height=5, align='bottom')
button_upload.when_clicked = clicked
button_upload.text_color = "white"
button_cycle = PushButton(entry_box, enabled=True, text="Cycle", width='fill', height=5, align='bottom')
button_cycle.text_color = "white"
button_cycle.when_clicked = clicked
button_block = PushButton(entry_box, enabled=True, text="Blocked Cartridge", width='fill', height=5, align='bottom')
button_block.text_color = "white"
button_block.when_clicked = clicked
button_upload.bg = "green"
app.display()
