import reportlab.pdfgen.canvas
import pandas as pd

import os


path_to_data_dir = "fake_test_data/"  # make sure to end the path with a "/"

all_files = os.listdir(path_to_data_dir)

relevant_files = filter(lambda x: x.__contains__("_attributeList_Person.csv"), all_files)  # yields a filter object

relevant_files = [*relevant_files]  # unpacks the filter object into a list of file names

# TODO gather correct alter attributes from data
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
top_margin = 50
# US_letter_dimensions =
page_begin_y = 841
font_size = 12


def draw_line(canvas, tab_level, category, string, index):
    """ draws a line of text to the canvas at a specified tab level, with vertical offset """
    canvas.drawString(left_margin + (12 * (tab_level + 1)), page_begin_y - top_margin - 15 - (12 * index), f'{category}: {string}')


def draw_ego_ID(canvas, ego_id):
    canvas.drawString(left_margin, page_begin_y - top_margin, f'ID: {ego_id}')


def draw_alter(canvas, category_list, value_list, number, block_line_length):
    """ draws formatted lines of data for a single alter """
    # alter name
    draw_line(canvas, 0, category_list[0], value_list[0], number * block_line_length)

    # alter attributes
    for i in range(len(category_list)):
        if i != 0:
            draw_line(canvas, 1, category_list[i], value_list[i], i + number * block_line_length)


def draw_all_alters(canvas, num_alters, category_list, all_alter_values, block_line_length):
    """ draws a series of blocks of formatted alter data """
    for i in range(num_alters):
        draw_alter(canvas, category_list, all_alter_values[i], i, block_line_length)


def get_attributes(alters_dataframe, entry):
    # print(alters_dataframe[entry:entry+1])
    data = alters_dataframe[entry:entry+1]

    print(data)
    # attributes needed for report
    name = "NAME"
    gender = "GENDER"
    relationship = "RELATIONSHIP"
    communication_frequency = "COMMUNICATION_FREQUENCY"
    discussed_su_in_last_90_days = "DISCUSSED SU IN LAST 30 DAYS"

    attributes = {'name': name, 'gender': gender, 'relationship': relationship,
                  'communication_frequency': communication_frequency,
                  'discussed_su_in_last_90_days': discussed_su_in_last_90_days}


    # collect attributes (this is a bit annoying, at least the way I do it)
    name = data['name'].values
    # gender = data["gender_m"]
    # print(gender.values)
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

    communication_frequency = data['communication_frequency'].values[0]
    if communication_frequency == 0:
        communication_frequency = "refused"
    if communication_frequency == 1:
        communication_frequency = "daily"
    if communication_frequency == 2:
        communication_frequency = "weekly"
    if communication_frequency == 3:
        communication_frequency = "monthly"
    if communication_frequency == 4:
        communication_frequency = "less than monthly"
    if communication_frequency == 5:
        communication_frequency = "never"

    if data['discuss_substance'].values[0]:
        discussed_su_in_last_90_days = True


    attributes = {'name': name, 'gender': gender, 'relationship': relationship,
                  'communication_frequency': communication_frequency,
                  'discussed_su_in_last_90_days': discussed_su_in_last_90_days}

    return attributes


def process_interview_responses(alter_data):  # input: pandas DF
    """ intakes alter data and outputs list of dicts, each containing one alter's attributes """
    attribute_list = []
    for i in range(len(alter_data.index)):
        # attribute_list.append({"name": "NAME"})
        attribute_list.append(get_attributes(alter_data, i))
        print(f'attribute list: {attribute_list}')
    return attribute_list
    # return [{'alter name': 'NAME', 'alter gender': 'GENDER', 'alter relationship': 'REL'}, {'alter name': 'NAME', 'alter gender': 'GENDER', 'alter relationship': 'REL'}]


# TODO gather ego uuid

def create_report_for_interview(path):
    """ creates and saves a PDF of alter data for a single ego """
    alter_data = pd.read_csv(path)
    attributes_list: list = process_interview_responses(alter_data)
    BLOCK_LINE_LENGTH = len([*attributes_list[0].keys()])  # number of attributes per alter. This allows us to space alter data blocks
    num_alters = len(attributes_list)
    # print(f'n alters: {num_alters}')
    ego_UUID = "example_ego_UUID"   # TODO regex this
    canvas = reportlab.pdfgen.canvas.Canvas(f'{ego_UUID}.pdf')
    attribute_name_list = [*attributes_list[0].keys()]
    # print(f'attr names: {attribute_name_list}')
    attribute_values_list = [[*attributes.values()] for attributes in attributes_list]
    # print(f'attr values: {attribute_values_list}')

    draw_ego_ID(canvas, ego_UUID)
    draw_all_alters(canvas, num_alters, attribute_name_list, attribute_values_list, BLOCK_LINE_LENGTH)
    canvas.showPage()
    canvas.save()


create_report_for_interview(path_to_data_dir + relevant_files[0])
