from .. import dispatcher

def test_dispatch_help():
    result = dispatcher.Dispatcher().dispatch("chan","user","help")
    assert result.startswith("Commands:")

def test_dispatch_nohelp():
    result = dispatcher.Dispatcher().dispatch("chan","user","help notacmd")
    assert  result == "No help for that action."

def test_dispatch_nocmd():
    result = dispatcher.Dispatcher().dispatch("chan","user","notacmd")
    assert  result == "No such action."
