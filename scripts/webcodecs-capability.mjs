import {createServer} from 'node:http';
import {mkdtemp, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {chromium} from 'playwright';

const executablePath = process.env.WEB_CODECS_CHROME ?? '/opt/google/chrome/chrome';
const width = 1920;
const height = 1080;
const config = {
  codec: 'avc1.640028',
  width,
  height,
  bitrate: 3_000_000,
  alpha: 'discard',
  avc: {format: 'avc'},
};

const asError = (error) => ({
  name: error?.name ?? typeof error,
  message: error?.message ?? String(error),
  code: error?.code ?? null,
  string: String(error),
});

const probe = async (page) => page.evaluate(async ({config, width, height}) => {
  const result = {
    api: typeof VideoEncoder === 'function' ? 'present' : 'missing',
    config,
    support: null,
    initialization: null,
  };

  if (typeof VideoEncoder !== 'function') {
    return result;
  }

  try {
    const support = await VideoEncoder.isConfigSupported(config);
    result.support = {
      supported: support.supported,
      config: support.config ?? null,
    };

    if (!support.supported) {
      return result;
    }
  } catch (error) {
    result.support = {error: {
      name: error?.name ?? typeof error,
      message: error?.message ?? String(error),
      code: error?.code ?? null,
      string: String(error),
    }};
    return result;
  }

  const chunks = [];
  let callbackError = null;
  let encoder = null;
  let frame = null;
  try {
    encoder = new VideoEncoder({
      output: (chunk) => chunks.push({
        type: chunk.type,
        timestamp: chunk.timestamp,
        duration: chunk.duration ?? null,
        byteLength: chunk.byteLength,
      }),
      error: (error) => {
        callbackError = {
          name: error?.name ?? typeof error,
          message: error?.message ?? String(error),
          code: error?.code ?? null,
          string: String(error),
        };
      },
    });
    const stateBeforeConfigure = encoder.state;
    encoder.configure(config);
    const stateAfterConfigure = encoder.state;
    frame = new VideoFrame(new Uint8Array(width * height * 4), {
      format: 'RGBA',
      codedWidth: width,
      codedHeight: height,
      timestamp: 0,
    });
    encoder.encode(frame, {keyFrame: true});
    frame.close();
    frame = null;
    await encoder.flush();
    result.initialization = {
      stateBeforeConfigure,
      stateAfterConfigure,
      stateAfterFlush: encoder.state,
      chunks,
      callbackError,
    };
  } catch (error) {
    result.initialization = {
      chunks,
      callbackError,
      error: {
        name: error?.name ?? typeof error,
        message: error?.message ?? String(error),
        code: error?.code ?? null,
        string: String(error),
      },
    };
  } finally {
    frame?.close();
    encoder?.close();
  }

  return result;
}, {config, width, height});

const main = async () => {
  const profile = await mkdtemp(join(tmpdir(), 'timeline-webcodecs-profile-'));
  const server = createServer((request, response) => {
    response.writeHead(200, {'content-type': 'text/html'});
    response.end('<!doctype html><title>WebCodecs capability probe</title>');
  });
  let context;
  try {
    await new Promise((resolve, reject) => {
      server.once('error', reject);
      server.listen(0, '127.0.0.1', resolve);
    });
    const address = server.address();
    if (!address || typeof address === 'string') throw new Error('Loopback probe server did not expose a port');
    context = await chromium.launchPersistentContext(profile, {
      executablePath,
      headless: true,
    });
    const page = await context.newPage();
    await page.goto(`http://127.0.0.1:${address.port}/`);
    const result = await probe(page);
    console.log(JSON.stringify({
      result,
      executablePath,
      profile,
    }, null, 2));
  } finally {
    await context?.close();
    await new Promise((resolve) => server.close(resolve));
    await rm(profile, {recursive: true, force: true});
  }
};

try {
  await main();
} catch (error) {
  console.error(JSON.stringify({error: asError(error)}, null, 2));
  process.exitCode = 1;
}
