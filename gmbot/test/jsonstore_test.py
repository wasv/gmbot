from .. import jsonstore

def test_empty_get(tmpdir):
    ctx = jsonstore.JsonStore(tmpdir.join("empty.json"))
    assert not ctx.get()
    assert not ctx.get('chan')
    assert not ctx.get('chan','user')
    assert not ctx.get('chan','user','key')

def test_get(tmpdir):
    ctx = jsonstore.JsonStore(tmpdir.join("set.json"))

    exp = {'chan': {'user': {'key': 'value'}}}
    ctx.set('chan','user','key','value')

    assert ctx.get() == exp
    assert ctx.get('chan') == exp['chan']
    assert ctx.get('chan','user') == exp['chan']['user']
    assert ctx.get('chan','user','key') == exp['chan']['user']['key']

def test_load(tmpdir):
    ctx = jsonstore.JsonStore(tmpdir.join("state.json"))

    exp = {'chan': {'user': {'key': 'value'}}}
    ctx.set('chan','user','key','value')

    newctx = jsonstore.JsonStore(tmpdir.join("state.json"))
    assert ctx.get() == newctx.get()
