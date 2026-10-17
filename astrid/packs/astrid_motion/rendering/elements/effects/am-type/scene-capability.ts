/** Prepare the selected drawing once in its browser; frame queries use only
 * immutable font ink/layout measurements. No text rectangle is opaque support. */
import {renderToStaticMarkup} from 'react-dom/server';
import {measureText} from '@remotion/layout-utils';
import type {ComponentCapabilityContext, PreparedComponentCapability, ComponentFrameSupport} from '@banodoco/timeline-composition/evaluation';
import type {ElementComponentProps} from '../../_shared/am';
import {amTypeDrawing} from './drawing';
import {amTypeLayout, amTypeReveal} from './layout';
import {easeOutCubic, finiteNumber} from '../../_shared/am';

type Rect = {x:number; y:number; width:number; height:number};
type Ink = {rect:Rect; chars:number[]; mask:Rect|null};
const emptyRect = ():Rect => ({x:0,y:0,width:0,height:0});
const unknown = (reason:string):ComponentFrameSupport => ({presence:'unknown',bounds:{status:'unknown',reason},opaqueSupport:'unknown'});
const absent:ComponentFrameSupport = {presence:'absent',bounds:{status:'known',rect:emptyRect()},opaqueSupport:'none'};
const intersection = (a:Rect,b:Rect):Rect => {
  const x=Math.max(a.x,b.x), y=Math.max(a.y,b.y);
  return {x,y,width:Math.max(0,Math.min(a.x+a.width,b.x+b.width)-x),height:Math.max(0,Math.min(a.y+a.height,b.y+b.height)-y)};
};
const union = (a:Rect,b:Rect):Rect => ({x:Math.min(a.x,b.x),y:Math.min(a.y,b.y),
  width:Math.max(a.x+a.width,b.x+b.width)-Math.min(a.x,b.x),height:Math.max(a.y+a.height,b.y+b.height)-Math.min(a.y,b.y)});
