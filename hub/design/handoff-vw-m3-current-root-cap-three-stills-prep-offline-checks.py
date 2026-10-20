"""One-off instrument calibration against the retained MAIN PNGs; no new capture."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

from PIL import Image

prefix = Path(__file__).with_name('handoff-vw-m3-current-root-cap-three-stills-prep-')
spec = importlib.util.spec_from_file_location('current_cap', str(prefix) + 'controller.py')
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)
assert not controller.output('CAPTURE-GRANT.txt').exists()
assert not controller.output('CAPTURE-STARTED').exists()
try:
    controller.grant()
except FileNotFoundError:
    pass
else:
    raise AssertionError('capture accepted without a grant')
reference_prefix = controller.MAIN
with tempfile.TemporaryDirectory(prefix='vw-cap-check-', dir=controller.OWN) as folder:
    folder = Path(folder)
    controller.output = lambda name: folder / name
    for frame in controller.FRAMES:
        shutil.copyfile(Path(str(reference_prefix) + f'frame-{frame}.png'), controller.output(f'frame-{frame}.png'))
    controller.compare()
    assert json.loads(controller.output('comparison.json').read_text())['pass']
    path = controller.output('frame-105.png')
    with Image.open(path) as source:
        image = source.copy()
    original = image.getpixel((0, 0))
    for delta, expected in ((2, True), (3, False)):
        image.putpixel((0, 0), (original[0] + delta, *original[1:]))
        image.save(path)
        try:
            controller.compare()
        except RuntimeError:
            assert not expected
        report = json.loads(controller.output('comparison.json').read_text())
        assert report['pass'] is expected
        assert report['files']['105']['max_rgb_channel_difference_255'] == delta
        assert report['files']['105']['pixels_exceeding_2_255'] == (0 if expected else 1)
    Image.new('RGB', (1920, 1079), (240, 240, 240)).save(path)  # Wrong-size input must be refused.
    try:
        controller.compare()
    except RuntimeError as exc:
        assert 'dimensions' in str(exc)
    else:
        raise AssertionError('wrong-size PNG accepted')
print('PASS: missing-grant refusal; exact 3-PNG all-pixel positive; +2 accepted; one pixel +3 rejected; wrong dimensions rejected. No browser/render.')
