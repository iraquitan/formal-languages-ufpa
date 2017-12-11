# -*- coding: utf-8 -*-


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

    def process_sequence(self, sequence, verbose=True):
        if len(self.transitions) == 0 or len(self.states) == 0:
            raise RuntimeError('{} has no states or transitions.'
                               .format(self.__class__.__name__))
        if self.initial_state is None:
            raise RuntimeError('{} has no initial state.'
                               .format(self.__class__.__name__))
        if len(self.get_accept_states()) == 0:
            raise RuntimeError('{} has no accept states.'
                               .format(self.__class__.__name__))
        if verbose:
            print('Processing "{}"'.format(sequence))
        cur_state = self.initial_state
        if verbose:
            print('Transitions:')
        for s in sequence:
            if s not in self.alphabet:
                raise ValueError('sequence symbol {0} not in {1} alphabet.'
                                 .format(s, self.__class__.__name__))
            for next_, symbol in cur_state.transitions:
                if s == symbol:
                    if verbose:
                        print('\t({from_.name}, {symbol}) -> {to_.name}'
                              .format(from_=cur_state, symbol=s, to_=next_))
                    cur_state = next_
                    break
            else:
                if verbose:
                    print('\tReject', end='\t')
                    print('{cl_name} without transition for {state.name} '
                          'with symbol {symbol}.'
                          .format(cl_name=self.__class__.__name__,
                                  state=cur_state, symbol=s))
                return False

        if cur_state.accept:
            if verbose:
                print('\tAccept')
            return True
        else:
            if verbose:
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
        # Clean states transitions
        for s in self.states:
            for to_, symbol in s.transitions:
                if to_ not in useful_states:
                    s.transitions.remove((to_, symbol))
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

        equiv_pairs = [pairs[e] for e in equiv]
        new_states = []
        for i in range(len(equiv_pairs)):
            cur_pair_i = equiv_pairs[i]
            new_state = cur_pair_i
            for j in range(len(equiv_pairs)):
                if i != j:
                    cur_pair_j = equiv_pairs[j]
                    if len(cur_pair_i.intersection(cur_pair_j)) != 0:
                        new_state = new_state.union(cur_pair_j)
            if new_state not in new_states:
                new_states.append(new_state)

        # Create new states
        for ns in new_states:
            new_name = ','.join([s.name for s in ns])
            is_initial = True if any([s.initial for s in ns]) else False
            is_accept = True if any([s.accept for s in ns]) else False
            for s in ns:
                if s.initial:
                    self.initial_state = None
                self.states.remove(s)
            self.add_state(new_name, initial=is_initial, accept=is_accept)

        # Transitions
        for ns in new_states:
            transitions = set()
            new_name = ','.join([s.name for s in ns])
            for s in ns:
                for to_, symbol in s.transitions:
                    ck = []
                    for ns2 in new_states:
                        new_name2 = ','.join([s.name for s in ns2])
                        if to_.name in new_name2 and symbol not in [s for t, s in transitions]:
                            transitions.add((new_name2, symbol))
                        elif to_.name not in new_name2 and symbol not in [s for t, s in transitions]:
                            ck.append(True)
                    if all(ck) and len(ck) == len(new_states):
                        transitions.add((to_.name, symbol))

            for to_, symbol in transitions:
                self.add_transition(new_name, to_, symbol)

        ns_names = [','.join([s.name for s in ns]) for ns in new_states]
        for s in self.states:
            transitions = set()
            if s.name in ns_names:
                continue
            for to_, symbol in s.transitions:
                ck = []
                for ns2 in new_states:
                    new_name2 = ','.join([s.name for s in ns2])
                    if to_.name in new_name2 and symbol not in [s for t, s in transitions]:
                        transitions.add((new_name2, symbol))
                    elif to_.name not in new_name2 and symbol not in [s for t, s in transitions]:
                        ck.append(True)
                if all(ck) and len(ck) == len(new_states):
                    transitions.add((to_.name, symbol))
            # remove transitions
            s.transitions = []
            for to_, symbol in transitions:
                self.add_transition(s.name, to_, symbol)
