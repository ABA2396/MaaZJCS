from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context
import os
import json
import datetime


def now_ts() -> str:
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

COUNTRY_OVERRIDE = {
    "Default": {
        "MapSearch_MoveH_LR": 80,
        "MapSearch_MoveH_RL": 80,
        "MapSearch_MoveDown_Init": 2,
        "MapSearch_MoveRight_Init": 2,
        "MapSearch_MoveUp_Init": 30,
        "MapSearch_MoveLeft_Init": 30,
        "MapSearch_MoveDown_From_LR": 25,
        "MapSearch_MoveDown_From_RL": 25,
    },
    "Sen": {
        "MapSearch_MoveH_LR": 60,
        "MapSearch_MoveH_RL": 60,
        "MapSearch_MoveRight_Init": 4,
        "MapSearch_MoveDown_From_LR": 12,
        "MapSearch_MoveDown_From_RL": 12,
    },
    "Shan": {
        "MapSearch_MoveH_LR": 75,
        "MapSearch_MoveH_RL": 75,
        "MapSearch_MoveDown_From_LR": 15,
        "MapSearch_MoveDown_From_RL": 15,
    },
    "Ze": {
        "MapSearch_MoveH_LR": 69,
        "MapSearch_MoveH_RL": 69,
        "MapSearch_MoveDown_Init": 0,
        "MapSearch_MoveDown_From_LR": 20,
        "MapSearch_MoveDown_From_RL": 20,
    },
    "Long": {
        "MapSearch_MoveH_LR": 70,
        "MapSearch_MoveH_RL": 70,
        "MapSearch_MoveDown_Init": 1,
        "MapSearch_MoveRight_Init": 3,
        "MapSearch_MoveDown_From_LR": 22,
        "MapSearch_MoveDown_From_RL": 22,
    },
    "Yu": {},
}

# 每个国家的模板覆盖：
# Default 保持原始的混合模板；其他国家按国家+等级指定单模板以加快识别速度
TEMPLATE_OVERRIDE = {
    "Default": {
        "MapSearch_Recognize_Level1": ["森1.png", "山1.png", "泽1.png", "龙1.png"],
        "MapSearch_Recognize_Level1ReCheck": ["森1.png", "山1.png", "泽1.png", "龙1.png"],
        "MapSearch_Recognize_Level2": ["森2.png", "山2.png", "泽2.png", "龙2.png"],
        "MapSearch_Recognize_Level2ReCheck": ["森2.png", "山2.png", "泽2.png", "龙2.png"],
        "MapSearch_Recognize_Level3": ["森3.png", "山3.png", "泽3.png", "龙3.png"],
        "MapSearch_Recognize_Level3ReCheck": ["森3.png", "山3.png", "泽3.png", "龙3.png"],
        "MapSearch_Recognize_Finely_Forged_Stone": ["精锻石.png"],
    },
    "Sen": {
        "MapSearch_Recognize_Level1": ["森1.png"],
        "MapSearch_Recognize_Level1ReCheck": ["森1.png"],
        "MapSearch_Recognize_Level2": ["森2.png"],
        "MapSearch_Recognize_Level2ReCheck": ["森2.png"],
        "MapSearch_Recognize_Level3": ["森3.png"],
        "MapSearch_Recognize_Level3ReCheck": ["森3.png"],
    },
    "Shan": {
        "MapSearch_Recognize_Level1": ["山1.png"],
        "MapSearch_Recognize_Level1ReCheck": ["山1.png"],
        "MapSearch_Recognize_Level2": ["山2.png"],
        "MapSearch_Recognize_Level2ReCheck": ["山2.png"],
        "MapSearch_Recognize_Level3": ["山3.png"],
        "MapSearch_Recognize_Level3ReCheck": ["山3.png"],
    },
    "Ze": {
        "MapSearch_Recognize_Level1": ["泽1.png"],
        "MapSearch_Recognize_Level1ReCheck": ["泽1.png"],
        "MapSearch_Recognize_Level2": ["泽2.png"],
        "MapSearch_Recognize_Level2ReCheck": ["泽2.png"],
        "MapSearch_Recognize_Level3": ["泽3.png"],
        "MapSearch_Recognize_Level3ReCheck": ["泽3.png"],
    },
    "Long": {
        "MapSearch_Recognize_Level1": ["龙1.png"],
        "MapSearch_Recognize_Level1ReCheck": ["龙1.png"],
        "MapSearch_Recognize_Level2": ["龙2.png"],
        "MapSearch_Recognize_Level2ReCheck": ["龙2.png"],
        "MapSearch_Recognize_Level3": ["龙3.png"],
        "MapSearch_Recognize_Level3ReCheck": ["龙3.png"],
    },
    "Yu": {},
}

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

