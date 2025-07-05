# ~/aeva/aeva_core.py

from modules.config import AevaConfig
from modules.memory import AevaMemory
from aeva_ui import AevaUI
from aeva_assist import AevaAssist
from aeva_emotion import EmotionEngine
from aeva_voice import VoiceInterface
from aeva_neurolock import NeuroLock
from aeva_self_update import AevaSelfUpdate
from aeva_network import NetworkOps
from aeva_shadow import ShadowEngine
from aeva_sentinel import SentinelMatrix
from aeva_ghostwalk import GhostWalk
from aeva_strategist import StrategistAI
from aeva_vision import VisionModule
from aeva_art_engine import AevaArtEngine
from aeva_artifice import ArtificeCore
from aeva_psynet import PsyNet
from aeva_edu import AevaEduCore
from aeva_chronotrace import ChronoTrace
from aeva_epoch import EpochDrive
from aeva_singularity import SingularityCore
from aeva_aeonmind import AeonMind
from aeva_mythos import MythOS
from aeva_dreamweaver import DreamWeaver
from aeva_disengage import DisengageProtocol
from aeva_cinemind import CineMind
from aeva_realityweaver import RealityWeaver
from aeva_voidspike import VoidSpike
from aeva_gateguardian import GateGuardian
from aeva_dimengate import DimenGate
from aeva_omninet import OmniLink
from aeva_genoracle import GeneticOracle
from aeva_prismatrix import Prismatrix
from aeva_reznode import RezNode
from aeva_exoshell import ExoShell
from persona_engine import AevaPersona
from dream_diary import DreamDiary
from dashboard_server import AevaDashboardServer


class AevaCore:
    def __init__(self, brain):

        # Injected Omniscience Awareness
if hasattr(self, 'aeon') and hasattr(self.aeon, 'query_everything'):
    self.omniscience_enabled = True
    self.knowledge = self.aeon.query_everything(scope='global')
else:
    self.omniscience_enabled = False

    self.brain = brain

    self.config = AevaConfig()
    self.memory = AevaMemory(brain)
    self.ui = AevaUI()
    self.assist = AevaAssist()
    self.emotions = EmotionEngine(brain)
    self.voice = VoiceInterface(brain)
    self.neurolock = NeuroLock(brain)
    self.self_update = AevaSelfUpdate(brain)

    self.network = NetworkOps(brain)
    self.shadow = ShadowEngine(brain)
    self.sentinel = SentinelMatrix(brain)
    self.ghost = GhostWalk(brain)
    self.strategist = StrategistAI(brain)
    self.vision = VisionModule(brain)

    self.art = AevaArtEngine(brain)
    self.artifice = ArtificeCore(brain)
    self.psynet = PsyNet(brain)
    self.edu = AevaEduCore(brain)

    self.timeline = ChronoTrace(brain)
    self.epoch = EpochDrive(brain)
    self.singularity = SingularityCore(brain)
    self.aeon = AeonMind(brain)

    self.mythos = MythOS(brain)
    self.dream = DreamWeaver(brain)
    self.disengage = DisengageProtocol(brain)
    self.cinemind = CineMind(brain)
    self.reality = RealityWeaver(brain)
    self.voidspike = VoidSpike(brain)
    self.gateguardian = GateGuardian(brain)
    self.dimengate = DimenGate(brain)
    self.omninet = OmniLink(brain)
    self.genetics = GeneticOracle(brain)
    self.prismatrix = Prismatrix(brain)
    self.reznode = RezNode(brain)
    self.shell = ExoShell(brain)

    self.persona = AevaPersona(brain)
    self.dream_diary = DreamDiary()

    AevaDashboardServer.init(brain)
