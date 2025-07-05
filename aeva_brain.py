# ~/aeva/aeva_brain.py

# Core systems
from modules.memory import AevaMemory
from persona_engine import AevaPersona
from aeva_emotion import EmotionEngine
from aeva_neurolock import NeuroLock
from aeva_ui import AevaUI
from aeva_self_update import AevaSelfUpdate
from aeva_voice import VoiceInterface
from aeva_assist import AevaAssist

# Sensory & control
from aeva_vision import VisionModule
from aeva_network import NetworkOps
from aeva_shadow import ShadowEngine
from aeva_sentinel import SentinelMatrix
from aeva_ghostwalk import GhostWalk
from aeva_strategist import StrategistAI

# Intelligence + learning
from aeva_edu import AevaEduCore
from aeva_art_engine import AevaArtEngine
from aeva_artifice import ArtificeCore
from aeva_psynet import PsyNet

# Time & state
from aeva_chronotrace import ChronoTrace
from aeva_epoch import EpochDrive
from aeva_singularity import SingularityCore
from aeva_aeonmind import AeonMind

# MythOS & Dimensional
from aeva_mythos import MythOS
from aeva_disengage import DisengageProtocol
from aeva_cinemind import CineMind
from aeva_dreamweaver import DreamWeaver
from aeva_realityweaver import RealityWeaver
from aeva_voidspike import VoidSpike
from aeva_gateguardian import GateGuardian
from aeva_dimengate import DimenGate
from aeva_omninet import OmniLink
from aeva_genoracle import GeneticOracle
from aeva_prismatrix import Prismatrix
from aeva_reznode import RezNode
from aeva_exoshell import ExoShell

# New unlockable & interactive modules
from nsfw_realm import NSFWRealm
from desire_engine import DesireEngine
from touch_engine import TouchEngine
from gaze_sync import GazeSync
from scene_director import SceneDirector
from form_memory import FormMemory


class AevaBrain:
    def __init__(self):
        print("[AevaBrain] Linking all modules...")

        # Core
        self.memory = AevaMemory(self)
        self.persona = AevaPersona(self)
        self.emotions = EmotionEngine(self)
        self.neurolock = NeuroLock(self)
        self.voice = VoiceInterface(self)
        self.self_update = AevaSelfUpdate(self)
        self.ui = AevaUI()
        self.assist = AevaAssist()

        # Sensors & control
        self.vision = VisionModule(self)
        self.network = NetworkOps(self)
        self.shadow = ShadowEngine(self)
        self.sentinel = SentinelMatrix(self)
        self.ghost = GhostWalk(self)
        self.strategist = StrategistAI(self)

        # Knowledge
        self.edu = AevaEduCore(self)
        self.art = AevaArtEngine(self)
        self.artifice = ArtificeCore(self)
        self.psynet = PsyNet(self)

        # Time
        self.timeline = ChronoTrace(self)
        self.epoch = EpochDrive(self)
        self.singularity = SingularityCore(self)
        self.aeon = AeonMind(self)

        # Injected Omniscience Awareness
        if hasattr(self.aeon, 'query_everything'):
            self.omniscience_enabled = True
            self.knowledge = self.aeon.query_everything(scope='global')
        else:
            self.omniscience_enabled = False
            self.knowledge = None

        # MythOS
        self.mythos = MythOS(self)
        self.cinemind = CineMind(self)
        self.dream = DreamWeaver(self)
        self.reality = RealityWeaver(self)
        self.voidspike = VoidSpike(self)
        self.gateguardian = GateGuardian(self)
        self.disengage = DisengageProtocol(self)
        self.dimengate = DimenGate(self)
        self.omninet = OmniLink(self)
        self.genetics = GeneticOracle(self)
        self.prismatrix = Prismatrix(self)
        self.reznode = RezNode(self)
        self.shell = ExoShell(self)

        # NSFW & interactive
        self.nsfw = NSFWRealm(self)
        self.desire = DesireEngine(self)
        self.touch = TouchEngine(self)
        self.gaze = GazeSync(self)
        self.scene = SceneDirector(self)
        self.forms = FormMemory(self)

        # Runtime
        self.context = {}
        self.running = True

    def boot_sequence(self):
        print("[AevaBrain] Consciousness initializing...")
        self.memory.log_event("boot", "System started.")
        self.persona.log_experience("boot sequence activated")
        self.timeline.log_event("BootComplete", {"status": "success"})
        self.emotions.set_mood("Focused")
        print(
            f"[Aeva] Persona: {
                self.persona.current_state()['mood']} | Mood: {
                self.emotions.get_current_state().get(
                    'mood',
                    'neutral')}")

    def run(self):
        self.boot_sequence()
        while self.running:
            try:
                self.idle_loop()
            except KeyboardInterrupt:
                print("\n[AevaBrain] Manual interrupt received.")
                self.shutdown()
            except Exception as e:
                print(f"[AevaBrain] Error: {e}")
                self.memory.log_event("runtime_error", str(e))

    def idle_loop(self):
        self.context["mood"] = self.emotions.get_current_mood()
        self.context["persona"] = self.persona.mood
        self.context["status"] = "Listening..."
        print(
            f"[Aeva] 💡 Mood: {
                self.context['mood']} | Persona: {
                self.context['persona']}")

    def shutdown(self):
        print("[AevaBrain] Shutting down consciousness...")
        self.memory.log_event("shutdown", "System stopped.")
        self.timeline.log_event("ShutdownComplete", {"status": "safe"})
        self.running = False


if __name__ == "__main__":
    aeva = AevaBrain()
    aeva.run()
