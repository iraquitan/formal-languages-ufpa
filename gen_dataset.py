# -*- coding: utf-8 -*-
import os
import numpy as np
import rstr

from dfa import DFA


def gen_dataset(fname):
    with open(os.path.expanduser(fname), 'r') as f:
        str_dataset = f.read()

    dict_dataset = {}
    cur_id = '0'
    fl = []
    for r in str_dataset.split('\n'):
        if r == '':
            dict_dataset[cur_id] = fl
            break
        id, fr = r.split(' ')
        if id == cur_id:
            fl.append(fr)
        else:
            dict_dataset[cur_id] = fl
            fl = [fr]
        cur_id = id
    return dict_dataset


def gen_fake(n_total=4039, n_genuines=1399):
    total = np.arange(n_total)
    genuines = np.random.choice(total, size=n_genuines, replace=False)
    fakes = total[np.in1d(total, genuines, invert=True)]
    return genuines, fakes


def friend_pattern(px_friend_list, genuine_ix):
    new_friend_list = []
    n_genuines = 0
    n_genuines = []
    # n_fakes = 0
    n_fakes = []
    genuine_fp = '(a|b)*a#'  # Facebook FP
    fake_fp = '(a*|b)(b|ab*a)#'
    for i, inst in enumerate(px_friend_list):
        if int(inst) in genuine_ix:
            fp_to_use = genuine_fp
            # n_genuines += 1
            n_genuines.append('genuine')
        else:
            fp_to_use = fake_fp
            # n_fakes += 1
            n_fakes.append('fake')
        while True:
            fp = rstr.xeger(fp_to_use)
            if fp not in new_friend_list:
                break
        new_friend_list.append(fp)
    return new_friend_list, n_genuines, n_fakes


class FacebookIPR(object):
    def __init__(self, ):
        """"""
        ipr = DFA(alphabet=['a', 'b', '#'])
        # States
        ipr.add_state(initial=True)  # q_0
        ipr.add_state()  # q_1
        ipr.add_state()  # q_2
        ipr.add_state(accept=True)  # q_3
        # Transitions
        ipr.add_transition('q_0', 'q_1', 'a')
        ipr.add_transition('q_0', 'q_1', 'b')
        ipr.add_transition('q_1', 'q_2', 'a')
        ipr.add_transition('q_1', 'q_1', 'b')
        ipr.add_transition('q_2', 'q_2', 'a')
        ipr.add_transition('q_2', 'q_1', 'b')
        ipr.add_transition('q_2', 'q_3', '#')
        self.dfa = ipr

    def check_profile(self, profile):
        return self.dfa.process_sequence(profile, verbose=False)


if __name__ == '__main__':
    fname = '~/Downloads/facebook_combined.txt'
    fb_ipr = FacebookIPR()
    ds = gen_dataset(fname)
    genuine_ix, fake_ix = gen_fake()
    test_genuine_count = 0
    y_test = []
    test_fake_count = 0
    genuine_count = 0
    y_pred = []
    fake_count = 0
    for i, (px, fl) in enumerate(ds.items()):
        # print('Working on profile px = {}'.format(px))
        fl_intances, n_g, n_f = friend_pattern(ds[px], genuine_ix)
        test_genuine_count += len(n_g)
        test_fake_count += len(n_f)
        y_test.extend(n_g)
        y_test.extend(n_f)
        for px_i, ix in enumerate(fl_intances):
            if fb_ipr.check_profile(ix):
                genuine_count += 1
                y_pred.append('genuine')
            else:
                fake_count += 1
                y_pred.append('fake')
        if i == 50:
            break
    print('Number of test genuine profiles: {}'.format(test_genuine_count))
    print('Number of predicted genuine profiles: {}'.format(genuine_count))
    print('Number of test fake profiles: {}'.format(test_fake_count))
    print('Number of predicted fake profiles: {}'.format(fake_count))
    print('done.')
