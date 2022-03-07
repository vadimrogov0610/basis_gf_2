from typing import List, Tuple, Set, Dict
from bisect import bisect_left as bl


class Basis:
    # by default making sort and gauss
    def __init__(self, ab: List[int], sg=True):
        self.ab = ab
        if sg:
            self.sort_gauss()

    def __str__(self):
        return f'{self.ab}'

    def __repr__(self):
        return f'{self.ab}'

    def __len__(self):
        return len(self.ab)

    def __iter__(self):
        return iter(self.ab)

    def __bool__(self):
        return bool(self.ab)

    @property
    def to_set(self) -> Set[int]:
        return set(self.ab)

    def copy(self):
        return Basis(self.ab.copy(), False)

    @classmethod
    def empty(cls):
        return Basis([], False)

    # returns basis with strictly descending order by bit_length
    def sort_gauss(self):
        if self.ab:
            self.ab.sort(reverse=True)
            n = len(self.ab)
            D = {}
            for i in range(n - 1):
                boo = False
                if self.ab[i].bit_length() == self.ab[i + 1].bit_length():
                    self.ab[i] ^= self.ab[i + 1]
                    boo = True
                b = self.ab[i].bit_length()
                while b in D:
                    self.ab[i] ^= D[b]
                    b = self.ab[i].bit_length()
                    boo = True
                if boo and b:
                    D[b] = self.ab[i]
            b = self.ab[n - 1].bit_length()
            while b in D:
                self.ab[n - 1] ^= D[b]
                b = self.ab[n - 1].bit_length()
            self.ab.sort(reverse=True)
            if 0 in self.ab:
                del self.ab[self.ab.index(0):]

    def find_intersection_dimension(self, other):
        u = self.ab + other.ab
        if not u:
            return 0
        u.sort(reverse=True)
        n = len(u)
        count = 0
        D = {}
        for i in range(n - 1):
            boo = False
            if u[i].bit_length() == u[i + 1].bit_length():
                u[i] ^= u[i + 1]
                boo = True
            b = u[i].bit_length()
            while b in D:
                u[i] ^= D[b]
                b = u[i].bit_length()
                boo = True
            if boo and b:
                D[b] = u[i]
            if not b:
                count += 1
        b = u[n - 1].bit_length()
        while b in D:
            u[n - 1] ^= D[b]
            b = u[n - 1].bit_length()
        if not b:
            count += 1
        return count

    # returns (index, j_new) for self.ab.insert(index, j_new)
    def find_place(self, j: int):
        n = len(self.ab)
        a = [i.bit_length() for i in reversed(self.ab)]
        while True:
            jl = j.bit_length()
            index = bl(a, jl)
            if (len(a) != index) and (jl == a[index]):
                j ^= self.ab[n - 1 - index]
                del a[index + 1:]  # a = a[:index + 1]
            else:
                break
        return n - index, j

    # basis of sum
    def __add__(self, other):
        return Basis(self.ab + other.ab)

    # basis of intersection
    def __mul__(self, other):
        TL = [(x, x) for x in self.ab] + [(x, 0) for x in other.ab]
        if not TL:
            return Basis.empty()
        TL.sort(key=lambda t: -t[0])
        lst, left = map(list, zip(*TL))
        ans = []
        n = len(lst)
        D = {}
        D_left = {}
        for i in range(n - 1):
            boo = False
            if lst[i].bit_length() == lst[i + 1].bit_length():
                lst[i] ^= lst[i + 1]
                left[i] ^= left[i + 1]
                boo = True
            b = lst[i].bit_length()
            while b in D:
                lst[i] ^= D[b]
                left[i] ^= D_left[b]
                b = lst[i].bit_length()
                boo = True
            if boo and b:
                D[b] = lst[i]
                D_left[b] = left[i]
            if not b:
                ans.append(left[i])
        b = lst[n - 1].bit_length()
        while b in D:
            lst[n - 1] ^= D[b]
            left[n - 1] ^= D_left[b]
            b = lst[n - 1].bit_length()
        if not b:
            ans.append(left[n - 1])
        return Basis(ans)

    # adding element to basis not breaking structure; element can be modified
    def add(self, num: int):
        index, num = self.find_place(num)
        if num:
            self.ab.insert(index, num)

    # extending basis with list of numbers
    # type(lst) -- set всвязи с тем, что в методах так лучше
    def extend(self, lst):
        self.ab.extend(lst)
        self.sort_gauss()

    # returns True if self.ab extended
    def extend_bool(self, lst):
        le = len(self.ab)
        self.ab.extend(lst)
        self.sort_gauss()
        return len(self.ab) > le

    @property
    def contains_one(self) -> bool:
        if not self.ab:
            return False
        return self.ab[-1] == 1

    # does num belongs to linear span of self
    def belongs(self, num: int) -> bool:
        return self.find_place(num)[1] == 0

    def mod_zeros(self, num: int) -> int:
        lead = [1 << (tt.bit_length() - 1) for tt in self.ab]
        for t, q in zip(self.ab, lead):
            if num & q:
                num ^= t
            right = num & (q - 1)
            num = ((num ^ right) >> 1) ^ right
        return num

    def mod_zeros_with_gaps(self, num: int) -> int:
        lead = [1 << (tt.bit_length() - 1) for tt in self.ab]
        for t, q in zip(self.ab, lead):
            if num & q:
                num ^= t
        return num

    def reverse_gauss(self):
        n = len(self.ab)
        for i in range(n - 1, 0, -1):
            power = 1 << (self.ab[i].bit_length() - 1)
            for j in range(i):
                if self.ab[j] & power:
                    self.ab[j] ^= self.ab[i]


"""
Some old versions:


def old_mul(self, other):
    lst = self.ab + other.ab
    left = self.ab + [0] * len(other.ab)
    lead = [w.bit_length() - 1 for w in lst]
    nn = len(lst)
    for i in range(nn):
        l_m = lead[i:]
        q = max(l_m)
        if q == -1:
            return Basis(left[i:])
        ind = l_m.index(q) + i
        lst[i], lst[ind] = lst[ind], lst[i]
        left[i], left[ind] = left[ind], left[i]
        lead[i], lead[ind] = lead[ind], lead[i]
        for j in range(i + 1, nn):
            if q == lead[j]:
                lst[j] ^= lst[i]
                left[j] ^= left[i]
                lead[j] = lst[j].bit_length() - 1
    return Basis.empty()


def sort_gauss(self):
    self.ab.sort(reverse=True)
    nn = len(self.ab)
    lead = [w.bit_length() - 1 for w in self.ab]
    for ii in range(nn):
        l_m = lead[ii:]
        q = max(l_m)
        if q == -1:
            del self.ab[ii:]
            break
        ind = l_m.index(q) + ii
        self.ab[ii], self.ab[ind] = self.ab[ind], self.ab[ii]
        lead[ii], lead[ind] = lead[ind], lead[ii]
        for jj in range(ii + 1, nn):
            if q == lead[jj]:
                self.ab[jj] ^= self.ab[ii]
                lead[jj] = self.ab[jj].bit_length() - 1
"""
