# -*- coding: utf-8 -*-
"""

"""


class DFAState(object):
    def __init__(self, name, initial=False, accept=False):
        """"""
        self.name = name
        self.initial = initial
        self.accept = accept
        self.transitions = []

    def __repr__(self):
        return "{0}(initial={1}, accept={2})".format(self.name, self.initial,
                                                     self.accept)

    def add_transition(self, to_, symbol):
        self.transitions.append((to_, symbol))


class MooreState(DFAState):
    def __init__(self, name, out_symbol, initial=False, accept=False):
        """"""
        super(MooreState, self).__init__(name, initial, accept)
        self.out_symbol = out_symbol

    def __repr__(self):
        return ("{0}/{1}(initial={2}, accept={3})"
                .format(self.name, self.out_symbol, self.initial, self.accept))


class MealyState(DFAState):
    def add_transition(self, to_, symbol, out_symbol):
        self.transitions.append((to_, symbol, out_symbol))


class DFA(object):
    def __init__(self, alphabet=None):
        """"""
        if alphabet is None:
            alphabet = []
        self.alphabet = alphabet
        self.initial_state = None
        self.states = []
        self.transitions = []

    def add_state(self, name=None, initial=False, accept=False):
        if initial and self.initial_state is not None:
            raise ValueError('{} already has an initial state.'
                             .format(self.__class__.__name__))
        if name is None:
            last_num = len(self.states)
            name = 'q_{}'.format(last_num)
        state = DFAState(name, initial, accept)
        if initial:
            self.initial_state = state
        self.states.append(state)

    def add_transition(self, from_name, to_name, symbol):
        if len(self.alphabet) == 0:
            raise RuntimeError('{} without alphabet.'
                               .format(self.__class__.__name__))
        if symbol not in self.alphabet:
            raise ValueError('transition symbol not in {} alphabet.'
                             .format(self.__class__.__name__))
        from_ = self.get_state(from_name)
        to_ = self.get_state(to_name)
        if from_ is None:
            raise ValueError('state {0} not in {1}.'
                             .format(from_name, self.__class__.__name__))
        if to_ is None:
            raise ValueError('state {0} not in {1}.'
                             .format(to_name, self.__class__.__name__))
        from_.add_transition(to_, symbol)
        self.transitions.append((from_, to_, symbol))

    def get_accept_states(self):
        return [s for s in self.states if s.accept]

    def process_sequence(self, sequence):
        if len(self.transitions) == 0 or len(self.states) == 0:
            raise RuntimeError('{} has no states or transitions.'
                               .format(self.__class__.__name__))
        if self.initial_state is None:
            raise RuntimeError('{} has no initial state.'
                               .format(self.__class__.__name__))
        if len(self.get_accept_states()) == 0:
            raise RuntimeError('{} has no accept states.'
                               .format(self.__class__.__name__))
        print('Processing "{}"'.format(sequence))
        cur_state = self.initial_state
        print('Transitions:')
        for s in sequence:
            if s not in self.alphabet:
                raise ValueError('sequence symbol {0} not in {1} alphabet.'
                                 .format(s, self.__class__.__name__))
            for next_, symbol in cur_state.transitions:
                if s == symbol:
                    print('\t({from_.name}, {symbol}) -> {to_.name}'
                          .format(from_=cur_state, symbol=s, to_=next_))
                    cur_state = next_
                    break
            else:
                print('\tReject', end='\t')
                print('{cl_name} without transition for {state.name} '
                      'with symbol {symbol}.'
                      .format(cl_name=self.__class__.__name__,
                              state=cur_state, symbol=s))
                return False

        if cur_state.accept:
            print('\tAccept')
            return True
        else:
            print('\tReject', end='\t')
            print('\tState {state.name} is not an accept state.'
                  .format(state=cur_state))
            return False

    def get_state(self, name):
        for s in self.states:
            if name == s.name:
                return s

    def print_matrix(self):
        rows = len(self.states)
        cols = len(self.alphabet)
        mtx = []
        for r in rows:
            sv = [self.states[r].name]
            for c in cols:
                sv.append()

    def remove_unreachable_states(self):
        accessible_states = []
        checked_states = []
        accessible_states.append(self.initial_state)
        i = 0
        while True:
            try:
                cur_state = accessible_states[i]
            except IndexError:
                break
            for to_, symbol in cur_state.transitions:
                if to_ not in accessible_states:
                    accessible_states.append(to_)
            checked_states.append(cur_state)
            i += 1
        self.states = checked_states

    def remove_useless_states(self):
        accept_states = self.get_accept_states()
        useful_states = accept_states
        checked_states = []
        i = 0
        while True:
            try:
                cur_state = useful_states[i]
                # print('cur_state = {}'.format(cur_state.name))
            except IndexError:
                break
            for s in self.states:
                for to_, symbol in s.transitions:
                    if to_ == cur_state and s not in useful_states:
                        # print('adding state {}'.format(s.name))
                        useful_states.append(s)
            checked_states.append(cur_state)
            i += 1
        self.states = useful_states

    def minimize(self):
        self.remove_unreachable_states()
        self.remove_useless_states()

        pairs = []
        # State pairs
        for i in range(len(self.states)):
            for j in range(i, len(self.states)):
                if i != j and (self.states[i], self.states[j]) not in pairs:
                    pairs.append(set([self.states[i], self.states[j]]))
        not_equiv = []
        for i, (q_a, q_b) in enumerate(pairs):
            if ((q_a in self.get_accept_states()
                 and q_b not in self.get_accept_states())
                or (q_b in self.get_accept_states()
                    and q_a not in self.get_accept_states())):
                not_equiv.append(i)
        equiv = []
        not_chkd = [i for i in range(len(pairs)) if i not in not_equiv]

        ni = 0
        while len(not_chkd) != 0:
            try:
                q_a, q_b = pairs[not_chkd[ni]]
            except IndexError:
                ni = 0
                q_a, q_b = pairs[not_chkd[ni]]
            cur_pair = (q_a, q_b)
            eq_chk = []
            eq_chk2 = []
            for t_a, s_a in q_a.transitions:
                for t_b, s_b in q_b.transitions:
                    if s_a == s_b:
                        cur_to_pair = set([t_a, t_b])
                        break
                if t_a == t_b:
                    eq_chk.append(True)
                else:
                    eq_chk.append(False)
                if cur_to_pair in [pairs[n] for n in not_equiv]:
                    not_equiv.append(not_chkd[ni])
                    not_chkd.remove(not_chkd[ni])
                    eq_chk2.append(False)
                    break
                elif cur_to_pair in [pairs[e] for e in equiv]:
                    eq_chk2.append(True)
            if all(eq_chk):
                equiv.append(not_chkd[ni])
                not_chkd.remove(not_chkd[ni])
            elif all(eq_chk2):
                equiv.append(not_chkd[ni])
                not_chkd.remove(not_chkd[ni])
            else:
                ni += 1
        print('Pairs: {}'.format(pairs))
        print('Not equivalent states: {}'.format([pairs[n] for n in not_equiv]))
        print('Equivalent states: {}'.format([pairs[e] for e in equiv]))


