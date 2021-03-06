#! /usr/bin/env python3

from os import getcwd
from os.path import join
import sys
import unittest
sys.path.insert(0, join(getcwd(), "../"))
import numpy as np

from error import PuzzleProblem
from solvable import _get_inversions, get_solvable, generate_solvable

def fold(grid, l, size, off=0):
	if not len(l):
		return grid
	if grid[off, off] > -1: # move inward
		off += 1
		size -= 2
		if (size == 1):
			grid[off, off] = l[0]
			return grid
		elif size == 0:
			return grid
	grid[off, off:off+size-1] = l[0:size-1]
	return fold(np.rot90(grid), l[size-1:], size, off)

def unfold(grid, size):
	if grid.size == 1:
		return [grid[0, 0]]
	top = grid[0].tolist()
	l = top + unfold(np.rot90(grid[1:]), size-1)
	return l

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

class Valid(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_solvable_if_side_len_odd_start_blank_odd(self):
		a = np.array([[8, 1, 3], [6, 2, 7], [0, 4, 5]])
		self.assertTrue(get_solvable(a, 3))

	def test_solvable_if_side_len_odd_start_blank_even(self):
		a = np.array([[2, 7, 8], [5, 0, 4], [3, 1, 6]])
		self.assertTrue(get_solvable(a, 3))

	def test_solvable_if_side_len_even_goal_blank_even(self):
		a = np.array([[2, 1, 11, 13], [10, 3, 9, 12], [5, 0, 4, 6], [7, 14, 8, 15]])
		self.assertTrue(get_solvable(a, 4))

	def test_solvable_if_side_len_even_goal_blank_odd(self):
		a = np.array([[3, 6, 15, 34, 35, 17], [16, 29, 23, 5, 20, 18], [10, 9, 22, 24, 14, 2], [27, 28, 1, 33, 4, 30], [32, 13, 8, 26, 31, 12], [0, 19, 25, 11, 7, 21]])
		self.assertTrue(get_solvable(a, 6))

	def test_solvable_sidelen_even_goalblank_odd_startblank_odd(self):
		a = np.array([[3, 6, 15, 34, 35, 17], [16, 29, 23, 5, 20, 18], [10, 9, 22, 24, 14, 2], [27, 28, 1, 33, 4, 30], [32, 13, 8, 26, 31, 12], [0, 19, 25, 11, 7, 21]])
		self.assertTrue(get_solvable(a, 6))

	def test_solvable_sidelen_even_goalblank_even_startblank_even(self):
		a = np.array([[7, 0, 8, 10], [3, 1, 2, 12], [14, 9, 5, 13], [4, 6, 11, 15]])
		self.assertTrue(get_solvable(a, 4))

class Unsolvable(unittest.TestCase):
	def test_unsolvable_sidelen_odd_start_odd(self):
		a = np.array([[6, 8, 2], [5, 3, 7], [0, 1, 4]])
		self.assertFalse(get_solvable(a, 3))

	def test_unsolvable_sidelen_odd_start_even(self):
		a = np.array([[8, 2, 1], [7, 0, 4], [6, 5, 3]])
		self.assertFalse(get_solvable(a, 3))

	def test_unsolvable_sidelen_even_start_odd_goal_even(self):
		a = np.array([[1, 14, 13, 6], [0, 12, 15, 2], [9, 11, 10, 8], [7, 3, 5, 4]])
		self.assertFalse(get_solvable(a, 4))

	def test_unsolvable_sidelen_even_start_even_goal_even(self):
		a = np.array([[9, 3, 7, 12], [1, 8, 15, 11], [10, 0, 5, 14], [13, 2, 6, 4]])
		self.assertFalse(get_solvable(a, 4))

class GenerateSolvable(unittest.TestCase):
	def test_makes_solvable_from_any_size(self):
		for i in range(3, 15):
			with self.subTest(i=i):
				g = generate_solvable(i)
				self.assertTrue(get_solvable(g, i))

	def test_too_small_raises(self):
		for i in range(-3, 3):
			with self.subTest(i=i):
				with self.assertRaises(PuzzleProblem):
					generate_solvable(i)

	def test_too_big_raises(self):
		for i in np.random.randint(16, sys.maxsize, size=10):
			with self.subTest(i=i):
				with self.assertRaises(PuzzleProblem, msg=f'{i} did not raise PuzzleProblem'):
					generate_solvable(i)
	
if __name__ == '__main__':
	if '-v' not in sys.argv:
		print(f'{bcolors.OKBLUE} Recommended usage: ./solvable.py -v {bcolors.ENDC}')
	unittest.main()