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
                return False

        if cur_state.accept:
            print('\tOutput: ' + ''.join(output))
            print('\tAccept')
            return True
        else:
            print('\tOutput: ' + ''.join(output))
            print('\tReject', end='\t')
            print('\tState "{state.name}" is not an accept state.'
                  .format(state=cur_state))
            return False
        

if __name__ == '__main__':
    # # Ex 3.a ------------------------------------------------------------------
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

    # # Ex 3.b ------------------------------------------------------------------
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

    # # Ex 3.c ------------------------------------------------------------------
    # ex3_c = DFA(['a', 'b'])
    # ex3_c.add_state(initial=True, accept=True)  # q_0 (accept empty)
    # ex3_c.add_state()  # q_1
    # ex3_c.add_state()  # q_2
    # ex3_c.add_state()  # q_3
    # ex3_c.add_state(accept=True)  # q_4
    # 
    # ex3_c.add_transition('q_0', 'q_1', 'b')
    # ex3_c.add_transition('q_0', 'q_2', 'a')
    # ex3_c.add_transition('q_1', 'q_1', 'b')
    # ex3_c.add_transition('q_1', 'q_2', 'a')
    # ex3_c.add_transition('q_2', 'q_3', 'a')
    # ex3_c.add_transition('q_2', 'q_2', 'b')
    # ex3_c.add_transition('q_3', 'q_2', 'a')
    # ex3_c.add_transition('q_3', 'q_4', 'b')
    # ex3_c.add_transition('q_4', 'q_4', 'b')
    # ex3_c.add_transition('q_4', 'q_2', 'a')
    # 
    # # Ex 3.c [TEST]
    # ex3_c.process_sequence('')
    # ex3_c.process_sequence('b')
    # ex3_c.process_sequence('a')
    # ex3_c.process_sequence('aab')
    # ex3_c.process_sequence('bbaa')
    # ex3_c.process_sequence('bbaaaab')
    # ex3_c.process_sequence('babababab')

    # Ex 2.1 Remove blanks between words --------------------------------------
    ex2_1 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])
    
    ex2_1.add_state(initial=True)  # q_0
    ex2_1.add_state()  # q_1
    ex2_1.add_state()  # q_2
    ex2_1.add_state(accept=True)  # q_3

    ex2_1.add_transition('q_0', 'q_1', 'x', 'x')
    ex2_1.add_transition('q_0', 'q_1', 'X', 'X')
    ex2_1.add_transition('q_0', 'q_1', '_', '_')
    ex2_1.add_transition('q_1', 'q_1', 'x', 'x')
    ex2_1.add_transition('q_1', 'q_1', 'X', 'X')
    ex2_1.add_transition('q_1', 'q_2', '_', '_')
    ex2_1.add_transition('q_1', 'q_3', '.', '.')
    ex2_1.add_transition('q_2', 'q_2', '_', '')
    ex2_1.add_transition('q_2', 'q_1', 'x', 'x')
    ex2_1.add_transition('q_2', 'q_1', 'X', 'X')
    
    # Ex 2.1 [TEST]
    ex2_1.process_sequence('x___xxx.')
    ex2_1.process_sequence('x___xxx__x____xx.')

    # Ex 2.2 Remove blanks from the beginning ---------------------------------
    ex2_2 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])

    ex2_2.add_state(initial=True)  # q_0
    ex2_2.add_state()  # q_1
    ex2_2.add_state()  # q_2
    ex2_2.add_state(accept=True)  # q_3

    ex2_2.add_transition('q_0', 'q_1', 'x', 'x')
    ex2_2.add_transition('q_0', 'q_1', 'X', 'X')
    ex2_2.add_transition('q_0', 'q_2', '_', '')
    ex2_2.add_transition('q_1', 'q_1', 'x', 'x')
    ex2_2.add_transition('q_1', 'q_1', 'X', 'X')
    ex2_2.add_transition('q_1', 'q_1', '_', '_')
    ex2_2.add_transition('q_1', 'q_3', '.', '.')

    ex2_2.add_transition('q_2', 'q_2', '_', '')
    ex2_2.add_transition('q_2', 'q_1', 'x', 'x')
    ex2_2.add_transition('q_2', 'q_1', 'X', 'X')

    # Ex 2.2 [TEST]
    ex2_2.process_sequence('___xxx.')
    ex2_2.process_sequence('___xxx__x____xx.')

    # Ex 2.3 Remove blanks from the end ---------------------------------------
    ex2_3 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])

    ex2_3.add_state(initial=True)  # q_0
    ex2_3.add_state()  # q_1
    ex2_3.add_state()  # q_2
    ex2_3.add_state(accept=True)  # q_3
    ex2_3.add_state(accept=True)  # q_4

    ex2_3.add_transition('q_0', 'q_1', 'x', 'x')
    ex2_3.add_transition('q_0', 'q_1', 'X', 'X')
    ex2_3.add_transition('q_0', 'q_1', '_', '_')
    ex2_3.add_transition('q_1', 'q_1', 'x', 'x')
    ex2_3.add_transition('q_1', 'q_1', 'X', 'X')
    ex2_3.add_transition('q_1', 'q_2', '_', '')
    ex2_3.add_transition('q_1', 'q_3', '.', '.')

    ex2_3.add_transition('q_2', 'q_2', '_', '')
    ex2_3.add_transition('q_2', 'q_4', '.', '.')
    ex2_3.add_transition('q_2', 'q_1', 'x', '_x')
    ex2_3.add_transition('q_2', 'q_1', 'X', '_X')

    # Ex 2.3 [TEST]
    ex2_3.process_sequence('x_xxxx__.')

    # Ex 2.4 Title input  -----------------------------------------------------
    ex2_4 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])

    ex2_4.add_state(initial=True)  # q_0
    ex2_4.add_state()  # q_1
    ex2_4.add_state()  # q_2
    ex2_4.add_state(accept=True)  # q_3

    ex2_4.add_transition('q_0', 'q_1', 'x', 'X')
    ex2_4.add_transition('q_0', 'q_1', 'X', 'X')
    ex2_4.add_transition('q_0', 'q_2', '_', '_')
    ex2_4.add_transition('q_1', 'q_1', 'x', 'x')
    ex2_4.add_transition('q_1', 'q_1', 'X', 'x')
    ex2_4.add_transition('q_1', 'q_1', '_', '_')
    ex2_4.add_transition('q_1', 'q_3', '.', '.')
    ex2_4.add_transition('q_2', 'q_1', 'x', 'X')
    ex2_4.add_transition('q_2', 'q_1', 'X', 'X')
    ex2_4.add_transition('q_2', 'q_2', '_', '_')

    # Ex 2.4 [TEST]
    ex2_4.process_sequence('xXX_XxXx.')
    ex2_4.process_sequence('___xXX_XxXx.')

    # Ex 2.5 Phrase sequences w/ one space between ----------------------------
    ex2_5 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])

    ex2_5.add_state(initial=True)  # q_0
    ex2_5.add_state()  # q_1
    ex2_5.add_state()  # q_2
    ex2_5.add_state(accept=True)  # q_3

    ex2_5.add_transition('q_0', 'q_1', 'x', 'x')
    ex2_5.add_transition('q_0', 'q_1', 'X', 'X')
    ex2_5.add_transition('q_0', 'q_1', '_', '_')
    ex2_5.add_transition('q_1', 'q_1', 'x', 'x')
    ex2_5.add_transition('q_1', 'q_1', 'X', 'x')
    ex2_5.add_transition('q_1', 'q_1', '_', '_')
    ex2_5.add_transition('q_1', 'q_3', '.', '.')
    ex2_5.add_transition('q_2', 'q_2', '_', '')
    ex2_5.add_transition('q_2', 'q_1', 'x', 'x')
    ex2_5.add_transition('q_2', 'q_1', 'X', 'X')
    ex2_5.add_transition('q_3', 'q_1', 'x', '_x')
    ex2_5.add_transition('q_3', 'q_1', 'X', '_X')
    ex2_5.add_transition('q_3', 'q_2', '_', '_')

    # Ex 2.5 [TEST]
    ex2_5.process_sequence('Xx_xx.Xxx_x.')
    ex2_5.process_sequence('Xx_xx.Xxx_x.___Xx.')

    # Ex 2.6 Phrase sequences w/ one space between ----------------------------
    ex2_6 = MealyMachine(['x', 'X', '_', '.'], ['x', 'X', '_', '.', ''])

    ex2_6.add_state(initial=True)  # q_0
    ex2_6.add_state()  # q_1
    ex2_6.add_state()  # q_2
    ex2_6.add_state(accept=True)  # q_3

    ex2_6.add_transition('q_0', 'q_1', 'x', 'x')
    ex2_6.add_transition('q_0', 'q_1', 'X', 'X')
    ex2_6.add_transition('q_0', 'q_1', '_', '_')
    ex2_6.add_transition('q_1', 'q_1', 'x', 'x')
    ex2_6.add_transition('q_1', 'q_1', 'X', 'x')
    ex2_6.add_transition('q_1', 'q_1', '_', '_')
    ex2_6.add_transition('q_1', 'q_3', '.', '.')
    ex2_6.add_transition('q_2', 'q_2', '_', '')
    ex2_6.add_transition('q_2', 'q_1', 'x', 'x')
    ex2_6.add_transition('q_2', 'q_1', 'X', 'X')
    ex2_6.add_transition('q_2', 'q_1', '.', 'X')
    ex2_6.add_transition('q_3', 'q_1', 'x', '_x')
    ex2_6.add_transition('q_3', 'q_1', 'X', '_X')
    ex2_6.add_transition('q_3', 'q_2', '_', '_')

    # Ex 2.6 [TEST]
    ex2_6.process_sequence('X._._Xx_x.')
