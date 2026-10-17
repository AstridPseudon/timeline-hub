export const VIDEO_INTERPRETATION = 'remotion-media/html-video/first-video/h264-yuv-v1';
export const IMAGE_INTERPRETATION = 'remotion-image/jpeg-v1';
const digest = (value) => typeof value === 'string'
    && /^(?:sha256:)?[a-f0-9]{64}$/.test(value) ? value.replace(/^sha256:/, '') : null;
export const provenOpaqueMedia = (asset, proof) => {
    if (!asset || !proof || proof.version !== 1 || ![VIDEO_INTERPRETATION, IMAGE_INTERPRETATION].includes(proof.interpretation))
        return false;
    const content = digest(asset.content_sha256);
    const s = proof.stream;
    return content !== null && proof.objectId === 'sha256:' + content
        && proof.contentSha256 === content && proof.file === asset.file
        && ((proof.interpretation === VIDEO_INTERPRETATION && s?.codec === 'h264' && !asset.type?.startsWith('image')
            && ['Constrained Baseline', 'Baseline', 'Main', 'High'].includes(s.profile ?? '')
            && /^\d+$/.test(s.level ?? '') && Number(s.level) >= 10 && Number(s.level) <= 52
            && ['yuv420p', 'yuvj420p'].includes(s.pixelFormat))
            || (proof.interpretation === IMAGE_INTERPRETATION && s?.codec === 'mjpeg' && asset.type?.startsWith('image') === true))
        && ['yuv420p', 'yuvj420p', 'yuv422p', 'yuvj422p', 'yuv444p', 'yuvj444p'].includes(s.pixelFormat)
        && s.sampleAspectRatio === '1:1'
        && Number.isSafeInteger(s.index) && s.index >= 0
        && Number.isSafeInteger(s.width) && s.width > 0 && Number.isSafeInteger(s.height) && s.height > 0
        && asset.resolution === s.width + 'x' + s.height;
};
