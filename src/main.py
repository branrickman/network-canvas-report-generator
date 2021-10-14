import reportlab
import pandas as pd
import os

# TODO add import functionality
import reportlab.pdfgen.canvas

path_to_data_dir = "fake_test_data/"  # make sure to end the path with a "/"

all_files = os.listdir(path_to_data_dir)

relevant_files = filter(lambda x: x.__contains__("_attributeList_Person.csv"), all_files)  # yields a filter object

relevant_files = [*relevant_files]  # unpacks the filter object into a list of file names

# interview_session_ID = "1010101"
#
# ego_UUID = "28f05648-953f-4060-bbb1-1c3e51817687"
#
# data = pd.read_csv(path_to_data_dir + interview_session_ID + "_" + ego_UUID + "_attributeList_Person.csv")

# define alter attributes and attribute block line length
name = "NAME"
gender = "GENDER"
relationship = "RELATIONSHIP"
communication_frequency = "COMMUNICATION_FREQUENCY"
discussed_su_in_last_30_days = "DISCUSSED SU IN LAST 30 DAYS"

attributes = {'name': name, 'gender': gender, 'relationship': relationship,
              'communication_frequency': communication_frequency,
              'discussed_su_in_last_30_days': discussed_su_in_last_30_days}

BLOCK_LINE_LENGTH = len(attributes)

left_margin = 25
page_begin_y = 525

# subset = data.loc[
#     "networkCanvasEgoUUID", "name", "gender_m", "gender_f", "gender_transm",
#     "gender_transf", "gender_gnc", "gender_dk", "gender_refuse",
#     "relationship_type_partner", "relationship_type_parent",
#     "relationship_type_child", "relationship_type_otherFam", "relationship_type_roommate", "relationship_type_friend",
#     "relationship_type_usedWith", "relationship_type_boughtFrom", "relationship_type_sponsor",
#     "relationship_type_healthCare", "relationship_type_substanceProfessional", "relationship_type_o"]


def draw_line(canvas, tab_level, category, string, index):
    """ draws a line of text to the canvas at a specified tab level, with vertical offset """
    canvas.drawString(left_margin + (12 * (tab_level + 1)), 500 - (12 * index), f'{category}: {string}')


def draw_blank_line(canvas, index):
    draw_line(canvas, 0, "", "#################", index)


def draw_ego_ID(canvas, ego_id):
    canvas.drawString(left_margin, page_begin_y, f'ID: {ego_id}')


def draw_alter(canvas, category_list, value_list, number, block_line_length):
    """ draws formatted lines of data for a single alter """
    # Name
    draw_line(canvas, 0, category_list[0], value_list[0], number * block_line_length)

    # attributes
    for i in range(len(category_list)):
        if i != 0:
            draw_line(canvas, 1, category_list[i], value_list[i], i + number * block_line_length)


def draw_all_alters(canvas, num_alters, category_list, all_alter_values, block_line_length):
    """ draws a series of blocks of formatted alter data """
    for i in range(num_alters):
        draw_alter(canvas, category_list, all_alter_values[i], i, block_line_length)


def process_interview_responses():
    return [{'gender': 'GENDER', 'relationship': 'REL'}, {'gender': 'GENDER', 'relationship': 'REL'}]


def create_report_for_interview(path):
    alter_data = pd.read_csv(path)
    attributes_list: list = process_interview_responses()  # TODO
    BLOCK_LINE_LENGTH = len([*attributes_list[0].keys()])  # block line is the number of selected attributes per alter. This allows us to space alter data
    #print(BLOCK_LINE_LENGTH)
    num_alters = 2  # TODO
    ego_UUID = "asfklasdhfasldhf"
    canvas = reportlab.pdfgen.canvas.Canvas(f'{ego_UUID}.pdf')
    attribute_name_list = [*attributes_list[0].keys()]
    attribute_values_list = [[*attributes.values()] for attributes in attributes_list]
    #print([[*attributes.values()] for attributes in attributes_list])
    draw_ego_ID(canvas, ego_UUID)
    draw_all_alters(canvas, num_alters, attribute_name_list, attribute_values_list, BLOCK_LINE_LENGTH)

    canvas.showPage()
    canvas.save()


create_report_for_interview(path_to_data_dir + relevant_files[0])
