import {createRequire} from 'node:module';
import {privateGraphRoot} from './source/tests/e2e/timeline/tab-audio-capture.controller.mjs';
const require=createRequire(privateGraphRoot()+'/../package.json');
const {defineConfig}=require('@playwright/test');
export default defineConfig({
 testDir:'/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/source/tests/e2e/timeline',
 testMatch:'tab-audio-capture.probe.ts',
 outputDir:'/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate/output',
 workers:1,retries:0,
 projects:[{name:'native-codec-chrome155-tab-audio',use:{viewport:{width:1440,height:900},launchOptions:{executablePath:'/opt/google/chrome/chrome',ignoreDefaultArgs:['--mute-audio'],args:['--auto-accept-this-tab-capture','--enable-usermedia-screen-capturing','--allow-http-screen-capture','--disable-background-timer-throttling','--disable-renderer-backgrounding']}}}],
});
