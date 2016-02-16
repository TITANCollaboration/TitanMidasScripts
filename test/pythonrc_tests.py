#!/usr/bin/env python
"""Unit tests for the pythonrc module."""

import mock
from unittest import TestCase
import numpy as np
import pythonrc as prc


class StandAloneTests(TestCase):
    """Test stand-alone module functions."""

    def test_StringToList_splitSemiColon(self):
        """Test StringToList"""
        teststr = "1;2 ; 3    ;     4"
        expected = ['1', '2', '3', '4']
        self.assertEqual(prc.StringToList(teststr), expected)

    def test_StringToList_splitComma(self):
        """Test StringToList"""
        teststr = "1,2 , 3    ,     4"
        expected = ['1', '2', '3', '4']
        self.assertEqual(prc.StringToList(teststr, ","), expected)

    def test_StringListToFloatList(self):
        """Test StringListToFloatList"""
        teststr = prc.StringToList("1;2 ; 3    ;     4")
        expected = [1.0, 2., 3., 4.0]
        self.assertEqual(prc.StringListToFloatList(teststr), expected)

    def test_StringListToFloatList_trapVoltage(self):
        """Test StringListToFloatList for simulated trap volatges"""
        teststr = prc.StringToList("(1,1) (2,2)(3,3)     (4    ,    4)")
        expected = [np.array([[1, 1], [2, 2], [3, 3], [4, 4]])]
        result = prc.StringListToFloatList(teststr)
        print expected
        print result
        for i in range(expected[0].shape[0]):
            #print result[i], expected[i]
            self.assertTupleEqual(tuple(result[0][i]), tuple(expected[0][i]))

    def test_GetVariableStepSize(self):
        """Test GetVariableStepSize"""
        teststep = prc.GetVariableStepSize(0.0, 10.0, 11)
        expected = 1.0
        self.assertEqual(teststep, expected)

        teststep = prc.GetVariableStepSize(1, 10, 10)
        expected = 1.0
        self.assertEqual(teststep, expected)

    def test_GetVariableStepSize_trapVoltage(self):
        """Test GetVariableStepSize for simulated trap voltages"""
        trapStart = np.array([2.0, 0.0000])
        trapEnd = np.array([2.0, 10.0000])
        numStep = 11
        expected = (0.0, 1.0)
        result = prc.GetVariableStepSize(trapStart, trapEnd, numStep)
        self.assertEqual(tuple(result), expected)

    def test_NextVariableSetPoint(self):
        """Test NextVariableSetPoint"""
        test = prc.NextVariableSetPoint(0.0, 10.0, 11, 2)
        expected = 2.0
        self.assertEqual(test, expected)

    def test_NextVariableSetPoint_trapVoltage(self):
        """Test NextVariableSetPoint for simulated trap voltages"""
        # test stepping
        trapStart = np.array([2.0, 0.0000])
        trapEnd = np.array([2.0, 10.0000])
        numStep = 11
        currstep = 2
        expected = (2.0, 2.0)
        result = prc.NextVariableSetPoint(trapStart,
                                          trapEnd,
                                          numStep,
                                          currstep)
        self.assertEqual(tuple(result), expected)

        # test no step
        trapEnd = np.array([2.0, 0.0])
        expected = (2.0, 0.0)
        result = prc.NextVariableSetPoint(trapStart,
                                          trapEnd,
                                          numStep,
                                          currstep)
        self.assertEqual(tuple(result), expected)

    def test_ConvertValueToString(self):
        """Test ConvertValueToString"""
        self.assertEqual(prc.ConvertValueToString(1.0), '1.0')

    def test_ConvertValueToString_trapVoltage(self):
        """Test ConvertValueToString for simulated trap volatges"""
        testval = np.array([[1, 1], [2, 2.0], [3, 3], [4.0, 4]])
        expected = "(1,1.0000) (2,2.0000) (3,3.0000) (4,4.0000)"
        self.assertEqual(prc.ConvertValueToString(testval), expected)