class MealyMachine(DFA):
    def __init__(self, alphabet=None, out_alphabet=None):
        """"""
        super(MealyMachine, self).__init__(alphabet)
        self.out_alphabet = out_alphabet

    def add_state(self, name=None, initial=False, accept=False):
        if initial and self.initial_state is not None:
            raise ValueError('{} already has an initial state.'
                             .format(self.__class__.__name__))
        if name is None:
            last_num = len(self.states)
            name = 'q_{}'.format(last_num)
        state = MealyState(name, initial, accept)
        if initial:
            self.initial_state = state
        self.states.append(state)

    def add_transition(self, from_name, to_name, symbol, out_symbol):
        if len(self.alphabet) == 0:
            raise RuntimeError('{} without alphabet.'
                               .format(self.__class__.__name__))
        if len(self.out_alphabet) == 0:
            raise RuntimeError('{} without out alphabet.'
                               .format(self.__class__.__name__))
        if symbol not in self.alphabet:
            raise ValueError('transition symbol not in {} alphabet.'
                             .format(self.__class__.__name__))
        for out_s in out_symbol:
            if out_s not in self.out_alphabet:
                raise ValueError('transition out symbol {0} not in {1} out '
                                 'alphabet.'
                                 .format(out_s, self.__class__.__name__))
        from_ = self.get_state(from_name)
        to_ = self.get_state(to_name)
        if from_ is None:
            raise ValueError('state {0} not in {1}.'
                             .format(from_name, self.__class__.__name__))
        if to_ is None:
            raise ValueError('state {0} not in {1}.'
                             .format(to_name, self.__class__.__name__))
        from_.add_transition(to_, symbol, out_symbol)
        self.transitions.append((from_, to_, symbol, out_symbol))

    def process_sequence(self, sequence):
        if len(self.transitions) == 0 or len(self.states) == 0:
            raise RuntimeError('{} has no states or transitions.'
                               .format(self.__class__.__name__))
        if self.initial_state is None:
            raise RuntimeError('{} has no initial state.'
                               .format(self.__class__.__name__))
        if len(self.get_accept_states()) == 0:
            raise RuntimeError('{} has no accept states.'
                               .format(self.__class__.__name__))
        print('Processing "{}"'.format(sequence))
        cur_state = self.initial_state
        output = []
        print('Transitions:')
        for s in sequence:
            if s not in self.alphabet:
                raise ValueError('sequence symbol {0} not in {1} alphabet.'
                                 .format(s, self.__class__.__name__))
            for next_, symbol, out_symbol in cur_state.transitions:
                if s == symbol:
                    pr_out_symbol = 'ℇ' if out_symbol == '' else out_symbol
                    print('\t({from_.name}, {symbol}, {out_symbol})'
                          ' -> {to_.name}'
                          .format(from_=cur_state, symbol=s,
                                  out_symbol=pr_out_symbol, to_=next_))
                    cur_state = next_
                    output.append(out_symbol)
                    break
            else:
                print('\tReject', end='\t')
                print('{cl_name} without transition for {state.name} '
                      'with symbol "{symbol}".'
                      .format(cl_name=self.__class__.__name__,
                              state=cur_state, symbol=s))
                return False, ''.join(output)

        if cur_state.accept:
            print('\tOutput: ' + ''.join(output))
            print('\tAccept')
            return True, ''.join(output)
        else:
            print('\tOutput: ' + ''.join(output))
            print('\tReject', end='\t')
            print('\tState "{state.name}" is not an accept state.'
                  .format(state=cur_state))
            return False, ''.join(output)
        

