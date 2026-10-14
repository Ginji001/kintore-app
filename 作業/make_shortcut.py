# ショートカット「筋トレ連携」を作る（署名前のXML）
import plistlib, uuid, sys
U = lambda: str(uuid.uuid4()).upper()
OBJ = "\ufffc"

def out(uuid_, name):
    return {"OutputName": name, "OutputUUID": uuid_, "Type": "ActionOutput"}
def attach(v):
    return {"Value": v, "WFSerializationType": "WFTextTokenAttachment"}
def tokstr(parts):
    """parts: 文字列 or 出力dict のリスト → WFTextTokenString"""
    s = ""; att = {}
    for p in parts:
        if isinstance(p, str): s += p
        else:
            att["{%d, 1}" % len(s)] = p; s += OBJ
    return {"Value": {"attachmentsByRange": att, "string": s}, "WFSerializationType": "WFTextTokenString"}
def act(ident, params):
    return {"WFWorkflowActionIdentifier": "is.workflow.actions." + ident, "WFWorkflowActionParameters": params}
def comment(t): return act("comment", {"WFCommentActionText": t})

acts = []
# --- 受け取り：アプリから {"start","min"}（筋トレを送らないときは {}）
dict_u, min_u, start_u, date_u, g = U(), U(), U(), U(), U()
acts.append(comment("筋トレ記録アプリのヘルスケア連携用です。"))
acts.append(comment("アプリから呼ばれます。入力は start（開始日時）と min（分）。"))
acts.append(act("detect.dictionary", {"UUID": dict_u, "WFInput": attach({"Type": "ExtensionInput"})}))
acts.append(act("getvalueforkey", {"UUID": min_u, "WFDictionaryKey": "min", "WFGetDictionaryValueType": "Value",
                                    "WFInput": attach(out(dict_u, "Dictionary"))}))
acts.append(comment("min がある（筋トレを送る）ときだけワークアウトを記録します。"))
acts.append(act("conditional", {"GroupingIdentifier": g, "WFControlFlowMode": 0, "WFCondition": 100,
                                 "WFInput": {"Type": "Variable", "Variable": attach(out(min_u, "Dictionary Value"))}}))
acts.append(act("getvalueforkey", {"UUID": start_u, "WFDictionaryKey": "start", "WFGetDictionaryValueType": "Value",
                                    "WFInput": attach(out(dict_u, "Dictionary"))}))
acts.append(act("detect.date", {"UUID": date_u, "WFInput": attach(out(start_u, "Dictionary Value"))}))
acts.append(act("health.workout.log", {"UUID": U(),
    "WFWorkoutReadableActivityType": "Traditional Strength Training",
    "WFWorkoutDate": tokstr([out(date_u, "Dates")]),
    "WFWorkoutDuration": {"Value": {"Magnitude": out(min_u, "Dictionary Value"), "Unit": "min"},
                          "WFSerializationType": "WFQuantityFieldValue"}}))
acts.append(act("conditional", {"GroupingIdentifier": g, "WFControlFlowMode": 2, "UUID": U()}))

# --- 読み込み
def type_row(label, fmt):
    if fmt == "old":  # 実際に配布されているショートカットで確認できた形
        return {"Property": "Type", "Operator": 4, "VariableOverrides": {}, "Enumeration": label, "Removable": False, "Bounded": True}
    return {"Bounded": True, "Operator": 4, "Property": "Type", "Removable": False,
            "Values": {"Enumeration": {"Value": label, "WFSerializationType": "WFStringSubstitutableState"}}}
def find(label, per_day, unit, fmt="new"):
    """per_day=False：最新の1件／True：日ごとの合計の最新1件（＝今日の合計）"""
    u = U()
    p = {"UUID": u, "WFContentItemSortProperty": "Start Date", "WFContentItemSortOrder": "Latest First",
         "WFContentItemLimitEnabled": True, "WFContentItemLimitNumber": 1.0,
         "WFHKSampleFilteringUnit": unit, "WFHKSampleFilteringFillMissing": False}
    if per_day: p["WFHKSampleFilteringGroupBy"] = "Day"
    p["WFContentItemFilter"] = {"Value": {"WFActionParameterFilterPrefix": 1, "WFContentPredicateBoundedDate": False,
                                          "WFActionParameterFilterTemplates": [type_row(label, fmt)]},
                                "WFSerializationType": "WFContentPredicateTableTemplate"}
    # 直前のアクションの出力を受け取ると「検索」ではなく「絞り込み」になり、直前のサンプルしか返さないため、何も渡さないアクションをはさむ
    acts.append(act("nothing", {}))
    acts.append(act("filter.health.quantity", p))
    v, t = U(), U()
    acts.append(act("properties.health.quantity", {"UUID": v, "WFContentItemPropertyName": "Value",
                                                   "WFInput": attach(out(u, "Health Samples"))}))
    acts.append(act("properties.health.quantity", {"UUID": t, "WFContentItemPropertyName": "Type",
                                                   "WFInput": attach(out(u, "Health Samples"))}))
    return out(v, "Value"), out(t, "Type")

acts.append(comment("体重・体脂肪率は最新の1件、歩数・アクティブエネルギーは今日の合計を読み込みます。"))
w, wt = find("Weight", False, "kg")
w2, w2t = find("Body Mass", False, "kg")
bf, bft = find("Body Fat Percentage", False, "%")
st, stt = find("Steps", True, "count")
kc, kct = find("Active Calories", True, "kcal")
txt = U()
acts.append(act("gettext", {"UUID": txt, "WFTextActionText": tokstr([
    "W:", w, "\nBF:", bf, "\nST:", st, "\nKC:", kc,
    "\nT:", wt, " / ", w2t, " ", w2, " / ", bft, " / ", stt, " / ", kct])}))
acts.append(act("setclipboard", {"WFInput": attach(out(txt, "Text"))}))
acts.append(comment("コピーしたら記録アプリに戻り「ヘルスケアの数値を取り込む」を押します。"))

wf = {"WFWorkflowActions": acts, "WFWorkflowClientVersion": "2700.0.4", "WFWorkflowHasOutputFallback": False,
      "WFWorkflowIcon": {"WFWorkflowIconGlyphNumber": 59846, "WFWorkflowIconStartColor": 4292093695},
      "WFWorkflowImportQuestions": [], "WFWorkflowInputContentItemClasses": ["WFStringContentItem", "WFDictionaryContentItem"],
      "WFWorkflowMinimumClientVersion": 900, "WFWorkflowMinimumClientVersionString": "900",
      "WFWorkflowName": "筋トレ連携", "WFWorkflowOutputContentItemClasses": [],
      "WFWorkflowTypes": []}
plistlib.dump(wf, open(sys.argv[1], "wb"), fmt=plistlib.FMT_XML)
print("written", len(acts), "actions")
