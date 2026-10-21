import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createServer, request } from 'node:http';
import { lstatSync, readFileSync, readdirSync, realpathSync } from 'node:fs';
import path from 'node:path';

const hash = bytes => createHash('sha256').update(bytes).digest('hex');
export function assertDist(dist) {
  assert.equal(realpathSync(dist), path.resolve(dist), 'dist must be a real directory');
  const files = [];
  function visit(directory) {
    for (const name of readdirSync(directory).sort()) {
      const absolute = path.join(directory, name);
      const info = lstatSync(absolute);
      if (info.isDirectory()) visit(absolute);
      else {
        assert(info.isFile(), `dist member must be a regular file: ${absolute}`);
        files.push([path.relative(dist, absolute), hash(readFileSync(absolute))]);
      }
    }
  }
  visit(dist);
  assert.equal(files.length, 339, 'retained dist file count changed');
  const index = hash(readFileSync(path.join(dist, 'index.html')));
  assert.equal(index, 'aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b');
  return { path: dist, files: files.length, index, sha256: hash(JSON.stringify(files)) };
}

export async function availabilityGet(dist) {
  const before = assertDist(dist);
  const expected = readFileSync(path.join(dist, 'index.html'));
  const server = createServer((req, res) => {
    if (req.method !== 'GET' || req.url !== '/') {
      res.writeHead(404); res.end(); return;
    }
    res.writeHead(200, { 'content-type': 'text/html', connection: 'close' });
    res.end(expected);
  });
  let result;
  try {
    await new Promise((resolve, reject) => {
      server.once('error', reject);
      server.listen(0, '127.0.0.1', resolve);
    });
    const port = server.address().port;
    result = await new Promise((resolve, reject) => {
      const client = request({ hostname: '127.0.0.1', port, path: '/', method: 'GET', timeout: 5000 }, response => {
        const chunks = [];
        response.on('data', chunk => chunks.push(chunk));
        response.on('error', reject);
        response.on('end', () => {
          const bytes = Buffer.concat(chunks);
          resolve({ method: 'GET', url: `http://127.0.0.1:${port}/`, status: response.statusCode,
            bytes: bytes.length, sha256: hash(bytes), exact: bytes.equals(expected) });
        });
      });
      client.on('timeout', () => client.destroy(new Error('localhost GET timed out')));
      client.on('error', reject);
      client.end();
    });
    assert.equal(result.status, 200);
    assert.equal(result.exact, true);
    assert.equal(result.sha256, before.index);
  } finally {
    if (server.listening) {
      server.closeAllConnections();
      await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
    }
  }
  assert.deepEqual(assertDist(dist), before);
  return { ...result, privateServerClosed: !server.listening };
}
