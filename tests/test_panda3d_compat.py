import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EDEN_LIB = REPO_ROOT / "eden_lib"

if str(EDEN_LIB) not in sys.path:
    sys.path.insert(0, str(EDEN_LIB))


from Eden.Eden3D.Actors.EdenActor import EdenActor
from Eden.Eden3D.Simulators.Board.Board_8x8 import Board_8x8
from Eden.Eden3D.Worlds.Creation import Creation
from Eden.EdenTools.Systemic.SystemSensor import SystemSensor


class DummyBaseActor:
    def __init__(self, control_result):
        self.control_result = control_result
        self.calls = []

    def controlJoint(self, node_path, model_root, joint_name):
        self.calls.append((node_path, model_root, joint_name))
        return self.control_result


class DummySound:
    def __init__(self):
        self.balance = None
        self.play_count = 0

    def setBalance(self, value):
        self.balance = value

    def play(self):
        self.play_count += 1


class Panda3DCompatibilityTests(unittest.TestCase):
    def test_joint_control_path_stores_returned_node(self):
        actor = EdenActor.__new__(EdenActor)
        actor.baseActor = DummyBaseActor(control_result="joint-node")
        actor.controllerList = {}

        result = EdenActor.getJointControlPath(actor, "RightHand")

        self.assertTrue(result)
        self.assertEqual(actor.controllerList["RightHand"], "joint-node")
        self.assertEqual(actor.baseActor.calls, [(None, "modelRoot", "RightHand")])

    def test_joint_control_path_returns_false_when_joint_missing(self):
        actor = EdenActor.__new__(EdenActor)
        actor.baseActor = DummyBaseActor(control_result=None)
        actor.controllerList = {}

        result = EdenActor.getJointControlPath(actor, "MissingJoint")

        self.assertFalse(result)
        self.assertEqual(actor.controllerList, {})

    def test_set_sound_pan_clamps_balance(self):
        sound = DummySound()
        world = type("WorldStub", (), {"jukeBox": {"fx": sound}})()

        Creation.setSoundPan(world, "fx", 2.5)

        self.assertEqual(sound.balance, 1.0)

    def test_set_sound_pan_returns_false_for_missing_sound(self):
        world = type("WorldStub", (), {"jukeBox": {}})()

        result = Creation.setSoundPan(world, "missing", 0.2)

        self.assertFalse(result)

    def test_event_processor_plays_registered_sound(self):
        sound = DummySound()
        board = type(
            "BoardStub",
            (),
            {"eventCodeLibrary": {"move": "tick"}, "jukeBox": {"tick": sound}},
        )()

        Board_8x8.eventProcessor(board, "move")

        self.assertEqual(sound.play_count, 1)

    def test_event_processor_ignores_unknown_event(self):
        sound = DummySound()
        board = type(
            "BoardStub",
            (),
            {"eventCodeLibrary": {"move": "tick"}, "jukeBox": {"tick": sound}},
        )()

        Board_8x8.eventProcessor(board, "missing")

        self.assertEqual(sound.play_count, 0)

    def test_system_sensor_accepts_partial_custom_prc(self):
        sensor = SystemSensor(customData={"fullscreen": False})

        self.assertEqual(sensor.systemData["screenResolution"], (800.0, 600.0))


if __name__ == "__main__":
    unittest.main()
