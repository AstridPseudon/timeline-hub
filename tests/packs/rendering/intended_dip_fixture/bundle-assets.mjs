import {constants, copyFileSync} from 'node:fs';
import path from 'node:path';

export function exposeDeclaredImages(bundleDirectory) {
  // Remotion copies publicDir into <bundle>/public, but the unchanged film
  // requests these two images at the renderer's bundle URL root.
  for (const name of ['plate.png', 'footage.png']) {
    copyFileSync(path.join(bundleDirectory, 'public', name),
      path.join(bundleDirectory, name), constants.COPYFILE_EXCL);
  }
}
