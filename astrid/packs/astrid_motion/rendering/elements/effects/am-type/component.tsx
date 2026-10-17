import {amTypeLayout, amTypeReveal} from './layout';
import {prepareAmTypeCapability} from './scene-capability';
import type {CSSProperties, ReactElement} from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {
  COLOR,
  FAMILY,
  clamp,
  easeOutCubic,
  finiteNumber,
  narrowParams,
  oneOf,
  type ElementComponentProps,
} from '../../_shared/am';

// am-type: editorial type. Type may ease (masked slide-up uses ease-out
// cubic); the typewriter reveal and the underline step on frames.

type Params = {
  text?: string;
  italicWord?: string;
  /** Colour of the italic word (default rust #A94714; use orange on charcoal, where rust is too dark). */
  italicColor?: string;
  font?: 'display' | 'label';
  fontFamily?: string;
  bold?: boolean;
  italic?: boolean;
  size?: number;
  color?: string;
  align?: 'left' | 'center' | 'right';
  x?: number;
  y?: number;
  width?: number;
  reveal?: 'slideUp' | 'type' | 'none';
  tracking?: number;
  lineHeight?: number;
  underlineWord?: string;
  underlineAt?: number;
};

const UNDERLINE_FRAMES = 6;
const UNDERLINE_PX = 6;
const ALIGNS = ['left', 'center', 'right'] as const;

type Run = {text: string; italic: boolean; underline: boolean; space: boolean};

// Split into word and whitespace runs. The first word matching italicWord
// (and the first matching underlineWord) is styled. Punctuation is ignored
// when matching, so "tomorrow." matches "tomorrow".
const buildRuns = (text: string, italicWord: string, underlineWord: string): Run[] => {
  const cleaned = (token: string): string => token.replace(/[^\p{L}\p{N}']/gu, '').toLowerCase();
  let italicUsed = false;
  let underlineUsed = false;
  return text.split(/(\s+)/).filter((part) => part.length > 0).map((part) => {
    if (/^\s+$/.test(part)) {
      return {text: part, italic: false, underline: false, space: true};
    }
    const key = cleaned(part);
    const italic = !italicUsed && italicWord !== '' && key === italicWord.toLowerCase();
    if (italic) italicUsed = true;
    const underline = !underlineUsed && underlineWord !== '' && key === underlineWord.toLowerCase();
    if (underline) underlineUsed = true;
    return {text: part, italic, underline, space: false};
  });
};

export default function AmType(props: ElementComponentProps): ReactElement | null {
  const frame = useCurrentFrame();
  const params = narrowParams<Params>(props.params);
  const text = typeof params.text === 'string' ? params.text : '';
  if (!text.trim()) {
    return null;
  }

  // Explicit inline typography uses the same canonical clip geometry that the
  // App constructor/inspector edits. No params geometry mirror or second box.
  // Editorial am-type and transcript captions retain the original path below.
  if (typeof params.fontFamily === 'string') {
    return (
      <AbsoluteFill style={{
        left: finiteNumber(props.clip.x, 120),
        top: finiteNumber(props.clip.y, 120),
        width: finiteNumber(props.clip.width, 640),
        height: finiteNumber(props.clip.height, 180),
        position: 'absolute',
        justifyContent: 'center',
        color: params.color ?? '#ffffff',
        fontFamily: params.fontFamily,
        fontSize: Math.max(1, finiteNumber(params.size, 64)),
        fontWeight: params.bold ? 700 : 400,
        fontStyle: params.italic ? 'italic' : 'normal',
        textAlign: oneOf(params.align, ALIGNS, 'center'),
        whiteSpace: 'pre-wrap',
        lineHeight: 1.1,
        textShadow: '0 2px 4px rgba(0, 0, 0, 0.95), 0 2px 18px rgba(0, 0, 0, 0.8)',
        // ClipLook applies canonical clip opacity exactly once.
      }}>
        {text}
      </AbsoluteFill>
    );
  }

  const layout = amTypeLayout(params as Record<string, unknown>, frame);
  const {reveal} = layout;

  const italicWord = typeof params.italicWord === 'string' ? params.italicWord.trim() : '';
  const underlineWord = typeof params.underlineWord === 'string' ? params.underlineWord.trim() : '';
  const runs = buildRuns(text, italicWord, underlineWord);

  // Underline draw-in: 6 frames, eased, from underlineAt. Before it starts the
  // background size is 0 and nothing shows.
  const underlineStart = finiteNumber(params.underlineAt, 0);
  const underlineP = easeOutCubic((frame - underlineStart) / UNDERLINE_FRAMES);

  // Typewriter reveal: one character every 2 frames, first character on frame 0.
  const {visibleChars} = amTypeReveal(frame);
  let charIndex = 0;

  const renderChars = (value: string, key: string): ReactElement[] => {
    const chars = Array.from(value);
    return chars.map((ch, i) => {
      const index = charIndex;
      charIndex += 1;
      const shown = reveal !== 'type' || index < visibleChars;
      return (
        <span key={`${key}-${i}`} style={{opacity: shown ? 1 : 0}}>
          {ch}
        </span>
      );
    });
  };

  const underlineFraction = clamp(underlineP, 0, 1);
  const body = runs.map((run, index) => {
    if (run.space) {
      return <span key={`s-${index}`}>{run.text}</span>;
    }
    // A run can be both the italic word and the underlined word, so the two
    // style sets are merged. The underline is an absolutely positioned bar
    // whose width steps with the eased progress. A background-size gradient on
    // an inline span did not paint in the Remotion renderer.
    const runStyle: CSSProperties = {};
    if (run.italic) {
      Object.assign(runStyle, {fontFamily: FAMILY.display, fontStyle: 'italic', color: params.italicColor ?? COLOR.rust, textTransform: 'none'});
    }
    if (run.underline) {
      runStyle.position = 'relative';
      runStyle.display = 'inline-block';
    }
    return (
      <span key={`w-${index}`} style={runStyle}>
        {renderChars(run.text, `w-${index}`)}
        {run.underline ? (
          <span
            aria-hidden
            style={{
              position: 'absolute',
              left: 0,
              bottom: '-0.1em',
              height: UNDERLINE_PX,
              width: `${underlineFraction * 100}%`,
              backgroundColor: COLOR.orange,
            }}
          />
        ) : null}
      </span>
    );
  });

  const {mask, line} = layout;

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={mask}>
        <div style={line}>{body}</div>
      </div>
    </AbsoluteFill>
  );
}

// Selected registry wrappers forward this declaration from the same implementation.
AmType.prepareSceneCapability = prepareAmTypeCapability;
