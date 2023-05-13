from unittest import TestCase

from reflect_strings import *

class TestReflectStrings(TestCase):

    def test_get_parameters(self):
        methods = [
            ".method protected onResume()V",
            ".method public onTrimMemory(I)V",
            ".method public onWindowFocusChanged(Z)V",
            ".method protected updateUnityCommandLineArguments(Ljava/lang/String;)Ljava/lang/String;"
        ]
        params_ = get_parameters(methods[0])
        self.assertEqual(params_, [])

        params_ = get_parameters(methods[1])
        self.assertEqual(["I"],params_)
        params_ = get_parameters(methods[2])
        self.assertEqual(["Z"],params_)
        params_ = get_parameters(methods[3])
        self.assertEqual(["Ljava/lang/String;"],params_)


