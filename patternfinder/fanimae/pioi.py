from Bio import pairwise2
# from Bio.pairwise2 import format_alignment
import midiparser
import os
# from pprint import pprint
import math


def compare_pitch(p1, p2):
    '''Local alignment algorithm using values for pitch comparison.'''

    match = 1
    mismat = -1
    insert = -2
    delete = -2

    alignment = pairwise2.align.localms(p1, p2, match, mismat, insert, delete)
    return alignment[0][2]


def compare_ioi(ioi1, ioi2):
    '''Local alignment algorithm using values for IOI comparison'''

    matrix = {('R', 'R'): 3,
              ('s', 's'): 2,
              ('l', 'l'): 2,
              ('S', 'S'): 1,
              ('L', 'L'): 1,
              ('S', 's'): 0,
              ('L', 'l'): 0,
              ('R', 's'): -2,
              ('R', 'l'): -2,
              ('R', 'S'): -2,
              ('R', 'L'): -2,
              ('S', 'L'): -3,
              ('S', 'l'): -3,
              ('s', 'L'): -3,
              ('s', 'l'): -3}
    insert = -2
    delete = -2

    alignment = pairwise2.align.localds(ioi1, ioi2, matrix, insert, delete)
    return alignment[0][2]


def vector_score(score_dict):
    '''Computing the total score based on the two parameters' scores'''

    for piece in score_dict:
        pitch, ioi = score_dict[piece]
        pitch = math.pow(18, 2) * math.pow(pitch, 2)
        ioi = math.pow(ioi, 2)
        total = math.sqrt(pitch + ioi)
        score_dict[piece] = total
    return score_dict


def run(query, directory):

    q_info = midiparser.process_file(query)
    q_info = q_info[0][0], q_info[1][0]

    d_num = {}
    for file in os.listdir(directory):
        if file != '.DS_Store':
            d_info = midiparser.process_file(directory + '/' + file)
            dinfo = []
            for n in range(len(d_info[0])):
                dinfo.append((d_info[0][n], d_info[1][n]))

            for part in range(len(dinfo)):

                ioi_score = compare_ioi(q_info[0], dinfo[part][0])
                pitch_score = compare_pitch(q_info[1], dinfo[part][1])
                d_num[file] = (pitch_score, ioi_score)

    final_scores = vector_score(d_num)
    return final_scores
