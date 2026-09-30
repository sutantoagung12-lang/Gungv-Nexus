from core.tool_engine import ToolEngine
def test_tool_lifecycle():
    e=ToolEngine()
    e.register("echo","Echo","returns input",lambda value: value)
    assert e.execute("echo",value="x")["status"]=="BLOCKED"
    e.validate("echo",{"test":"passed"}); e.promote("echo")
    r=e.execute("echo",value="x")
    assert r["status"]=="COMPLETED" and r["result"]=="x"
def test_invalid_handler():
    e=ToolEngine()
    try: e.register("bad","Bad","invalid",None)
    except TypeError: return
    assert False
