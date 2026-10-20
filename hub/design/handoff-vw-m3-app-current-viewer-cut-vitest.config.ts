import { defineConfig } from 'vitest/config';
import base from './config/testing/vitest.config';
import path from 'node:path';
export default defineConfig({ ...base, cacheDir: path.resolve(__dirname, '.test-cache') });
