from tests.packs.timeline import test_visualize_drafts as t


class Adv(t.FakeTimelines):
    head = "rev-head"

    def open_bundle(self, project, ref, revision_id=None):
        r = super().open_bundle(project, ref, revision_id)
        self.head = "rev-next"
        return r


def test_probe(tmp_path, monkeypatch, capsys):
    from astrid.sdk import timeline_checkout
    path = tmp_path / "main.json"
    path.write_text("{}")
    monkeypatch.setattr(timeline_checkout, "find_draft", lambda project, timeline, name="main", client=None: path)
    monkeypatch.setattr(timeline_checkout, "Checkout", t.FakeCheckout)
    c = t.FakeClient()
    c.timelines = Adv()
    print("CODE", t._visualize(["--json"], c))
    print("OUT<<" + capsys.readouterr().out + ">>")
    print("CALLS", c.timelines.visualize_calls)
    print("NOW", c.timelines.head)
