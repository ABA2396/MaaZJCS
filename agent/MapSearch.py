from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

@AgentServer.custom_action("MapSearch_RowReset")
class MapSearchRowReset(CustomAction):
    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        try:
            context.clear_hit_count("MapSearch_MoveH_LR")
            context.clear_hit_count("MapSearch_MoveH_RL")
        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)

@AgentServer.custom_action("MapSearch_ClearLevelHits1")
class MapSearchClearLevelHits(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            context.clear_hit_count("MapSearch_Recognize_Level1")
        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)
    
@AgentServer.custom_action("MapSearch_ClearLevelHits2")
class MapSearchClearLevelHits2(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            context.clear_hit_count("MapSearch_Recognize_Level2")
        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)

@AgentServer.custom_action("MapSearch_ClearLevelHits3")
class MapSearchClearLevelHits3(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            context.clear_hit_count("MapSearch_Recognize_Level3")
        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)


@AgentServer.custom_action("MapSearch_StartReset")
class MapSearchStartReset(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            context.clear_hit_count("MapSearch_MoveLeft_Init")
            context.clear_hit_count("MapSearch_MoveUp_Init")
            context.clear_hit_count("MapSearch_MoveDown_From_LR")
            context.clear_hit_count("MapSearch_MoveDown_From_RL")
        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)