if __name__ == '__main__':
    # # Ex 2.1 Remove blanks between words --------------------------------------
    # print('========================Exercício 2.1========================')
    # ex2_1 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])
    #
    # ex2_1.add_state(initial=True)  # q_0
    # ex2_1.add_state()  # q_1
    # ex2_1.add_state()  # q_2
    # ex2_1.add_state(accept=True)  # q_3
    # ex2_1.add_state()  # q_4
    #
    # ex2_1.add_transition('q_0', 'q_1', 'x', 'x')
    # ex2_1.add_transition('q_0', 'q_1', 'X', 'X')
    # ex2_1.add_transition('q_0', 'q_4', '_', '_')
    # ex2_1.add_transition('q_1', 'q_1', 'x', 'x')
    # ex2_1.add_transition('q_1', 'q_1', 'X', 'X')
    # ex2_1.add_transition('q_1', 'q_2', '_', '_')
    # ex2_1.add_transition('q_1', 'q_3', '.', '.')
    # ex2_1.add_transition('q_2', 'q_2', '_', '')
    # ex2_1.add_transition('q_2', 'q_1', 'x', 'x')
    # ex2_1.add_transition('q_2', 'q_1', 'X', 'X')
    # ex2_1.add_transition('q_2', 'q_3', '.', '.')
    # ex2_1.add_transition('q_3', 'q_1', 'x', 'x')
    # ex2_1.add_transition('q_3', 'q_1', 'X', 'X')
    # ex2_1.add_transition('q_3', 'q_1', '_', '_')
    # ex2_1.add_transition('q_4', 'q_4', '_', '_')
    # ex2_1.add_transition('q_4', 'q_1', 'x', 'x')
    # ex2_1.add_transition('q_4', 'q_1', 'X', 'X')
    # ex2_1.add_transition('q_4', 'q_3', '.', '.')
    #
    # # Ex 2.1 [TEST]
    # # _, out2_1 = ex2_1.process_sequence('x___xxx.')
    # # _, out2_1 = ex2_1.process_sequence('x___xxx__x____xx.')
    # _, out2_1 = ex2_1.process_sequence('_____x___xxx__x____xx____._.xX___x__.')
    #
    # # Ex 2.2 Remove blanks from the beginning ---------------------------------
    # print('========================Exercício 2.2========================')
    # ex2_2 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])
    #
    # ex2_2.add_state(initial=True)  # q_0
    # ex2_2.add_state()  # q_1
    # ex2_2.add_state()  # q_2
    # ex2_2.add_state(accept=True)  # q_3
    #
    # ex2_2.add_transition('q_0', 'q_1', 'x', 'x')
    # ex2_2.add_transition('q_0', 'q_1', 'X', 'X')
    # ex2_2.add_transition('q_0', 'q_2', '_', '')
    #
    # ex2_2.add_transition('q_1', 'q_1', 'x', 'x')
    # ex2_2.add_transition('q_1', 'q_1', 'X', 'X')
    # ex2_2.add_transition('q_1', 'q_1', '_', '_')
    # ex2_2.add_transition('q_1', 'q_3', '.', '.')
    #
    # ex2_2.add_transition('q_2', 'q_2', '_', '')
    # ex2_2.add_transition('q_2', 'q_1', 'x', 'x')
    # ex2_2.add_transition('q_2', 'q_1', 'X', 'X')
    # ex2_2.add_transition('q_2', 'q_3', '.', '.')
    #
    # ex2_2.add_transition('q_3', 'q_1', 'x', 'x')
    # ex2_2.add_transition('q_3', 'q_1', 'X', 'X')
    # ex2_2.add_transition('q_3', 'q_2', '_', '_')
    #
    # # Ex 2.2 [TEST]
    # # _, out2_2 = ex2_2.process_sequence('___xxx.')
    # # _, out2_2 = ex2_2.process_sequence('___xxx__x____xx.')
    # _, out2_2 = ex2_2.process_sequence(out2_1)
    #
    # # Ex 2.3 Remove blanks from the end ---------------------------------------
    # print('========================Exercício 2.3========================')
    # ex2_3 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])
    #
    # ex2_3.add_state(initial=True)  # q_0
    # ex2_3.add_state()  # q_1
    # ex2_3.add_state()  # q_2
    # ex2_3.add_state(accept=True)  # q_3
    # ex2_3.add_state(accept=True)  # q_4
    #
    # ex2_3.add_transition('q_0', 'q_1', 'x', 'x')
    # ex2_3.add_transition('q_0', 'q_1', 'X', 'X')
    # ex2_3.add_transition('q_0', 'q_1', '_', '_')
    #
    # ex2_3.add_transition('q_1', 'q_1', 'x', 'x')
    # ex2_3.add_transition('q_1', 'q_1', 'X', 'X')
    # ex2_3.add_transition('q_1', 'q_2', '_', '')
    # ex2_3.add_transition('q_1', 'q_3', '.', '.')
    #
    # ex2_3.add_transition('q_2', 'q_2', '_', '')
    # ex2_3.add_transition('q_2', 'q_4', '.', '.')
    # ex2_3.add_transition('q_2', 'q_1', 'x', '_x')
    # ex2_3.add_transition('q_2', 'q_1', 'X', '_X')
    #
    # ex2_3.add_transition('q_3', 'q_1', 'x', 'x')
    # ex2_3.add_transition('q_3', 'q_1', 'X', 'X')
    # ex2_3.add_transition('q_3', 'q_2', '_', '_')
    # ex2_3.add_transition('q_3', 'q_4', '.', '.')
    #
    # ex2_3.add_transition('q_4', 'q_1', 'x', 'x')
    # ex2_3.add_transition('q_4', 'q_1', 'X', 'X')
    # ex2_3.add_transition('q_4', 'q_3', '_', '_')
    #
    # # Ex 2.3 [TEST]
    # # _, out2_3 = ex2_3.process_sequence('x_xxxx__.')
    # _, out2_3 = ex2_3.process_sequence(out2_2)
    #
    # # Ex 2.4 Title input  -----------------------------------------------------
    # print('========================Exercício 2.4========================')
    # ex2_4 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])
    #
    # ex2_4.add_state(initial=True)  # q_0
    # ex2_4.add_state()  # q_1
    # ex2_4.add_state()  # q_2
    # ex2_4.add_state(accept=True)  # q_3
    #
    # ex2_4.add_transition('q_0', 'q_1', 'x', 'X')
    # ex2_4.add_transition('q_0', 'q_1', 'X', 'X')
    # ex2_4.add_transition('q_0', 'q_2', '_', '_')
    #
    # ex2_4.add_transition('q_1', 'q_1', 'x', 'x')
    # ex2_4.add_transition('q_1', 'q_1', 'X', 'x')
    # ex2_4.add_transition('q_1', 'q_1', '_', '_')
    # ex2_4.add_transition('q_1', 'q_3', '.', '.')
    #
    # ex2_4.add_transition('q_2', 'q_1', 'x', 'X')
    # ex2_4.add_transition('q_2', 'q_1', 'X', 'X')
    # ex2_4.add_transition('q_2', 'q_2', '_', '_')
    # ex2_4.add_transition('q_2', 'q_3', '.', '.')
    #
    # ex2_4.add_transition('q_3', 'q_1', 'x', 'X')
    # ex2_4.add_transition('q_3', 'q_1', 'X', 'X')
    # ex2_4.add_transition('q_3', 'q_2', '_', '_')
    #
    # # Ex 2.4 [TEST]
    # # _, out2_4 = ex2_4.process_sequence('xXX_XxXx.')
    # # _, out2_4 = ex2_4.process_sequence('___xXX_XxXx.')
    # _, out2_4 = ex2_4.process_sequence(out2_3)
    #
    # # Ex 2.5 Phrase sequences w/ one space between ----------------------------
    # print('========================Exercício 2.5========================')
    # ex2_5 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])
    #
    # ex2_5.add_state(initial=True)  # q_0
    # ex2_5.add_state()  # q_1
    # ex2_5.add_state()  # q_2
    # ex2_5.add_state(accept=True)  # q_3
    #
    # ex2_5.add_transition('q_0', 'q_1', 'x', 'x')
    # ex2_5.add_transition('q_0', 'q_1', 'X', 'X')
    # ex2_5.add_transition('q_0', 'q_1', '_', '_')
    #
    # ex2_5.add_transition('q_1', 'q_1', 'x', 'x')
    # ex2_5.add_transition('q_1', 'q_1', 'X', 'x')
    # ex2_5.add_transition('q_1', 'q_1', '_', '_')
    # ex2_5.add_transition('q_1', 'q_3', '.', '.')
    #
    # ex2_5.add_transition('q_2', 'q_2', '_', '')
    # ex2_5.add_transition('q_2', 'q_1', 'x', 'x')
    # ex2_5.add_transition('q_2', 'q_1', 'X', 'X')
    # ex2_5.add_transition('q_2', 'q_3', '.', '.')
    #
    # ex2_5.add_transition('q_3', 'q_1', 'x', '_x')
    # ex2_5.add_transition('q_3', 'q_1', 'X', '_X')
    # ex2_5.add_transition('q_3', 'q_2', '_', '_')
    #
    # # Ex 2.5 [TEST]
    # # _, out2_5 = ex2_5.process_sequence('Xx_xx.Xxx_x.')
    # # _, out2_5 = ex2_5.process_sequence('Xx_xx.Xxx_x.___Xx.')
    # _, out2_5 = ex2_5.process_sequence(out2_4)
    #
    # # Ex 2.6 Phrase sequences without empty phrases ---------------------------
    # print('========================Exercício 2.6========================')
    # ex2_6 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])
    #
    # ex2_6.add_state(initial=True)  # q_0
    # ex2_6.add_state()  # q_1
    # ex2_6.add_state()  # q_2
    # ex2_6.add_state(accept=True)  # q_3
    #
    # ex2_6.add_transition('q_0', 'q_1', 'x', 'x')
    # ex2_6.add_transition('q_0', 'q_1', 'X', 'X')
    # ex2_6.add_transition('q_0', 'q_2', '_', '_')
    #
    # ex2_6.add_transition('q_1', 'q_1', 'x', 'x')
    # ex2_6.add_transition('q_1', 'q_1', 'X', 'X')
    # ex2_6.add_transition('q_1', 'q_1', '_', '_')
    # ex2_6.add_transition('q_1', 'q_3', '.', '.')
    #
    # ex2_6.add_transition('q_2', 'q_2', '_', '')
    # ex2_6.add_transition('q_2', 'q_1', 'x', 'x')
    # ex2_6.add_transition('q_2', 'q_1', 'X', 'X')
    # ex2_6.add_transition('q_2', 'q_1', '.', '')
    #
    # ex2_6.add_transition('q_3', 'q_1', 'x', 'x')
    # ex2_6.add_transition('q_3', 'q_1', 'X', 'X')
    # ex2_6.add_transition('q_3', 'q_2', '_', '')
    #
    # # Ex 2.6 [TEST]
    # # _, out2_6 = ex2_6.process_sequence('X._._Xx_x.')
    # _, out2_6 = ex2_6.process_sequence(out2_5)

    # # Ex 3.a all sentences of (0, 1)* where every “1” is followed by two 0’s.
    # print('========================Exercício 3.A========================')
    # ex3_a = DFA(['0', '1'])
    #
    # ex3_a.add_state(initial=True,
    #                 accept=True)  # q_0 (accept empty and all zeros)
    # ex3_a.add_state()  # q_1 (1st one, not accept)
    # ex3_a.add_state()  # q_2 (1st zero after one)
    #
    # ex3_a.add_transition('q_0', 'q_1', '1')
    # ex3_a.add_transition('q_0', 'q_0', '0')
    # ex3_a.add_transition('q_1', 'q_2', '0')
    # ex3_a.add_transition('q_2', 'q_0', '0')  # (2nd zero after one)
    #
    # # Ex 3.a [TEST]
    # ex3_a.process_sequence('')
    # ex3_a.process_sequence('0')
    # ex3_a.process_sequence('1')
    # ex3_a.process_sequence('100')
    # ex3_a.process_sequence('000000100')
    # ex3_a.process_sequence('01100')
    # ex3_a.process_sequence('0100100100')
    # ex3_a.process_sequence('1001')
    #
    # # Ex 3.b all sentences (a, b)* where all “a” is between two “b”s. -------
    # print('========================Exercício 3.B========================')
    # ex3_b = DFA(['a', 'b'])
    #
    # ex3_b.add_state(initial=True,
    #                 accept=True)  # q_0 (accept empty)
    # ex3_b.add_state(accept=True)  # q_1
    # ex3_b.add_state()  # q_2
    #
    # ex3_b.add_transition('q_0', 'q_1', 'b')  # (1st b)
    # ex3_b.add_transition('q_1', 'q_1', 'b')  # (successive b's)
    # ex3_b.add_transition('q_1', 'q_2', 'a')  # (1st a after b)
    # ex3_b.add_transition('q_2', 'q_1', 'b')  # (1st a after b)
    #
    # # Ex 3.b [TEST]
    # ex3_b.process_sequence('')
    # ex3_b.process_sequence('b')
    # ex3_b.process_sequence('a')
    # ex3_b.process_sequence('bab')
    # ex3_b.process_sequence('aba')
    # ex3_b.process_sequence('baaab')
    # ex3_b.process_sequence('bababab')
    #
    # # Ex 3.c all sentences of (a, b)* where the last symbol is “b” and the
    # # number of “a”s is even
    # print('========================Exercício 3.C========================')
    # ex3_c = DFA(['a', 'b'])
    # ex3_c.add_state(initial=True)  # q_0 (accept empty)
    # ex3_c.add_state(accept=True)  # q_1
    # ex3_c.add_state()  # q_2
    # ex3_c.add_state()  # q_3
    # ex3_c.add_state(accept=True)  # q_4
    # ex3_c.add_state()  # q_5
    #
    # ex3_c.add_transition('q_0', 'q_1', 'b')
    # ex3_c.add_transition('q_0', 'q_2', 'a')
    # ex3_c.add_transition('q_1', 'q_5', 'b')
    # ex3_c.add_transition('q_1', 'q_2', 'a')
    # ex3_c.add_transition('q_2', 'q_3', 'a')
    # ex3_c.add_transition('q_2', 'q_2', 'b')
    # ex3_c.add_transition('q_3', 'q_2', 'a')
    # ex3_c.add_transition('q_3', 'q_4', 'b')
    # ex3_c.add_transition('q_4', 'q_4', 'b')
    # ex3_c.add_transition('q_4', 'q_2', 'a')
    # ex3_c.add_transition('q_5', 'q_5', 'b')
    # ex3_c.add_transition('q_5', 'q_2', 'a')
    #
    # # Ex 3.c [TEST]
    # ex3_c.process_sequence('')
    # ex3_c.process_sequence('b')
    # ex3_c.process_sequence('a')
    # ex3_c.process_sequence('aab')
    # ex3_c.process_sequence('bbaa')
    # ex3_c.process_sequence('bbaaaab')
    # ex3_c.process_sequence('babababab')
    # ex3_c.process_sequence('aaab')
    # ex3_c.process_sequence('baaaab')

    # # Ex 4 traffic lights -----------------------------------------------------
    # print('========================Exercício 4========================')
    # ex4 = MealyMachine(['a'], ['G', 'Y', 'R'])
    #
    # ex4.add_state(initial=True)  # q_0
    # ex4.add_state(accept=True)  # q_1
    # ex4.add_state(accept=True)  # q_2
    # ex4.add_state(accept=True)  # q_3
    #
    # ex4.add_transition('q_0', 'q_1', 'a', 'G')
    # ex4.add_transition('q_1', 'q_2', 'a', 'Y')
    # ex4.add_transition('q_2', 'q_3', 'a', 'R')
    # ex4.add_transition('q_3', 'q_1', 'a', 'G')
    #
    # # Ex 4 [TEST]
    # ex4.process_sequence('aaaaaaaaa')
    # ex4.process_sequence('aaa')

    # # Ex 1.b minimization -----------------------------------------------------
    # ex1_b = DFA(['a', 'b'])
    #
    # ex1_b.add_state(initial=True)  # q_0
    # ex1_b.add_state()  # q_1
    # ex1_b.add_state(accept=True)  # q_2
    # ex1_b.add_state(accept=True)  # q_3
    # ex1_b.add_state(accept=True)  # q_4
    # ex1_b.add_state()  # q_5
    #
    # ex1_b.add_transition('q_0', 'q_1', 'a')
    # ex1_b.add_transition('q_0', 'q_2', 'b')
    # ex1_b.add_transition('q_1', 'q_0', 'a')
    # ex1_b.add_transition('q_1', 'q_3', 'b')
    # ex1_b.add_transition('q_2', 'q_4', 'a')
    # ex1_b.add_transition('q_2', 'q_5', 'b')
    # ex1_b.add_transition('q_3', 'q_4', 'a')
    # ex1_b.add_transition('q_3', 'q_5', 'b')
    # ex1_b.add_transition('q_4', 'q_4', 'a')
    # ex1_b.add_transition('q_4', 'q_5', 'b')
    #
    # # Ex 1.b [TEST]
    # print(ex1_b.states)
    # ex1_b.remove_useless_states()
    # print('After removing useless states')
    # print(ex1_b.states)
    #
    # # Test removing unreachable states ----------------------------------------
    # rm_unreachable = DFA(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
    #
    # rm_unreachable.add_state(initial=True)  # q_0
    # rm_unreachable.add_state()  # q_1
    # rm_unreachable.add_state(accept=True)  # q_2
    # rm_unreachable.add_state()  # q_3
    # rm_unreachable.add_state()  # q_4
    # rm_unreachable.add_state(accept=True)  # q_5
    #
    # rm_unreachable.add_transition('q_0', 'q_0', 'a')
    # rm_unreachable.add_transition('q_0', 'q_4', 'b')
    # rm_unreachable.add_transition('q_0', 'q_3', 'c')
    # rm_unreachable.add_transition('q_1', 'q_4', 'a')
    # rm_unreachable.add_transition('q_1', 'q_1', 'd')
    # rm_unreachable.add_transition('q_2', 'q_4', 'b')
    # rm_unreachable.add_transition('q_2', 'q_1', 'e')
    # rm_unreachable.add_transition('q_3', 'q_4', 'e')
    # rm_unreachable.add_transition('q_4', 'q_3', 'd')
    # rm_unreachable.add_transition('q_4', 'q_5', 'f')
    # rm_unreachable.add_transition('q_5', 'q_0', 'c')
    # rm_unreachable.add_transition('q_5', 'q_5', 'g')
    #
    # # [TEST]
    # print(rm_unreachable.states)
    # rm_unreachable.remove_unreachable_states()
    # print('After removing unreachable states')
    # print(rm_unreachable.states)

    # Test minimize DFA -------------------------------------------------------
    print('======================Exercício Minimização======================')
    min_dfa = DFA(['a', 'b'])

    min_dfa.add_state(initial=True)  # q_0
    min_dfa.add_state()  # q_1
    min_dfa.add_state(accept=True)  # q_2
    min_dfa.add_state()  # q_3
    min_dfa.add_state(accept=True)  # q_4
    min_dfa.add_state(accept=True)  # q_5
    min_dfa.add_state()  # q_6

    min_dfa.add_transition('q_0', 'q_1', 'a')
    min_dfa.add_transition('q_0', 'q_6', 'b')
    min_dfa.add_transition('q_1', 'q_2', 'a')
    min_dfa.add_transition('q_1', 'q_3', 'b')
    min_dfa.add_transition('q_2', 'q_2', 'a')
    min_dfa.add_transition('q_2', 'q_3', 'b')
    min_dfa.add_transition('q_3', 'q_4', 'a')
    min_dfa.add_transition('q_3', 'q_2', 'b')
    min_dfa.add_transition('q_4', 'q_2', 'a')
    min_dfa.add_transition('q_4', 'q_3', 'b')
    min_dfa.add_transition('q_5', 'q_4', 'a')
    min_dfa.add_transition('q_5', 'q_5', 'b')
    min_dfa.add_transition('q_6', 'q_4', 'a')
    min_dfa.add_transition('q_6', 'q_4', 'b')

    # [TEST]
    print(min_dfa.states)
    min_dfa.minimize()
    print('After minimizing')
    print(min_dfa.states)

    print('===========================Exercício 1.a==========================')
    ex1_a = DFA(['a', 'b'])

    ex1_a.add_state(initial=True)  # q_0
    ex1_a.add_state()  # q_1
    ex1_a.add_state()  # q_2
    ex1_a.add_state(accept=True)  # q_3
    ex1_a.add_state(accept=True)  # q_4

    ex1_a.add_transition('q_0', 'q_1', 'a')
    ex1_a.add_transition('q_1', 'q_2', 'b')
    ex1_a.add_transition('q_1', 'q_3', 'a')
    ex1_a.add_transition('q_2', 'q_4', 'a')
    ex1_a.add_transition('q_2', 'q_2', 'b')
    ex1_a.add_transition('q_3', 'q_3', 'a')
    ex1_a.add_transition('q_3', 'q_2', 'b')
    ex1_a.add_transition('q_4', 'q_2', 'b')
    ex1_a.add_transition('q_4', 'q_3', 'a')

    # [TEST]
    print(ex1_a.states)
    ex1_a.minimize()
    print('After minimizing')
    print(ex1_a.states)

    print('===========================Exercício 2.b==========================')
    ex1_b = DFA(['a', 'b'])

    ex1_b.add_state(initial=True)  # q_0
    ex1_b.add_state()  # q_1
    ex1_b.add_state(accept=True)  # q_2
    ex1_b.add_state(accept=True)  # q_3
    ex1_b.add_state(accept=True)  # q_4
    ex1_b.add_state()  # q_5

    ex1_b.add_transition('q_0', 'q_1', 'a')
    ex1_b.add_transition('q_0', 'q_2', 'b')
    ex1_b.add_transition('q_1', 'q_0', 'a')
    ex1_b.add_transition('q_1', 'q_3', 'b')
    ex1_b.add_transition('q_2', 'q_4', 'a')
    ex1_b.add_transition('q_2', 'q_5', 'b')
    ex1_b.add_transition('q_3', 'q_5', 'b')
    ex1_b.add_transition('q_3', 'q_4', 'a')
    ex1_b.add_transition('q_4', 'q_4', 'a')
    ex1_b.add_transition('q_4', 'q_5', 'b')

    # [TEST]
    print(ex1_b.states)
    ex1_b.minimize()
    print('After minimizing')
    print(ex1_b.states)
