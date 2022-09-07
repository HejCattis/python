#!/usr/bin/env python3
"""
An autogenerated testfile for python.
"""

import unittest
from io import StringIO
import os
import sys
from unittest.mock import patch
from unittest import TextTestRunner
from examiner import ExamTestCase, ExamTestResult, tags
from examiner import import_module, find_path_to_assignment


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = find_path_to_assignment(FILE_DIR)

if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

# Path to file and basename of the file to import
main = import_module(REPO_PATH, 'main')



class Test3Marvin3Main(ExamTestCase):
    """
    Each assignment has 1 testcase with multiple asserts.
    The different asserts https://docs.python.org/3.6/library/unittest.html#test-cases
    """

    link_to_assignment = "https://dbwebb.se/uppgift/din-egen-chattbot-marvin-steg-3-v4"

    PICKUP = ["inv pick car", "", "inv pick house", ""]

    @classmethod
    def setUpClass(cls):
        """
        To find all relative files that are read or written to.
        """
        os.chdir(REPO_PATH)


    def check_print_contain(self, inp, correct):
        """
        One function for testing print input functions.
        """
        with patch("builtins.input", side_effect=inp):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main.main()
                for val in correct:
                    str_data = fake_out.getvalue()
                    self.assertIn(val, str_data)


    def check_print_not_contain(self, inp, correct):
        """
        One function for testing print input functions.
        """
        with patch("builtins.input", side_effect=inp):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main.main()
                for val in correct:
                    str_data = fake_out.getvalue()
                    self.assertNotIn(val, str_data, ["Förväntar att följande inte finns med i utskrifter:", "Fick med följande:"])



    @tags("menu", "inv")
    def test_inv_command_empty(self):
        """
        Testar att anropa 'inv kommandot' i main.py.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = ["inv", "", "q"]

        self.check_print_contain(self._multi_arguments, ["0", "[]"])



    @tags("menu", "pick")
    def test_pick_command(self):
        """
        Testar att anropa 'inv pick' med och utan index.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = Test3Marvin3Main.PICKUP + [
            "inv pick bike 1", "", "q"
        ]

        correct = ["car", "", "house", "bike", "1"]
        self.check_print_contain(self._multi_arguments, correct)
        self.check_print_not_contain(self._multi_arguments, ["Error"])



    @tags("menu", "drop")
    def test_pick_and_drop(self):
        """
        Testar både 'inv pick' och 'inv drop' kommandon.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = Test3Marvin3Main.PICKUP + [
            "inv drop car", "", "q"
        ]

        self.check_print_contain(self._multi_arguments, ["car"])
        self.check_print_not_contain(self._multi_arguments, ["Error"])



    @tags("menu", "drop")
    def test_pick_and_drop_error(self):
        """
        Testar 'inv drop' på ett icke existerande värde.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = Test3Marvin3Main.PICKUP + [
            "inv drop bike", "", "q"
        ]

        self.check_print_contain(self._multi_arguments, ["bike"])
        self.check_print_contain(self._multi_arguments, ["Error"])



    @tags("menu", "swap")
    def test_pick_and_swap(self):
        """
        Testar 'inv pick och 'inv swap' kommandot
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = Test3Marvin3Main.PICKUP + [
            "inv swap car house", "", "q"
        ]

        self.check_print_contain(self._multi_arguments, ["house", "car"])
        self.check_print_not_contain(self._multi_arguments, ["Error"])



    @tags("menu", "swap")
    def test_pick_and_swap_error(self):
        """
        Testar pick och swap kommandot som ska ge error.
        Använder följande som input:
        {arguments}
        Förväntar att följande finns med i utskrift:
        {correct}
        Fick följande:
        {student}
        """
        self.norepr = True
        self._multi_arguments = Test3Marvin3Main.PICKUP + [
            "inv swap bike house", "", "q"
        ]

        self.check_print_contain(self._multi_arguments, ["bike"])
        self.check_print_contain(self._multi_arguments, ["Error"])





if __name__ == '__main__':
    runner = TextTestRunner(resultclass=ExamTestResult, verbosity=2)
    unittest.main(testRunner=runner, exit=False)
