from reportlab.pdfgen import canvas
import pandas as pd

# TODO add import functionality

interview_session_ID = "fake_test_data/1010101"

ego_UUID = "28f05648-953f-4060-bbb1-1c3e51817687"

data = pd.read_csv(interview_session_ID + "_" + ego_UUID + "_attributeList_Person.csv")

# subset = data.loc[
#     "networkCanvasEgoUUID", "name", "gender_m", "gender_f", "gender_transm",
#     "gender_transf", "gender_gnc", "gender_dk", "gender_refuse",
#     "relationship_type_partner", "relationship_type_parent",
#     "relationship_type_child", "relationship_type_otherFam", "relationship_type_roommate", "relationship_type_friend",
#     "relationship_type_usedWith", "relationship_type_boughtFrom", "relationship_type_sponsor",
#     "relationship_type_healthCare", "relationship_type_substanceProfessional", "relationship_type_o"]


# define alter attributes and attribute block line length
name = "NAME"
gender = "GENDER"
relationship = "RELATIONSHIP"
communication_frequency = "COMMUNICATION_FREQUENCY"
discussed_su_in_last_30_days = "DISCUSSED SU IN LAST 30 DAYS"

attributes = {name: "NAME", gender: "GENDER", relationship: "REL", communication_frequency: "COMS", discussed_su_in_last_30_days: "DSU30"}

BLOCK_LINE_LENGTH = len(attributes)

def draw_line(canvas, tab_level, category, string, index):
    """ draws a line of text to the canvas at a specified tab level, with vertical offset """
    canvas.drawString(100 + (12 * tab_level), 500 - (12 * index) , f'{category}: {string}')


def draw_blank_line(canvas, index):
    draw_line(canvas, 0, "", "#################", index)

def draw_alter(canvas, category_list, value_list, number, block_line_length):
    """ draws formatted lines of data for a single alter """
    # Name
    draw_line(canvas, 0, category_list[0], value_list[0], number * block_line_length)

    # attributes
    for i in range(len(category_list)):
        if i != 0:
            draw_line(canvas, 1, category_list[i], value_list[i], i + number * block_line_length)


def draw_all_alters(canvas, alter_list, category_list, all_alter_values, block_line_length):
    """ draws a series of blocks of formatted alter data """
    for i in range(len(alter_list)):
        draw_alter(canvas, category_list, all_alter_values[i], block_line_length)


canvas = canvas.Canvas('hello_world.pdf')
draw_alter(canvas, [*attributes.keys()], [*attributes.values()], 0, BLOCK_LINE_LENGTH)  # unpacking keys and values as a lists
draw_alter(canvas, [*attributes.keys()], [*attributes.values()], 1, BLOCK_LINE_LENGTH)
canvas.showPage()
canvas.save()