# Exception class to replace pythonmidas exceptions
class KeyNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DependentTests(TestCase):
    """Test pythonrc calls to pythonmidas to ensure the correct arguments
    are passed."""

    @mock.patch('pythonrc.datetime')
    def test_GetTime(self, mock_datetime):
        # Here was mock the calls to the datetime module
        mDate = mock.MagicMock()
        mDate.strftime = mock.MagicMock(return_value="stringtime")
        mock_datetime.datetime.now.return_value = mDate

        result = prc.GetTime()
        print result
        self.assertEqual(result, "stringtime")

    @mock.patch('pythonrc.Midas')
    def test_GetVarName(self, mock_midas):
        mock_midas.varget.return_value = "True"
        rval = prc.GetVarName("perlVarName")

        self.assertEqual(rval, "True")
        mock_midas.varget.assert_called_with(prc.ControlVarPath +
                                             "perlVarName")

    @mock.patch('pythonrc.Midas')
    def test_MidasSetVar(self, mock_midas):
        varPath = "/testPath"
        varValue = 1.0

        prc.MidasSetVar(varPath, varValue)
        mock_midas.varset.assert_called_with(varPath, str(varValue))

        mock_midas.KeyNotFound = KeyNotFound
        mock_midas.varset.side_effect = mock_midas.KeyNotFound("Key not found")
        self.assertRaises(Exception, prc.MidasSetVar)
        try:
            prc.MidasSetVar(varPath, varValue)
        except:
            mock_midas.sendmessage.assert_called_with('pythonrc',
                                                      "Key not found")

        mock_midas.FailedCommand = KeyNotFound
        mock_midas.varset.side_effect = \
            mock_midas.FailedCommand("Failed Command")
        self.assertRaises(Exception, prc.MidasSetVar)
        try:
            prc.MidasSetVar(varPath, varValue)
        except:
            mock_midas.sendmessage.assert_called_with('pythonrc',
                                                      "Failed Command")

    @mock.patch('pythonrc.Midas')
    def test_ChangeTune(self, mock_midas):
        mock_midas.dirlist.return_value = [["a", 1.0]]
        mock_midas.varget.return_value = "varname"

        prc.ChangeTune("a tune")

        # Probably too many tests here, since I've already tested
        # some of these functions....
        mock_midas.dirlist.assert_called_with(prc.TunePath + "a tune")
        mock_midas.varget.assert_called_with(prc.ControlVarPath + "a")
        mock_midas.varset.assert_called_with("varname", "1.0")
        mock_midas.sendmessage.assert_called_with("pythonrc",
                                                  "Changed tune to: "
                                                  + "a tune")

    @mock.patch('pythonrc.ChangeTune')
    @mock.patch('pythonrc.Midas')
    def test_TuneSwitch(self, mock_midas, mock_ChangeTune):
        # Currently the variable order that use varget are:
        # RunN, Runcurrn, Tunes, currn
        mock_midas.varget.side_effect = [11, 1, "tune1; tune2", 2]

        result = prc.TuneSwitch()
        self.assertEqual(result, "Tune is \"tune1\"")

        # Check calls to varget:
        expected = [mock.call(prc.RunControlPath + "RCTotalRuns"),
                    mock.call(prc.RunControlPath + "RCCurrentRun"),
                    mock.call(prc.TuneSwitchPath + "TunesList"),
                    mock.call(prc.TuneSwitchPath + "CurrentTuneIndex")]

        self.assertEqual(mock_midas.varget.call_args_list, expected)
        self.assertEqual(mock_midas.varget.call_count, 4)

        # Check calls to varset
        expected = [mock.call(prc.RunControlPath + "RCCurrentRun", 2),
                    mock.call(prc.TuneSwitchPath + "CurrentTuneIndex", 1),
                    mock.call(prc.TuneSwitchPath + "CurrentTuneName", "tune1")]

        self.assertEqual(mock_midas.varset.call_args_list, expected)
        self.assertEqual(mock_midas.varset.call_count, 3)

        # Check call to ChangeTune
        mock_ChangeTune.assert_called_with("tune1")

        # Reset and do it again, but such that we need to loop back to 1
        mock_midas.reset_mock()
        mock_ChangeTune.reset_mock()

        mock_midas.varget.side_effect = [11, 11, "tune1; tune2", 2]

        result = prc.TuneSwitch()
        self.assertEqual(result, "Tune is \"tune1\"")

        # Check calls to varget:
        expected = [mock.call(prc.RunControlPath + "RCTotalRuns"),
                    mock.call(prc.RunControlPath + "RCCurrentRun"),
                    mock.call(prc.TuneSwitchPath + "TunesList"),
                    mock.call(prc.TuneSwitchPath + "CurrentTuneIndex")]

        self.assertEqual(mock_midas.varget.call_args_list, expected)
        self.assertEqual(mock_midas.varget.call_count, 4)

        expected = [mock.call(prc.RunControlPath + "RCCurrentRun", 1),
                    mock.call(prc.TuneSwitchPath + "CurrentTuneIndex", 1),
                    mock.call(prc.TuneSwitchPath + "CurrentTuneName", "tune1")]
        self.assertEqual(mock_midas.varset.call_args_list, expected)

        # Check call to ChangeTune
        mock_ChangeTune.assert_called_with("tune1")

    @mock.patch('pythonrc.MidasSetVar')
    @mock.patch('pythonrc.GetVarName')
    @mock.patch('pythonrc.Midas')
    def test_Scan1D(self, mock_midas, mock_GetVarName, mock_MidasSetVar):
        # Current order of calls for pythonmidas.varget:
        # Scan1Dn, Scan1Dcurrn, Variables, Start, Stop
        mock_midas.varget.side_effect = [11, 11, "var1; var2",
                                         "0; 10", "10 ; 0"]

        mock_GetVarName.side_effect = [prc.ControlVarPath + "var1",
                                       prc.ControlVarPath + "var2"]

        result = prc.Scan1D()
        expected = "var1=0.0;var2=10.0;"

        self.assertEqual(result, expected)

        expected = [mock.call(prc.RunControlPath + "RCTotalRuns"),
                    mock.call(prc.RunControlPath + "RCCurrentRun"),
                    mock.call(prc.Scan1DPath + "Variables"),
                    mock.call(prc.Scan1DPath + "VarStart"),
                    mock.call(prc.Scan1DPath + "VarStop")]

        self.assertEqual(mock_midas.varget.call_args_list, expected)
        self.assertEqual(mock_midas.varget.call_count, 5)

        expected = [mock.call(prc.RunControlPath + "RCCurrentRun", 1)]

        self.assertEqual(mock_midas.varset.call_args_list, expected)
        self.assertEqual(mock_midas.varset.call_count, 1)

        expected = [mock.call("var1"), mock.call("var2")]

        self.assertEqual(mock_GetVarName.call_args_list, expected)
        self.assertEqual(mock_GetVarName.call_count, 2)

        expected = [mock.call(prc.ControlVarPath + "var1", 0.0),
                    mock.call(prc.ControlVarPath + "var2", 10.0)]

        self.assertEqual(mock_MidasSetVar.call_args_list, expected)
        self.assertEqual(mock_MidasSetVar.call_count, 2)

    @mock.patch('pythonrc.GetVarName')
    @mock.patch('pythonrc.MidasSetVar')
    @mock.patch('pythonrc.Midas')
    def test_Scan2D(self, mock_midas, mock_MidasSetVar, mock_GetVarName):
        mock_midas.varget.side_effect = ["22", "22",
                                         "var1", "0", "10", "11", "1",
                                         "var2", "100", "0", "2", "2"]

        expected = "var1=1.0;;var2=100.0;"

        self.assertEqual(prc.Scan2D(), expected)

        expected = [mock.call(prc.RunControlPath + "RCCurrentRun", 1),
                    mock.call(prc.Scan2DPath + "Var1CurrentStep", 2),
                    mock.call(prc.Scan2DPath + "Var2CurrentStep", 1)]

        self.assertEqual(mock_midas.varset.call_args_list, expected)
        self.assertEqual(mock_midas.varset.call_count, 3)
        self.assertEqual(mock_MidasSetVar.call_count, 2)

        mock_midas.reset_mock()
        mock_MidasSetVar.reset_mock()
        mock_GetVarName.reset_mock()

        mock_midas.varget.side_effect = ["22", "22",
                                         "var1", "0", "10", "11", "11",
                                         "var2", "100", "0", "2", "2"]

        expected = "var1=0.0;;var2=100.0;"

        self.assertEqual(prc.Scan2D(), expected)

        expected = [mock.call(prc.RunControlPath + "RCCurrentRun", 1),
                    mock.call(prc.Scan2DPath + "Var1CurrentStep", 1),
                    mock.call(prc.Scan2DPath + "Var2CurrentStep", 1)]

    @mock.patch('pythonrc.LogScanError')
    @mock.patch('pythonrc.LogSwitchedTune')
    @mock.patch('pythonrc.time')
    @mock.patch('pythonrc.Scan1D')
    @mock.patch('pythonrc.Scan2D')
    @mock.patch('pythonrc.TuneSwitch')
    @mock.patch('pythonrc.ChangeTune')
    @mock.patch('pythonrc.LogScanStart')
    @mock.patch('pythonrc.LogScanVarStep')
    @mock.patch('pythonrc.LogScanStop')
    @mock.patch('pythonrc.sys')
    @mock.patch('pythonrc.Midas')
    def test_main_cmdlineArg(self, mock_midas, mock_sys, mock_logscanstop,
                             mock_logscanvarstep, mock_logscanstart,
                             mock_ChangeTune, mock_TuneSwitch, mock_Scan2D,
                             mock_Scan1D, mock_time, mock_logswitchedtune,
                             mock_logscanerror):
        mocks = [mock_midas, mock_sys, mock_logscanstop,
                 mock_logscanvarstep, mock_logscanstart,
                 mock_ChangeTune, mock_TuneSwitch, mock_Scan2D,
                 mock_Scan1D, mock_time, mock_logswitchedtune,
                 mock_logscanerror]
        # First test starting a PerlRC scan
        mock_sys.argv = ["ProgramName", "start"]

        # Test with Scan1D
        mock_midas.varget.side_effect = ["n", "Scan1D"]

        mock_Scan1D.return_value = "called"

        # call main()
        prc.main()

        mock_midas.varset.assert_called_with(prc.RCActive, 'y')
        mock_Scan1D.assert_called_once_with()
        mock_Scan2D.assert_not_called()
        mock_TuneSwitch.assert_not_called()
        mock_logscanstart.assert_called_once_with()
        mock_logscanvarstep.assert_called_once_with("called")
        mock_logscanstop.assert_called_once_with()
        mock_time.sleep.assert_called_once_with(1)
        mock_midas.startrun.assert_called_once_with()

        map(lambda x: x.reset_mock(), mocks)

        # First test starting a PerlRC scan
        mock_sys.argv = ["ProgramName", "start"]

        # Test with Scan2D
        mock_midas.varget.side_effect = ["n", "Scan2D"]

        mock_Scan2D.return_value = "called"

        # call main()
        prc.main()

        mock_midas.varset.assert_called_with(prc.RCActive, 'y')
        mock_Scan1D.assert_not_called()
        mock_Scan2D.assert_called_once_with()
        mock_TuneSwitch.assert_not_called()
        mock_logscanstart.assert_called_once_with()
        mock_logscanvarstep.assert_called_once_with("called")
        mock_logscanstop.assert_called_once_with()
        mock_time.sleep.assert_called_once_with(1)
        mock_midas.startrun.assert_called_once_with()

        map(lambda x: x.reset_mock(), mocks)

        # First test starting a PerlRC scan
        mock_sys.argv = ["ProgramName", "start"]

        # Test with Scan2D
        mock_midas.varget.side_effect = ["n", "TuneSwitch"]

        mock_TuneSwitch.return_value = "called"

        # call main()
        prc.main()

        mock_midas.varset.assert_called_with(prc.RCActive, 'y')
        mock_Scan1D.assert_not_called()
        mock_Scan2D.assert_not_called()
        mock_TuneSwitch.assert_called_once_with()
        mock_logscanstart.assert_called_once_with()
        mock_logscanvarstep.assert_called_once_with("called")
        mock_logscanstop.assert_called_once_with()
        mock_time.sleep.assert_called_once_with(1)
        mock_midas.startrun.assert_called_once_with()

        map(lambda x: x.reset_mock(), mocks)

        # Scan1D/Scan2D/TuneSwitch raises an Exception
        mock_sys.argv = ["ProgramName", "start"]
        mock_midas.varget.side_effect = ["n", "TuneSwitch"]

        mock_TuneSwitch.side_effect = Exception

        # call main()
        prc.main()

        expected = [mock.call(prc.RCActive, 'y'),
                    mock.call(prc.RCActive, 'n')]

        self.assertEqual(mock_midas.varset.call_args_list, expected)

        mock_Scan1D.assert_not_called()
        mock_Scan2D.assert_not_called()
        mock_TuneSwitch.assert_called_once_with()
        mock_logscanstart.assert_not_called()
        mock_logscanvarstep.assert_not_called()
        mock_logscanstop.assert_not_called()
        mock_time.sleep.assert_not_called()
        mock_midas.startrun.assert_not_called()
        mock_logscanerror.assert_called_once_with()
        self.assertEqual(mock_midas.sendmessage.call_count, 1)

        map(lambda x: x.reset_mock(), mocks)

        # Stopping a PerlRC scan
        mock_sys.argv = ["ProgramName", "stop"]

        mock_midas.varget.side_effect = ["y"]

        prc.main()

        mock_midas.varset.assert_called_once_with(prc.RCActive, 'n')
        mock_Scan1D.assert_not_called()
        mock_Scan2D.assert_not_called()
        mock_TuneSwitch.assert_not_called()
        mock_logscanstart.assert_not_called()
        mock_logscanvarstep.assert_not_called()
        mock_logscanstop.assert_not_called()
        mock_time.sleep.assert_not_called()
        mock_midas.starting.assert_not_called()

        map(lambda x: x.reset_mock(), mocks)

        # Changing a tune
        mock_sys.argv = ["ProgramName", "tune", "tuneName"]

        mock_midas.varget.side_effect = ["n"]

        prc.main()

        mock_ChangeTune.assert_called_once_with("tuneName")
        mock_logswitchedtune.assert_called_once_with("tuneName")
        mock_midas.varset.assert_not_called()
        mock_Scan1D.assert_not_called()
        mock_Scan2D.assert_not_called()
        mock_TuneSwitch.assert_not_called()
        mock_logscanstart.assert_not_called()
        mock_logscanvarstep.assert_not_called()
        mock_logscanstop.assert_not_called()
        mock_time.sleep.assert_not_called()
        mock_midas.starting.assert_not_called()

        map(lambda x: x.reset_mock(), mocks)

        # Changing a tune
        mock_sys.argv = ["ProgramName", "tune", "tuneName"]

        mock_midas.varget.side_effect = ["n"]
        mock_ChangeTune.side_effect = Exception

        prc.main()

        mock_ChangeTune.assert_called_once_with("tuneName")
        mock_logswitchedtune.assert_called_once_with("tuneName", True)
        mock_midas.varset.assert_not_called()
        mock_Scan1D.assert_not_called()
        mock_Scan2D.assert_not_called()
        mock_TuneSwitch.assert_not_called()
        mock_logscanstart.assert_not_called()
        mock_logscanvarstep.assert_not_called()
        mock_logscanstop.assert_not_called()
        mock_time.sleep.assert_not_called()
        mock_midas.starting.assert_not_called()

    @mock.patch('pythonrc.LogScanError')
    @mock.patch('pythonrc.LogSwitchedTune')
    @mock.patch('pythonrc.time')
    @mock.patch('pythonrc.Scan1D')
    @mock.patch('pythonrc.Scan2D')
    @mock.patch('pythonrc.TuneSwitch')
    @mock.patch('pythonrc.ChangeTune')
    @mock.patch('pythonrc.LogScanStart')
    @mock.patch('pythonrc.LogScanVarStep')
    @mock.patch('pythonrc.LogScanStop')
    @mock.patch('pythonrc.sys')
    @mock.patch('pythonrc.Midas')
    def test_main_noCmdArgs(self, mock_midas, mock_sys, mock_logscanstop,
                            mock_logscanvarstep, mock_logscanstart,
                            mock_ChangeTune, mock_TuneSwitch, mock_Scan2D,
                            mock_Scan1D, mock_time, mock_logswitchedtune,
                            mock_logscanerror):
        mocks = [mock_midas, mock_sys, mock_logscanstop,
                 mock_logscanvarstep, mock_logscanstart,
                 mock_ChangeTune, mock_TuneSwitch, mock_Scan2D,
                 mock_Scan1D, mock_time, mock_logswitchedtune,
                 mock_logscanerror]

        # Test if PerlRC is not active
        mock_midas.varget.side_effect = ['n']
        # Set sys.argv = None, since it's not populated
        mock_sys.argv.side_effect = None

        prc.main()

        mock_ChangeTune.assert_not_called()
        mock_logswitchedtune.assert_not_called()
        mock_midas.varset.assert_not_called()
        mock_Scan1D.assert_not_called()
        mock_Scan2D.assert_not_called()
        mock_TuneSwitch.assert_not_called()
        mock_logscanstart.assert_not_called()
        mock_logscanvarstep.assert_not_called()
        mock_logscanstop.assert_not_called()
        mock_time.sleep.assert_not_called()
        mock_midas.starting.assert_not_called()
        mock_logscanerror.assert_not_called()

        map(lambda x: x.reset_mock(), mocks)

        # Test if PrelRC is active
        mock_midas.varget.side_effect = ['y', 'Scan1D']
        mock_sys.argv.side_effect = ['']
        mock_Scan1D.return_value = "called"

        prc.main()

        mock_Scan1D.assert_called_once_with()
        mock_Scan2D.assert_not_called()
        mock_TuneSwitch.assert_not_called()
        mock_logscanstart.assert_called_once_with()
        mock_logscanvarstep.assert_called_with("called")
        mock_logscanstop.assert_called_with()
        mock_time.sleep.assert_called_with(1)
        mock_midas.startrun.assert_called_with()
        mock_logscanerror.assert_not_called()
        mock_midas.sendmessage.assert_not_called()

    @mock.patch('pythonrc.GetTime')
    @mock.patch('pythonrc.Midas')
    def test_LogScanStart(self, mock_midas, mock_GetTime):
        # test with first time through a scan
        mock_midas.varget.side_effect = ["1", "tune1", "ScanType", "11"]

        # need to do some trickery to mock the bulitin funciton "open".
        # taken from:
        # http://stackoverflow.com/questions/1289894/how-do-i-mock-an-
        # open-used-in-a-with-statement-using-the-mock-framework-in-pyth
        open_ = mock.mock_open()
        with mock.patch("__builtin__.open", open_):
            prc.LogScanStart()

        open_.assert_called_once_with(prc.LogFile, 'a')
        mock_GetTime.assert_called_with()
        handle = open_()
        self.assertEqual(handle.write.call_count, 3)

        map(lambda x: x.reset_mock(), [mock_midas, mock_GetTime, open_])

        # test with the second time through a scan
        mock_midas.varget.side_effect = ["2"]

        with mock.patch("__builtin__.open", open_):
            prc.LogScanStart()

        open_.assert_not_called()
        mock_GetTime.assert_not_called()

    @mock.patch('pythonrc.Midas')
    def test_LogScanStop(self, mock_midas):
        # test with last time through a scan
        mock_midas.varget.side_effect = ["11", "11"]

        # need to do some trickery to mock the bulitin funciton "open".
        # taken from:
        # http://stackoverflow.com/questions/1289894/how-do-i-mock-an-
        # open-used-in-a-with-statement-using-the-mock-framework-in-pyth
        open_ = mock.mock_open()
        with mock.patch("__builtin__.open", open_):
            prc.LogScanStop()

        handle = open_()
        self.assertEqual(handle.write.call_count, 2)
        mock_midas.varset.assert_called_once_with(prc.RCActive, 'n')

        map(lambda x: x.reset_mock(), [mock_midas, open_])

        # test with the second time through a scan
        mock_midas.varget.side_effect = ["10", "11"]

        with mock.patch("__builtin__.open", open_):
            prc.LogScanStop()

        open_.assert_not_called()
        mock_midas.varset.assert_not_called()

    @mock.patch('pythonrc.Midas')
    def test_LogScanVarStep(self, mock_midas):
        # test with last time through a scan
        mock_midas.varget.side_effect = ["1000000"]

        # need to do some trickery to mock the bulitin funciton "open".
        # taken from:
        # http://stackoverflow.com/questions/1289894/how-do-i-mock-an-
        # open-used-in-a-with-statement-using-the-mock-framework-in-pyth
        open_ = mock.mock_open()
        with mock.patch("__builtin__.open", open_):
            prc.LogScanVarStep("teststring")

        handle = open_()
        self.assertEqual(handle.write.call_count, 1)
        handle.write.assert_called_once_with("<Run #1000001> teststring\n")

    def test_LogScanError(self):
        open_ = mock.mock_open()
        with mock.patch("__builtin__.open", open_):
            prc.LogScanError()

        handle = open_()
        self.assertEqual(handle.write.call_count, 1)
        handle.write.assert_called_once_with("!!!#### Aborting scan! " +
                                             "####!!!\n")

    @mock.patch('pythonrc.GetTime')
    def test_LogSwitchedTune(self, mock_GetTime):
        mock_GetTime.return_value = "currenttime"
        open_ = mock.mock_open()

        # Test with no error using default value
        with mock.patch("__builtin__.open", open_):
            prc.LogSwitchedTune("tune1")

        mock_GetTime.assert_called_once_with()
        handle = open_()
        handle.write.assert_called_once_with("SwitchedToTune tune1 " +
                                             "at currenttime\n")
        open_.reset_mock()
        mock_GetTime.reset_mock()

        # Test with setting error to False
        with mock.patch("__builtin__.open", open_):
            prc.LogSwitchedTune("tune1", False)

        mock_GetTime.assert_called_once_with()
        handle = open_()
        handle.write.assert_called_once_with("SwitchedToTune tune1 " +
                                             "at currenttime\n")
        open_.reset_mock()
        mock_GetTime.reset_mock()

        # Test with setting error to True
        with mock.patch("__builtin__.open", open_):
            prc.LogSwitchedTune("tune1", True)

        mock_GetTime.assert_called_once_with()
        handle = open_()
        handle.write.assert_called_once_with("ERROR trying to SwitchToTune " +
                                             "tune1 at currenttime\n")