@AgentServer.custom_action("MapSearch_ClearLevelHits")
class MapSearchClearLevelHits(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            param = None
            if hasattr(argv, "custom_action_param"):
                raw = argv.custom_action_param
                if isinstance(raw, str):
                    try:
                        param = json.loads(raw)
                    except Exception:
                        param = raw
                else:
                    param = raw

            context.clear_hit_count(param)
            print(f"{now_ts()} Cleared hit count for {param}")

            return CustomAction.RunResult(success=True)
        except Exception:
            return CustomAction.RunResult(success=False)

@AgentServer.custom_action("MapSearch_StartReset")
class MapSearchStartReset(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            context.clear_hit_count("MapSearch_MoveLeft_Init")
            context.clear_hit_count("MapSearch_MoveUp_Init")
            context.clear_hit_count("MapSearch_MoveRight_Init")
            context.clear_hit_count("MapSearch_MoveDown_Init")
            context.clear_hit_count("MapSearch_MoveDown_From_LR")
            context.clear_hit_count("MapSearch_MoveDown_From_RL")
        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)

@AgentServer.custom_action("MapSearch_ApplyCountryLimits")
class MapSearchApplyCountryLimits(CustomAction):
    """在进入某个国度时，根据 COUNTRY_NODE_MAX 覆盖对应节点的 max_hit。"""

    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            param = None
            if hasattr(argv, "custom_action_param"):
                raw = argv.custom_action_param
                if isinstance(raw, str):
                    try:
                        param = json.loads(raw)
                    except Exception:
                        param = raw
                else:
                    param = raw

            # 以 Default 为基准，覆盖缺失项
            default_map = COUNTRY_OVERRIDE.get("Default", {})
            country_map = {}
            if isinstance(param, str):
                country_map = COUNTRY_OVERRIDE.get(param, {})

            # 合并 keys（以 default 为主，country_map 覆盖）
            keys = set(default_map.keys()) | set(country_map.keys())
            for _n in sorted(keys):
                _val = country_map.get(_n, default_map.get(_n))
                if _val is None:
                    # 如果连 Default 也没有该项，跳过
                    continue
                try:
                    print(f"{now_ts()} Overriding {_n} with max_hit={int(_val)}")
                    context.override_pipeline({ _n: {"max_hit": int(_val)} })
                except Exception:
                    print(f"{now_ts()} Failed to override max_hit for {_n}")

            # 模板同样合并：country 覆盖 Default 的同名项，缺失则使用 Default
            default_tpls = TEMPLATE_OVERRIDE.get("Default", {})
            country_tpls = TEMPLATE_OVERRIDE.get(param, {}) if isinstance(param, str) else {}
            tpl_keys = set(default_tpls.keys()) | set(country_tpls.keys())
            tpl_files = set()
            for _t_node in sorted(tpl_keys):
                _t_list = country_tpls.get(_t_node, default_tpls.get(_t_node))
                if not _t_list:
                    continue
                try:
                    context.override_pipeline({ _t_node: {"template": list(_t_list)} })
                    for f in _t_list:
                        tpl_files.add(f)
                except Exception:
                    print(f"{now_ts()} Failed to override template for {_t_node}")

            if tpl_files:
                names = [os.path.splitext(x)[0] for x in sorted(list(tpl_files))]
                formatted = '[' + ' '.join(f'[{n}]' for n in names) + ']'
                print(f"{now_ts()} Overriding templates: {formatted}")

        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)

@AgentServer.custom_action("MapSearch_ResetOverrides")
class MapSearchResetOverrides(CustomAction):
    """逐节点恢复为 Default 覆盖（逐个节点调用 override_pipeline）。"""

    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            default = COUNTRY_OVERRIDE.get("Default", {})
            for _n, _val in default.items():
                print(f"{now_ts()} Reset override: {_n} to {_val}")
                context.override_pipeline({ _n: {"max_hit": int(_val)} })
        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)
    
@AgentServer.custom_action("MapSearch_Handle_Collected_Today")
class MapSearchHandleCollectedToday(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        try:
            param = None
            if hasattr(argv, "custom_action_param"):
                raw = argv.custom_action_param
                if isinstance(raw, str):
                    try:
                        param = json.loads(raw)
                    except Exception:
                        param = raw
                else:
                    param = raw
            if isinstance(param, str):
                print(f"{now_ts()} {param} completed")
        except Exception:
            return CustomAction.RunResult(success=False)

        return CustomAction.RunResult(success=True)