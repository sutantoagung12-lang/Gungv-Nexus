from skills.god_skill import GodSkill

def test_god_skill_assesses_and_verifies():
    s=GodSkill()
    a=s.assess("expand AI knowledge", {"memory": 1})
    assert a["next"]=="reason"
    assert s.verify({"ok":True},{"test":"pass"})["verified"] is True

def test_god_skill_expands():
    s=GodSkill()
    assert s.expand("new-domain")["status"]=="PROPOSED"
    assert "new-domain" in s.capabilities
