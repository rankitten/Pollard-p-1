#!/usr/bin/env python3
'Implement the pollard p-1 algorithm with a driver function'

# import numpy as np
import sys
from typing import (
    Optional,
    Tuple,
    Union,
)
from pprint import (
    pprint, )


def is_prime(num: int) -> bool:
    'check whether number is prime'
    return 2**(num - 1) % num == 1 if num > 2 else num == 2


def gcd(left: int, right: int) -> int:
    'Greatest Common Divisor'
    # sanity check
    if left < 0 or right < 0:
        return gcd(abs(left), abs(right))

    # base case
    if right == 0:
        return left

    # recursion
    print(f'GCD L={left} R={right}', file=sys.stderr)
    return gcd(right, left % right)


def pollard_p1(num: int, end: Optional[int] = None) -> Tuple[int, ...]:
    '''
        Use Pollard p-1 to find factors of `num`
    '''

    end_k: Union[int, float] = float('inf') if end is None else end

    def _pollard_p1(curr_num: int) -> Tuple[int, ...]:
        class _ak:
            a: int = 2
            k: int = 2

            def __repr__(self):
                return repr((self.a, self.k))

        ak: _ak = _ak()

        # if number is prime
        if is_prime(curr_num):
            return (curr_num, )

        # calculate a ** (fac(k))
        #   = a ** (k * fac(k-1))
        #   = (a ** fac(k-1)) ** k
        def _pollard_curr_pow(prev_a_pow: int, curr_k: int) -> int:
            res: int = (prev_a_pow**curr_k) % curr_num
            print(f'prev_a={prev_a_pow}, '
                  f'curr_k={curr_k}, '
                  f'res={res}',
                  file=sys.stderr)
            return res

        while ak.k < end_k:
            print(f'ak = {ak}', file=sys.stderr)
            ak.a = _pollard_curr_pow(ak.a, ak.k)

            # nontrivial factor
            _factor: int = gcd(ak.a - 1, curr_num)
            if 1 < _factor < curr_num:
                # found a factor!
                print(f'Factor {_factor} for {num} found! {{{curr_num}}}',
                      file=sys.stderr)

                # recursion
                return (_factor, ) + _pollard_p1(curr_num // _factor)

            print(f'ak = {ak},curr_num={curr_num}', file=sys.stderr)
            ak.k += 1

        return ()

    return _pollard_p1(num)


def main() -> None:
    if len(sys.argv) > 1:
        return

    num: int = int(input('Number to factor: '))
    has_end: bool = input('End somewhere? Y/[n] ').lower() == 'y'
    end: Optional[int] = int(input('Ending k? ')) if has_end else None
    print()

    pprint(pollard_p1(num, end))


if __name__ == '__main__':
    main()
