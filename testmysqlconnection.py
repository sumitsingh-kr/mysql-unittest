import unittest
import os
import mysqlconnection

class testconection(unittest.TestCase):

    def test_check_base_dir_config_file(self):
        actual_result = mysqlconnection.BASE_DIR+"config.json"

        expected_result = os.getcwd()+'config.json'
        self.assertEqual(expected_result,actual_result)

        



    



        






