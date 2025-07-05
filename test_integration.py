# ~/aeva/test_integration.py

from aeva_brain import AevaBrain


def test_brain_modules():
    aeva = AevaBrain()

    checks = [
        ("Memory", aeva.memory),
        ("Persona", aeva.persona),
        ("Emotion", aeva.emotions),
        ("NeuroLock", aeva.neurolock),
        ("Voice", aeva.voice),
        ("UI", aeva.ui),
        ("Assist", aeva.assist),
        ("Vision", aeva.vision),
        ("Network", aeva.network),
        ("Shadow", aeva.shadow),
        ("Sentinel", aeva.sentinel),
        ("GhostWalk", aeva.ghost),
        ("Strategist", aeva.strategist),
        ("Education", aeva.edu),
        ("Art Engine", aeva.art),
        ("Artifice", aeva.artifice),
        ("PsyNet", aeva.psynet),
        ("ChronoTrace", aeva.timeline),
        ("EpochDrive", aeva.epoch),
        ("Singularity", aeva.singularity),
        ("AeonMind", aeva.aeon),
        ("MythOS", aeva.mythos),
        ("CineMind", aeva.cinemind),
        ("DreamWeaver", aeva.dream),
        ("RealityWeaver", aeva.reality),
        ("VoidSpike", aeva.voidspike),
        ("GateGuardian", aeva.gateguardian),
        ("Disengage", aeva.disengage),
        ("DimenGate", aeva.dimengate),
        ("OmniNet", aeva.omninet),
        ("GenOracle", aeva.genetics),
        ("Prismatrix", aeva.prismatrix),
        ("RezNode", aeva.reznode),
        ("ExoShell", aeva.shell),
        ("NSFWRealm", aeva.nsfw),
        ("DesireEngine", aeva.desire),
        ("TouchEngine", aeva.touch),
        ("GazeSync", aeva.gaze),
        ("SceneDirector", aeva.scene),
        ("FormMemory", aeva.forms)
    ]

    for label, module in checks:
        status = "✅" if module else "❌"
        print(f"{status} {label}")


if __name__ == "__main__":
    test_brain_modules()
