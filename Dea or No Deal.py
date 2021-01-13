"""

@author: Megan McNamee
"""

#!/usr/bin/env python3

"""Simulate the Monty Hall problem.

"""

import argparse, random

def simulate(num_cases, switch, verbose):
    """(int, bool): bool

    Carry out the game for one contestant.  If 'switch' is True,
    the contestant will switch their chosen case when offered the chance.
    Returns a Boolean value telling whether the simulated contestant won.
    """

    # Doors are numbered from 0 up to num_cases-1 (inclusive).

    # Randomly choose the case hiding the prize.
    winning_case = random.randint(0, num_cases-1)
    if verbose:
        print('Prize is behind case {}'.format(winning_case+1))

    # The contestant picks a random case, too.
    choice = random.randint(0, num_cases-1)
    if verbose:
        print('Contestant chooses case {}'.format(choice+1))

    # The host opens all but two cases.
    closed_cases = list(range(num_cases))
    while len(closed_cases) > 2:
        # Randomly choose a case to open.
        case_to_remove = random.choice(closed_cases)

        # The host will never open the winning case, or the case
        # chosen by the contestant.
        if case_to_remove == winning_case or case_to_remove == choice:
            continue

        # Remove the case from the list of closed cases.
        closed_cases.remove(case_to_remove)
        if verbose:
            print('Host opens case {}'.format(case_to_remove+1))

    # There are always two cases remaining.
    assert len(closed_cases) == 2

    # Does the contestant want to switch their choice?
    if switch:
        if verbose:
            print('Contestant switches from case {} '.format(choice+1), end='')

        # There are two closed cases left.  The contestant will never
        # choose the same case, so we'll remove that case as a choice.
        available_cases = list(closed_cases) # Make a copy of the list.
        available_cases.remove(choice)

        # Change choice to the only case available.
        choice = available_cases.pop()
        if verbose:
            print('to {}'.format(choice+1))

    # Did the contestant win?
    won = (choice == winning_case)
    if verbose:
        if won:
            print('Contestant WON', end='\n\n')
        else:
            print('Contestant LOST', end='\n\n')
    return won


def main():
    # Get command-line arguments
    parser = argparse.ArgumentParser(
        description='simulate the Monty Hall problem')
    parser.add_argument('--cases', default=26, type=int, metavar='int',
                        help='number of cases offered to the contestant')
    parser.add_argument('--trials', default=100, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--verbose', default=True, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()

    print('Simulating {} trials...'.format(args.trials))

    # Carry out the trials
    winning_non_switchers = 0
    winning_switchers = 0
    for i in range(args.trials):
        # First, do a trial where the contestant never switches.
        won = simulate(args.cases, switch=False, verbose=args.verbose)
        if won:
            winning_non_switchers += 1

        # Next, try one where the contestant switches.
        won = simulate(args.cases, switch=True, verbose=args.verbose)
        if won:
            winning_switchers += 1

    print('    Switching won {0:5} times out of {1} ({2}% of the time)'.format(
            winning_switchers, args.trials,
            (winning_switchers / args.trials * 100 ) ))
    print('Not switching won {0:5} times out of {1} ({2}% of the time)'.format(
            winning_non_switchers, args.trials,
            (winning_non_switchers / args.trials * 100 ) ))


if __name__ == '__main__':
    main()
