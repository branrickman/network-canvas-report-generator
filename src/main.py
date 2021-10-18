import reportlab.pdfgen.canvas
import pandas as pd

import re
import os

path_to_data_dir = "fake_test_data/"
if path_to_data_dir[len(path_to_data_dir)-1] != '/':  # add a backslash to path name if omitted
    path_to_data_dir = path_to_data_dir + '/'
    print(path_to_data_dir)

# define alter attributes and attribute block line length
name = "NAME"
gender = "GENDER"
relationship = "RELATIONSHIP"
# communication_frequency = "COMMUNICATION_FREQUENCY"
# discussed_su_in_last_30_days = "DISCUSSED SU IN LAST 30 DAYS"

attributes = {'name': name, 'gender': gender, 'relationship': relationship, "": ""}

              # 'communication_frequency': communication_frequency,
              # 'discussed_su_in_last_30_days': discussed_su_in_last_30_days}

BLOCK_LINE_LENGTH = len(attributes)  # the length (in lines) of the alter attributes block
left_margin = 25
top_margin = 50
page_begin_y = 841  # this assumes the default reportlab size (A4)
font_size = 12


def get_relevant_files(path):
    """ grabs only the exported Net. Canvas files that contain alter data (*_attributeList_Person.csv) """
    path_to_data_dir = path
    all_files = os.listdir(path_to_data_dir)
    relevant_files = filter(lambda x: x.__contains__("_attributeList_Person.csv"), all_files)  # yields a filter object
    relevant_files = [*relevant_files]  # unpacks the filter object into a list of file names
    return relevant_files


def draw_ego_id(canvas, ego_id):
    """ draws the ego information """
    canvas.drawString(left_margin, page_begin_y - top_margin, f'Case ID: {ego_id[0]}')
    canvas.drawString(left_margin, page_begin_y - top_margin - 10, f'UUID: {ego_id[1]}')
    canvas.drawString(left_margin, page_begin_y - top_margin - 20, f'')



def draw_line(canvas, tab_level, category, string, index, kind):
    """ draws a line of text to the canvas at a specified tab level, with vertical offset """
    # a bunch of hardcoded, undocumented offsets hacked together
    if kind == "attribute":
        canvas.drawString(left_margin + (12 * (tab_level + 1)), page_begin_y - top_margin - 15 - 20 -(12 * index), f'{category}: {string}')

    if kind == "space":
        canvas.drawString(left_margin + (12 * (tab_level + 1)), page_begin_y - top_margin - 15 - 20 -(12 * index), f'')

def draw_alter(canvas, category_list, value_list, number, block_line_length):
    """ draws formatted lines of data for a single alter """
    # alter name
    # draw_line(canvas, 1, "", "", number * block_line_length)
    draw_line(canvas, 0, category_list[0], value_list[0], number * block_line_length, kind="attribute")

    # alter attributes
    for i in range(len(category_list)):
        if i != 0 and i != len(category_list) - 1:
            draw_line(canvas, 1, category_list[i], value_list[i], i + number * block_line_length, kind="attribute")
        else:
            draw_line(canvas, 1, category_list[i], value_list[i], i + number * block_line_length, kind="space")


def draw_all_alters(canvas, num_alters, category_list, all_alter_values, block_line_length):
    """ draws a series of blocks of formatted alter data """
    for i in range(num_alters):
        draw_alter(canvas, category_list, all_alter_values[i], i, block_line_length)


def strip_brackets(name):
    return name.strip('[]')


