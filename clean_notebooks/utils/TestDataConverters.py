import unittest
from label_converters import *

class BasicTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        self.bstate1 = 'r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1'
        self.bstate2 = '3k3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1'
        self.bstate3 = 'rnbqkbnr-pppppppp-8-8-8-8-PPPPPPPP-RNBQKBNR'
        self.bstate4 = 'rnbqkbnr.?.pppppppp.?.8.?.8.?.8.?.8.?.PPPPPPPP.?.RNBQKBNR'
        
    # executed after each test
    def tearDown(self):
        pass
    
    def test_input1(self):
        delimiter='/'
        flat = convert_FEN_to_2d_char_array(self.bstate1,
                                            delimiter=delimiter)
        three_d = convert_to_3d_one_hot_array(flat, null_char = delimiter)
        back2flat = convert_one_hot_array_to_3d(three_d, null_char = delimiter)
        back_to_ef = convert_2d_char_array_to_FEN(back2flat, 
                                                  null_char = delimiter)
        self.assertEqual(str(flat), str(back2flat))
        self.assertEqual(str(self.bstate1), str(back_to_ef))
    
    def test_input2(self):
        delimiter='/'

        flat = convert_FEN_to_2d_char_array(self.bstate2,
                                            delimiter=delimiter)
        three_d = convert_to_3d_one_hot_array(flat, null_char = delimiter)
        back2flat = convert_one_hot_array_to_3d(three_d, null_char = delimiter)
        back_to_ef = convert_2d_char_array_to_FEN(back2flat, 
                                                  null_char = delimiter)
        self.assertEqual(str(flat), str(back2flat))
        self.assertEqual(str(self.bstate2), str(back_to_ef))

    def test_input3(self):
        delimiter='-'
        flat = convert_FEN_to_2d_char_array(self.bstate3,
                                            delimiter=delimiter)
        three_d = convert_to_3d_one_hot_array(flat, null_char = delimiter)
        back2flat = convert_one_hot_array_to_3d(three_d, null_char = delimiter)
        back_to_ef = convert_2d_char_array_to_FEN(back2flat, 
                                                  null_char = delimiter)
        self.assertEqual(str(flat), str(back2flat))
        self.assertEqual(str(self.bstate3), str(back_to_ef))
    
    def test_input4(self):
        delimiter='.?.'
        flat = convert_FEN_to_2d_char_array(self.bstate4,
                                            delimiter=delimiter)
        three_d = convert_to_3d_one_hot_array(flat, null_char = delimiter)
        back2flat = convert_one_hot_array_to_3d(three_d, null_char = delimiter)
        back_to_ef = convert_2d_char_array_to_FEN(back2flat, 
                                                  null_char = delimiter)
        self.assertEqual(str(flat), str(back2flat))
        self.assertEqual(str(self.bstate4), str(back_to_ef))

    def test_bad_inputs(self):
        self.assertRaises(AssertionError, 
                          convert_FEN_to_2d_char_array, 'a')
        self.assertRaises(ValueError, 
                          convert_FEN_to_2d_char_array, 
                          'r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b')
        self.assertRaises(ValueError, 
                          convert_FEN_to_2d_char_array, 
                          'r1bk3r/p2pBp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1')
    
if __name__ == "__main__":
    unittest.main()