const finite = (r:Rect) => Object.values(r).every(Number.isFinite) && r.width>=0 && r.height>=0;
// These are the shipped, ASCII-covered faces. A Host supplies the authenticated
// selected-font digests, never authored params. Other faces retain honest unknown.
const fonts:Record<string,{file:string;digest:string}> = {
  'Gelasio/normal/400': {file:'Gelasio-Regular.woff2',digest:'698c2aa61ec1960371b6ed32e6120f028fa614613256f4b9e3f5d10ceb013eb5'},
  'Gelasio/italic/400': {file:'Gelasio-Italic.woff2',digest:'2df3d4a4d0cefc6440710666fa425627e54cb73707224bec044bca8e65940222'},
  'Departure Mono/normal/400': {file:'DepartureMono-Regular.woff2',digest:'5b4fed1daa90708aa9c6ee1190abca9dc22164a1c1def0020386e46b61038cfb'},
};
export const prepareAmTypeCapability = ({clip,width,height,rendererIdentity,fontDigests}:ComponentCapabilityContext):PreparedComponentCapability => {
  const params={...clip.params}, text=typeof params.text==='string'?params.text:'';
  const layout=amTypeLayout(params,8);
  const identity=JSON.stringify(['am-type/drawing-ink-v2',rendererIdentity,fontDigests,clip,width,height]);
  const unsupported=(reason:string):PreparedComponentCapability=>({identity,frame:()=>unknown(reason)});
  if (!text.trim()) return {identity,frame:()=>absent};
  const allowed=new Set(['text','font','size','color','align','x','y','width','reveal','tracking','lineHeight','italicWord','italicColor','underlineWord','underlineAt','fontFamily','bold','italic']);
  if (Object.keys(params).some(k=>!allowed.has(k)) || !/^[\x20-\x7e\n\r\t]+$/.test(text)
      || (params.font!==undefined&&!['display','label'].includes(String(params.font)))
      || (params.reveal!==undefined&&!['slideUp','type','none'].includes(String(params.reveal)))
      || (params.align!==undefined&&!['left','center','right'].includes(String(params.align)))
      || ['size','x','y','width','tracking','lineHeight','underlineAt'].some(k=>params[k]!==undefined&&(typeof params[k]!=='number'||!Number.isFinite(params[k])))
      || ['color','italicColor'].some(k=>params[k]!==undefined&&!/^#[a-f0-9]{6}$/i.test(String(params[k])))) return unsupported('Unsupported am-type parameters or unqualified glyph coverage');
  if (!rendererIdentity || typeof document==='undefined' || !document.fonts || !document.body)
    return unsupported('Selected browser/font identity is unavailable');
  // The inline drawing has CSS blurred shadows. Their painted extent is not a
  // font ink rectangle; do not silently bound this unsupported filter by a box.
  if (typeof params.fontFamily==='string') return unsupported('Inline text-shadow painted extent is undeclared');
  const host=document.createElement('div');
  Object.assign(host.style,{position:'absolute',left:'0px',top:'0px',width:`${width}px`,height:`${height}px`,visibility:'hidden',pointerEvents:'none',fontSize:'16px'});
  const inks:Ink[]=[], bars:Rect[]=[];
  let lineHeight=0, mask:Rect|null=null;
  try {
    // This is the very React subtree used by AmType, including inline runs,
    // white-space, wrapping, mask padding/margins and underline placement.
    host.innerHTML=renderToStaticMarkup(amTypeDrawing({clip,params} as ElementComponentProps,8));
    document.body.appendChild(host);
    const origin=host.getBoundingClientRect();
    const box=(r:DOMRect):Rect=>({x:r.left-origin.left,y:r.top-origin.top,width:r.width,height:r.height});
    const maskNode=host.firstElementChild?.firstElementChild as HTMLElement|null;
    const line=maskNode?.firstElementChild as HTMLElement|null;
    if (!maskNode || !line) throw new Error('Selected drawing structure unavailable');
    lineHeight=line.getBoundingClientRect().height;
    mask=box(maskNode.getBoundingClientRect());
    const canvas=document.createElement('canvas'), context=canvas.getContext('2d');
    if (!context) throw new Error('Selected browser ink metrics unavailable');
    const baselines=new Map<string,number>();
    const baselineOffset=(style:CSSStyleDeclaration):number=>{
      const key=[style.fontFamily,style.fontSize,style.fontWeight,style.fontStyle].join('/');
      const cached=baselines.get(key);if(cached!==undefined)return cached;
      const reference=document.createElement('span');
      Object.assign(reference.style,{position:'absolute',left:'0px',top:'0px',whiteSpace:'pre',fontFamily:style.fontFamily,fontSize:style.fontSize,fontWeight:style.fontWeight,fontStyle:style.fontStyle,lineHeight:style.lineHeight});
      const sample=document.createTextNode('Hg'), marker=document.createElement('span');
      Object.assign(marker.style,{display:'inline-block',width:'0px',height:'0px',verticalAlign:'baseline'});
      reference.append(sample,marker);host.appendChild(reference);
      const range=document.createRange();range.selectNodeContents(sample);
      const offset=marker.getBoundingClientRect().top-range.getBoundingClientRect().top;
      reference.remove();if(!Number.isFinite(offset))throw new Error('Unresolved actual font baseline');
      baselines.set(key,offset);return offset;
    };
    const walker=document.createTreeWalker(line,NodeFilter.SHOW_TEXT);
    let node:Node|null, charIndex=0;
    while ((node=walker.nextNode())) {
      const value=node.textContent??'', parent=node.parentElement!;
      const style=getComputedStyle(parent), family=style.fontFamily.replace(/["']/g,'');
      const face=fonts[`${family}/${style.fontStyle}/${style.fontWeight}`];
      if (!face || fontDigests[face.file]!==face.digest || !document.fonts.check(`${style.fontStyle} ${style.fontWeight} ${style.fontSize} "${family}"`,value))
        throw new Error('Unqualified, stale or unresolved selected font face');
      // Browser layout-utils checks this same selected font. DOM Range below
      // supplies actual wrapped run positions, rather than reimplementing wrap.
      measureText({text:value,fontFamily:family,fontSize:parseFloat(style.fontSize),fontWeight:style.fontWeight,validateFontIsLoaded:true,
        additionalStyles:{fontStyle:style.fontStyle,['--astrid-font-identity' as 'fontFeatureSettings']:rendererIdentity}});
      context.font=`${style.fontStyle} ${style.fontWeight} ${style.fontSize} "${family}"`;
      if (!('letterSpacing' in context)) throw new Error('Browser letter-spacing ink measurement unavailable');
      context.letterSpacing=style.letterSpacing==='normal'?'0px':style.letterSpacing;
      // Each character is already an individual span in the actual drawing.
      // Whitespace is not ink and does not advance the drawing's type counter.
      for(let i=0;i<value.length;i++) {
        const ch=value[i];
        if (/\s/.test(ch)) continue;
        const index=charIndex++;
        const range=document.createRange();range.setStart(node,i);range.setEnd(node,i+1);
        const r=box(range.getBoundingClientRect());
        const glyph=style.textTransform==='uppercase'?ch.toUpperCase():ch;
        const metrics=context.measureText(glyph);
        // Resolve the actual DOM baseline separately from the font ink metrics.
        // Font bounding boxes also guard unexpected Range/font disagreement.
        if (![metrics.fontBoundingBoxAscent,metrics.fontBoundingBoxDescent,metrics.actualBoundingBoxAscent,metrics.actualBoundingBoxDescent,metrics.actualBoundingBoxLeft,metrics.actualBoundingBoxRight].every(Number.isFinite)
            || Math.abs(r.height-metrics.fontBoundingBoxAscent-metrics.fontBoundingBoxDescent)>1.01)
          throw new Error('Selected font baseline geometry unavailable');
        const baseline=r.y+baselineOffset(style);
        const rect={x:r.x-metrics.actualBoundingBoxLeft,y:baseline-metrics.actualBoundingBoxAscent,
          width:metrics.actualBoundingBoxLeft+metrics.actualBoundingBoxRight,height:metrics.actualBoundingBoxAscent+metrics.actualBoundingBoxDescent};
        if (!finite(rect)) throw new Error('Invalid selected glyph ink metrics');
        if(rect.width>0&&rect.height>0) inks.push({rect,chars:[index],mask});
      }
    }
    for(const bar of Array.from(line.querySelectorAll<HTMLElement>('[aria-hidden]'))) {
      bar.style.width='100%'; const r=box(bar.getBoundingClientRect());
      if(!finite(r)) throw new Error('Invalid underline geometry');
      bars.push(r);
    }
    if(!finite(mask)||!Number.isFinite(lineHeight)) throw new Error('Invalid mask geometry');
  } catch(error) {
    return unsupported(error instanceof Error?error.message:'Selected browser drawing preparation unavailable');
  } finally {host.remove();}
  const frozen=JSON.parse(JSON.stringify({inks,bars,mask,lineHeight}));
  return {identity:JSON.stringify([identity,frozen]),frame:(frame:number)=>{
    if(!Number.isFinite(frame)) return unknown('Invalid component frame');
    let bounds:Rect|null=null, proven=false, ambiguous=false, canvasCandidate=false;
    const slide=layout.reveal==='slideUp'&&frame<8;
    const dy=slide?amTypeReveal(frame).slideFraction*lineHeight:0;
    const add=(r:Rect, glyph:boolean)=>{
      let clipped=r;
      if(slide&&mask)clipped=intersection(r,mask);
      if(clipped.width<=0||clipped.height<=0)return;
      bounds=bounds?union(bounds,clipped):clipped;
      // Full ink, or a vertical mask containing an ink extremum while
      // retaining its full width, proves presence. Arbitrary 2D cuts do not.
      const visible=intersection(clipped,{x:0,y:0,width,height});
      if(visible.width<=0||visible.height<=0)return;
      canvasCandidate=true;
      // A two-dimensional corner of an ink box need not contain glyph ink.
      // A full axis with a retained extremum does; a solid underline always does.
      const certain=!glyph || (visible.width===r.width
        && (visible.y===r.y||visible.y+visible.height===r.y+r.height))
        || (visible.height===r.height
          && (visible.x===r.x||visible.x+visible.width===r.x+r.width));
      if(certain)proven=true;else ambiguous=true;
    };
    for(const ink of inks) {
      if(layout.reveal==='type'&&ink.chars[0]>=amTypeReveal(frame).visibleChars)continue;
      add({...ink.rect,y:ink.rect.y+dy},true);
    }
    const fraction=easeOutCubic((frame-finiteNumber(params.underlineAt,0))/6);
    if(fraction>0)for(const bar of bars)add({...bar,y:bar.y+dy,width:bar.width*fraction},false);
    if(!bounds)return absent;
    return {presence:!canvasCandidate?'absent':!proven&&ambiguous?'unknown':'present',
      bounds:{status:'known',rect:bounds},opaqueSupport:'none'};
  }};
};