def get_attributes(alters_dataframe, entry):
    """ Gathers the attributes of each alter. Define the desired attributes by modifying "attributes" at the end of
    the function """
    # print(alters_dataframe[entry:entry+1])
    data = alters_dataframe[entry:entry+1]

    # define attributes needed for report
    name = "NAME"
    gender = "GENDER"
    relationship = "RELATIONSHIP"
    communication_frequency = "COMMUNICATION_FREQUENCY"
    discussed_su_in_last_90_days = "DISCUSSED SU IN LAST 30 DAYS"


    # collect attributes (this is a bit annoying, at least the way I do it)
    name = list(data['name'].values)
    name = name[0]  # this strips the brackets from the alter names

    if data['gender_m'].values[0]:
        gender = "gender_m"
    if data['gender_f'].values[0]:
        gender = "gender_f"
    if data['gender_transf'].values[0]:
        gender = "gender_transf"
    if data['gender_transm'].values[0]:
        gender = "gender_transm"
    if data['gender_gnc'].values[0]:
        gender = "gender_gnc"
    if data['gender_dk'].values[0]:
        gender = "gender_dk"
    if data['gender_refuse'].values[0]:
        gender = "gender_refuse"

    if data['relationship_type_partner'].values[0]:
        relationship = "relationship_type_partner"
    if data['relationship_type_parent'].values[0]:
        relationship = "relationship_type_parent"
    if data['relationship_type_child'].values[0]:
        relationship = "relationship_type_child"
    if data['relationship_type_otherFam'].values[0]:
        relationship = "relationship_type_otherFam"
    if data['relationship_type_roommate'].values[0]:
        relationship = "relationship_type_roommate"
    if data['relationship_type_friend'].values[0]:
        relationship = "relationship_type_friend"
    if data['relationship_type_usedWith'].values[0]:
        relationship = "relationship_type_usedWith"
    if data['relationship_type_boughtFrom'].values[0]:
        relationship = "relationship_type_boughtFrom"
    if data['relationship_type_sponsor'].values[0]:
        relationship = "relationship_type_sponsor"
    if data['relationship_type_healthCare'].values[0]:
        relationship = "relationship_type_healthCare"
    if data['relationship_type_substanceProfessional'].values[0]:
        relationship = "relationship_type_substanceProfessional"
    if data['relationship_type_o'].values[0]:
        relationship = "relationship_type_o"

    # communication_frequency = data['communication_frequency'].values[0]
    # if communication_frequency == 0:
    #     communication_frequency = "refused"
    # if communication_frequency == 1:
    #     communication_frequency = "daily"
    # if communication_frequency == 2:
    #     communication_frequency = "weekly"
    # if communication_frequency == 3:
    #     communication_frequency = "monthly"
    # if communication_frequency == 4:
    #     communication_frequency = "less than monthly"
    # if communication_frequency == 5:
    #     communication_frequency = "never"

    # if data['discuss_substance'].values[0]:
    #     discussed_su_in_last_90_days = True


    attributes = {'name': name, 'gender': gender, 'relationship': relationship, "space": "space"}
                  # 'communication_frequency': communication_frequency,
                  # 'discussed_su_in_last_90_days': discussed_su_in_last_90_days}
    print(attributes)

    return attributes


def process_interview_responses(alter_data):  # input: pandas DF
    """ intakes alter data and outputs list of dicts, each containing one alter's attributes """
    attribute_list = []
    for i in range(len(alter_data.index)):
        attribute_list.append(get_attributes(alter_data, i))
    return attribute_list


def create_report_for_interview(path):
    """ creates and saves a PDF of alter data for a single ego """
    alter_data = pd.read_csv(path)
    attributes_list: list = process_interview_responses(alter_data)
    BLOCK_LINE_LENGTH = len([*attributes_list[0].keys()])  # number of attributes per alter. This allows us to space alter data blocks
    num_alters = len(attributes_list)

    # grab the ego UUID
    separated_path = re.split(",|_|/", path)
    # print(f'sep. path: {separated_path}')
    # separated_path = [a for a in separated_path if len(a) > 32]  # grab the ego UUID (will not work with folder names over 32 characters in length)
    ego_UUID = f'{separated_path[len(separated_path) - 1 - 2]}'  # any NC export will place the ego UUID in the 3rd from the end when split as above
    ego_case_ID = f'{separated_path[len(separated_path) - 1 - 3]}'
    ego_combined_ID = [ego_case_ID, ego_UUID]

    attribute_name_list = [*attributes_list[0].keys()]
    attribute_values_list = [[*attributes.values()] for attributes in attributes_list]

    # create the reportlab canvas, draw to it, and save as pdf
    canvas = reportlab.pdfgen.canvas.Canvas(f'{ego_case_ID + "_" +  ego_UUID}_report.pdf')  # UUID at the beginning for easy searches
    draw_ego_id(canvas, ego_combined_ID)
    draw_all_alters(canvas, num_alters, attribute_name_list, attribute_values_list, BLOCK_LINE_LENGTH)
    canvas.showPage()
    canvas.save()


def main():
    relevant_files = get_relevant_files(path_to_data_dir)
    for i in range(len(relevant_files)):
        create_report_for_interview(path_to_data_dir + relevant_files[i])


if __name__ == "__main__":
    main()
