import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[1]
EDEN_LIB = REPO_ROOT / "eden_lib"

if str(EDEN_LIB) not in sys.path:
    sys.path.insert(0, str(EDEN_LIB))


from Eden.Eden3D.Actors.EdenActor import EdenActor
from Eden.Eden3D.Simulators.Board.Board_8x8 import Board_8x8
from Eden.Eden3D.Worlds.Creation import Creation
from Eden.EdenTools.Systemic.MVC import MVC_System
from Eden.EdenTools.Systemic.SystemSensor import SystemSensor
from Eden.EdenTools.XMLParsers.ConfigParser import ConfigParser


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

    def test_config_parser_converts_typed_values(self):
        xml_data = """
<config>
    <section Name="About">
        <value valueName="Title">Smoke Test</value>
        <bvalue valueName="Enabled">1</bvalue>
        <fvalue valueName="Speed">2.5</fvalue>
        <ivalue valueName="Lives">3</ivalue>
    </section>
</config>
""".strip()

        with TemporaryDirectory() as temp_dir:
            xml_path = Path(temp_dir) / "config.xml"
            xml_path.write_text(xml_data, encoding="utf-8")

            parser = ConfigParser()
            parser.parseFile(xml_path)
            parser.getSectionValues("section", "About")

            self.assertEqual(
                parser.Parser["XML_Values"]["About_Values"]["Title"], "Smoke Test"
            )
            self.assertTrue(parser.Parser["XML_Values"]["About_Values"]["Enabled"])
            self.assertEqual(parser.Parser["XML_Values"]["About_Values"]["Speed"], 2.5)
            self.assertEqual(parser.Parser["XML_Values"]["About_Values"]["Lives"], 3)

    def test_mvc_system_builds_absolute_convenience_paths(self):
        with TemporaryDirectory() as temp_dir:
            mvc_root = Path(temp_dir)
            for rel_path in (
                "resources/images",
                "resources/models/actors",
                "resources/models/geometry",
                "resources/sound/effects",
                "resources/sound/music",
                "resources/text/fonts",
                "resources/video",
                "scripts",
                "config",
            ):
                (mvc_root / rel_path).mkdir(parents=True, exist_ok=True)

            (mvc_root / "scripts" / "main.py").write_text(
                "print('ok')\n", encoding="utf-8"
            )
            (mvc_root / "config" / "config.xml").write_text(
                "<config />\n", encoding="utf-8"
            )

            mvc = MVC_System(str(mvc_root))

            self.assertTrue(mvc.fullMVC)
            self.assertEqual(mvc.mvcStructure["/"], str(mvc_root.resolve()))
            self.assertTrue(
                Path(mvc.mvcStructure["tier_resource"]["text"]).is_absolute()
            )
            self.assertTrue(
                Path(mvc.mvcStructure["tier_models"]["geometry"]).is_absolute()
            )
            self.assertTrue(
                Path(mvc.mvcStructure["tier_sound"]["effects"]).is_absolute()
            )
            self.assertTrue(Path(mvc.mvcStructure["tier_text"]["fonts"]).is_absolute())

    def test_creation_resolves_mvc_root_from_main_script(self):
        with TemporaryDirectory() as temp_dir:
            mvc_root = Path(temp_dir)
            for rel_path in ("resources", "scripts", "config"):
                (mvc_root / rel_path).mkdir(parents=True, exist_ok=True)

            main_file = mvc_root / "scripts" / "main.py"
            main_file.write_text("print('ok')\n", encoding="utf-8")

            resolved_root = Creation.resolveMVCRoot(mainFile=str(main_file))

            self.assertEqual(resolved_root, str(mvc_root.resolve()))

    def test_creation_resolves_explicit_startup_paths(self):
        with TemporaryDirectory() as temp_dir:
            mvc_root = Path(temp_dir)
            (mvc_root / "config").mkdir(parents=True, exist_ok=True)
            explicit_config = mvc_root / "config" / "custom.xml"
            explicit_config.write_text("<config />\n", encoding="utf-8")

            resolved_root, resolved_config = Creation.resolveStartupPaths(
                mvcRootDir=str(mvc_root), configXML="custom.xml"
            )

            self.assertEqual(resolved_root, str(mvc_root.resolve()))
            self.assertEqual(resolved_config, str(explicit_config.resolve()))

    def test_check_mvc_accepts_explicit_config_override(self):
        with TemporaryDirectory() as temp_dir:
            mvc_root = Path(temp_dir)
            for rel_path in (
                "resources",
                "resources/text/fonts",
                "scripts",
                "config",
            ):
                (mvc_root / rel_path).mkdir(parents=True, exist_ok=True)
            (mvc_root / "scripts" / "main.py").write_text(
                "print('ok')\n", encoding="utf-8"
            )

            explicit_config = mvc_root / "config" / "custom.xml"
            explicit_config.write_text("<config />\n", encoding="utf-8")

            class DummyCreation:
                def __init__(self):
                    self.parsed_configs = []

                def parseConfigXML(self, config_path):
                    self.parsed_configs.append(config_path)

            dummy = DummyCreation()

            Creation.checkMVC(dummy, str(mvc_root), str(explicit_config))

            self.assertTrue(dummy.gameMVC.fullMVC)
            self.assertEqual(dummy.parsed_configs, [str(explicit_config.resolve())])


if __name__ == "__main__":
    unittest.main()
